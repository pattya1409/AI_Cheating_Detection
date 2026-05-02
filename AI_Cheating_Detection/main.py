import cv2
import mediapipe as mp
import numpy as np
from mobile_detector import MobileDetector
from ultralytics import YOLO   # ✅ YOLOv8 IMPORT

mp_face_mesh = mp.solutions.face_mesh

# ✅ Load YOLOv8 model
model = YOLO("yolov8n.pt")

# ✅ FIXED LEFT / RIGHT HEAD TURN DETECTION
def detect_head_turn(landmarks):
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    nose = landmarks[1]

    face_center = (left_eye.x + right_eye.x) / 2
    offset = nose.x - face_center

    # ✅ Sensitive & correct thresholds
    if offset > 0.04:
        return "Looking Right"
    elif offset < -0.04:
        return "Looking Left"
    return "Normal"

# ✅ FIXED MOUTH / SPEAKING DETECTION
def detect_mouth_open(landmarks):
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]

    open_value = abs(top_lip.y - bottom_lip.y)

    # ✅ Sensitive enough for real talking
    if open_value > 0.025:
        return True
    return False

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Error: Could not open camera.')
        return

    mobile_detector = MobileDetector()

    with mp_face_mesh.FaceMesh(
            max_num_faces=4,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            h, w = frame.shape[:2]

            suspicious = []
            face_count = 0
            person_count = 0

            # ✅========== FACE + TALK + HEAD TURN DETECTION ==========
            if results.multi_face_landmarks:
                face_count = len(results.multi_face_landmarks)

                if face_count > 1:
                    suspicious.append("Multiple Faces")

                for face_landmarks in results.multi_face_landmarks:
                    landmarks = face_landmarks.landmark

                    head = detect_head_turn(landmarks)
                    if head != "Normal":
                        suspicious.append(head)

                    if detect_mouth_open(landmarks):
                        suspicious.append("Talking")

                    xs = [int(l.x * w) for l in landmarks]
                    ys = [int(l.y * h) for l in landmarks]
                    x1, x2 = min(xs), max(xs)
                    y1, y2 = min(ys), max(ys)
                    cv2.rectangle(frame, (x1-10, y1-10), (x2+10, y2+10), (0,255,0), 1)

            # ✅========== YOLOv8 OBJECT DETECTION ==========
            yolo_results = model(frame, stream=True, verbose=False)

            for r in yolo_results:
                boxes = r.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    conf = float(box.conf[0])

                    if conf > 0.5:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        if label == "person":
                            person_count += 1
                            text = "Person"
                        elif label == "cell phone":
                            suspicious.append("Mobile Phone Detected")
                            text = "⚠ Mobile Phone"
                        elif label == "book":
                            suspicious.append("Book Detected")
                            text = "⚠ Book"
                        else:
                            continue

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # ✅ FINAL ✅ CORRECT EXTRA PERSON LOGIC
            if person_count > face_count and face_count > 0:
                suspicious.append("Extra Person Detected")

            # ✅========== OLD MOBILE DETECTOR (OPTIONAL BACKUP) ==========
            mobile_found = mobile_detector.detect(frame)
            if mobile_found:
                suspicious.append("Mobile Phone Detected")

            # ✅========== DISPLAY STATUS ==========
            y = 30
            if suspicious:
                unique_alerts = list(set(suspicious))
                cv2.putText(frame, "Suspicious: " + ", ".join(unique_alerts), (10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            else:
                cv2.putText(frame, "Status: Normal", (10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            cv2.imshow("AI Cheating Detection System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
