import cv2
import mediapipe as mp
import numpy as np
from mobile_detector import MobileDetector

mp_face_mesh = mp.solutions.face_mesh

def detect_head_turn(landmarks):
    # Simple left/right check using eyes (normalized coords)
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    horizontal_move = right_eye.x - left_eye.x
    if horizontal_move > 0.15:
        return "Looking Right"
    elif horizontal_move < -0.15:
        return "Looking Left"
    return "Normal"

def detect_mouth_open(landmarks):
    # lips indices (approx) from MediaPipe FaceMesh
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]
    open_value = abs(top_lip.y - bottom_lip.y)
    if open_value > 0.05:
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

            if results.multi_face_landmarks:
                if len(results.multi_face_landmarks) > 1:
                    suspicious.append("Multiple faces detected")

                for face_landmarks in results.multi_face_landmarks:
                    landmarks = face_landmarks.landmark

                    head = detect_head_turn(landmarks)
                    if head != "Normal":
                        suspicious.append(head)

                    if detect_mouth_open(landmarks):
                        suspicious.append("Talking")

                    # Draw simple face bounding box (approx)
                    xs = [int(l.x * w) for l in landmarks]
                    ys = [int(l.y * h) for l in landmarks]
                    x1, x2 = min(xs), max(xs)
                    y1, y2 = min(ys), max(ys)
                    cv2.rectangle(frame, (x1-10, y1-10), (x2+10, y2+10), (0,255,0), 1)

            # Mobile detection (if model available)
            mobile_found = mobile_detector.detect(frame)
            if mobile_found:
                suspicious.append("Mobile phone detected")

            # Overlay suspicious messages
            y = 30
            if suspicious:
                cv2.putText(frame, "Suspicious: " + ", ".join(suspicious), (10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            else:
                cv2.putText(frame, "Status: Normal", (10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            cv2.imshow("AI Cheating Detection System", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
