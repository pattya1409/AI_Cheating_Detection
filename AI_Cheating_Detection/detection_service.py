import mediapipe as mp
import numpy as np
import cv2
import os
from datetime import datetime
from ultralytics import YOLO
from database import save_detection


class DetectionService:
    def __init__(self):
        # Load YOLOv8 model - this will download a fresh model if needed
        try:
            print("Loading YOLOv8 model...")
            self.model = YOLO("yolov8n.pt")
            print("YOLOv8 model loaded successfully!")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            # Fallback: create a dummy model for testing
            self.model = None

        # MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Camera & state
        self.cap = None
        self.running = False

        # Session info
        self.session_id = None
        self.examiner_id = None

        # Latest alert (for dashboard)
        self.latest_alert = None

        # Evidence folder
        self.evidence_dir = "static/evidence/screenshots"
        os.makedirs(self.evidence_dir, exist_ok=True)

    # ---------------- START DETECTION ----------------
    def start_detection(self, session_id, examiner_id):
        if self.running:
            print("Detection already running")
            return

        self.session_id = session_id
        self.examiner_id = examiner_id

        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                # Try without DirectShow on non-Windows systems
                self.cap = cv2.VideoCapture(0)
                if not self.cap.isOpened():
                    raise RuntimeError("Failed to access camera. Please check camera connection.")

            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            self.running = True
            print("Detection started successfully")
        except Exception as e:
            print(f"Error starting detection: {e}")
            raise RuntimeError(f"Failed to start camera: {str(e)}")

    # ---------------- STOP DETECTION ----------------
    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    # ---------------- VIDEO STREAM ----------------
    def generate_frames(self):
        while self.running and self.cap:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read frame from camera")
                    break

                result = self.process_frame(frame)

                if result["behaviors"]:
                    self.latest_alert = {
                        "timestamp": datetime.now().isoformat(),
                        "behaviors": result["behaviors"],
                        "evidence_path": result["evidence"]
                    }
                    
                    # Save detection to database for live updates
                    try:
                        save_detection(
                            session_id=self.session_id,
                            behaviors=result["behaviors"],
                            evidence_path=result["evidence"],
                            person_count=result.get("person_count", 0),
                            face_count=result.get("face_count", 0)
                        )
                    except Exception as e:
                        print(f"Error saving detection: {e}")

                _, buffer = cv2.imencode(".jpg", result["frame"])
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" +
                    buffer.tobytes() +
                    b"\r\n"
                )
            except Exception as e:
                print(f"Error in video stream: {e}")
                break

    # ---------------- HEAD & MOUTH DETECTION ----------------
    def detect_head_direction(self, landmarks):
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose = landmarks[1]

        eye_center_x = (left_eye.x + right_eye.x) / 2
        offset = nose.x - eye_center_x

        if offset > 0.04:
            return "Looking Right"
        elif offset < -0.04:
            return "Looking Left"
        return None

    def detect_talking(self, landmarks):
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]
        return abs(upper_lip.y - lower_lip.y) > 0.025

    # ---------------- DETECTION LOGIC ----------------
    def process_frame(self, frame):
        suspicious = []
        person_count = 0
        face_count = 0

        # -------- FACE ANALYSIS --------
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = self.face_mesh.process(rgb)

        if face_results.multi_face_landmarks:
            face_count = len(face_results.multi_face_landmarks)
            landmarks = face_results.multi_face_landmarks[0].landmark

            head_state = self.detect_head_direction(landmarks)
            if head_state:
                suspicious.append(head_state)

            if self.detect_talking(landmarks):
                suspicious.append("Talking")

        # -------- YOLO OBJECT DETECTION --------
        if self.model is not None:
            try:
                results = self.model(frame, verbose=False)
                
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        label = self.model.names[cls]
                        conf = float(box.conf[0])

                        if conf < 0.5:
                            continue

                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        if label == "person":
                            person_count += 1
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        if label == "cell phone":
                            suspicious.append("Mobile Phone")
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            except Exception as e:
                print(f"YOLO detection error: {e}")
        else:
            print("YOLO model not available - skipping object detection")

        # Check for multiple people (suspicious behavior)
        if person_count > 1:
            suspicious.append("Multiple People")

        # -------- SAVE EVIDENCE --------
        evidence_path = None
        if suspicious:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            evidence_path = f"{self.evidence_dir}/alert_{ts}.jpg"
            cv2.imwrite(evidence_path, frame)

        return {
            "behaviors": list(set(suspicious)),
            "frame": frame,
            "evidence": evidence_path,
            "person_count": person_count,
            "face_count": face_count
        }

    # ---------------- VIDEO UPLOAD PROCESSING ----------------
    def process_video(self, video_path, session_id, examiner_id):
        """Process uploaded video file and detect suspicious behaviors"""
        results = {
            "total_frames": 0,
            "suspicious_frames": 0,
            "detections": [],
            "behaviors_summary": {},
            "status": "processing"
        }
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                results["status"] = "error"
                results["message"] = "Failed to open video file"
                return results
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            results["total_frames"] = total_frames
            results["fps"] = fps
            
            frame_count = 0
            # Process every 5th frame for efficiency
            frame_skip = 5
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames for efficiency
                if frame_count % frame_skip != 0:
                    continue
                
                # Process frame
                result = self.process_frame(frame)
                
                if result["behaviors"]:
                    results["suspicious_frames"] += 1
                    
                    # Save detection
                    timestamp = frame_count / fps
                    detection = {
                        "frame_number": frame_count,
                        "timestamp": f"{int(timestamp // 60)}:{int(timestamp % 60):02d}",
                        "behaviors": result["behaviors"],
                        "evidence_path": result["evidence"]
                    }
                    results["detections"].append(detection)
                    
                    # Update behaviors summary
                    for behavior in result["behaviors"]:
                        results["behaviors_summary"][behavior] = results["behaviors_summary"].get(behavior, 0) + 1
                    
                    # Save to database
                    try:
                        save_detection(
                            session_id=session_id,
                            behaviors=result["behaviors"],
                            evidence_path=result["evidence"],
                            person_count=result.get("person_count", 0),
                            face_count=result.get("face_count", 0)
                        )
                    except Exception as e:
                        print(f"Error saving detection: {e}")
            
            cap.release()
            results["status"] = "completed"
            results["message"] = f"Processed {total_frames} frames, found {results['suspicious_frames']} suspicious frames"
            
        except Exception as e:
            results["status"] = "error"
            results["message"] = f"Error processing video: {str(e)}"
        
        return results
