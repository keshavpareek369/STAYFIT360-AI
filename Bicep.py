import cv2
import numpy as np
import mediapipe as mp
import joblib
import time
import os
import platform
import csv

# === Constants ===
MODEL_PATH = 'D:/Minor Project-2/knn_model.pkl'
CSV_OUTPUT = "Biceps-final.csv"
CAM_INDEX = 0

# === Load Trained Model ===
model = joblib.load(MODEL_PATH)

# === Initialize MediaPipe ===
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# === Utility Functions ===
def calculate_angle(a, b, c):
    """Returns the angle at point b given three 2D/3D points a, b, c."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(np.degrees(radians))
    return angle if angle <= 180 else 360 - angle

def beep():
    """Plays a beep on posture error based on OS."""
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 300)
    elif platform.system() == "Darwin":  # macOS
        os.system('afplay /System/Library/Sounds/Ping.aiff')
    else:  # Linux
        os.system('play -nq -t alsa synth 0.3 sine 1000')

def get_coords(landmarks, idx, use_z=False):
    """Get 2D or 3D coordinates of a landmark."""
    lm = landmarks[idx]
    return [lm.x, lm.y, lm.z] if use_z else [lm.x, lm.y]

def save_accuracy(accuracy, filename=CSV_OUTPUT):
    """Appends accuracy to a CSV file."""
    file_exists = os.path.exists(filename)
    is_empty = os.stat(filename).st_size == 0 if file_exists else True
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if is_empty:
            writer.writerow(["Accuracy (%)"])
        writer.writerow([round(accuracy, 2)])
def draw_text_with_bg(image, text, org, font, font_scale, text_color, bg_color, thickness, padding=10):
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = org
    top_left = (x - padding, y - text_h - padding)
    bottom_right = (x + text_w + padding, y + padding)

    # Overlay for transparency
    overlay = image.copy()
    cv2.rectangle(overlay, top_left, bottom_right, bg_color, -1)
    alpha = 0.6  # Transparency factor
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    # Text on top
    cv2.putText(image, text, (x, y), font, font_scale, text_color, thickness)
# === Main Function ===
def run_bicep_curl_tracker():
    left_counter = 0
    left_stage = None
    incorrect_reps = 0
    warning_text = ""
    warning_start_time = None
    warning_active = False

    cap = cv2.VideoCapture(CAM_INDEX)

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Preprocess
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # === 2D Coordinates ===
                l_shoulder = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER.value)
                l_elbow = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW.value)
                l_wrist = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_WRIST.value)

                # === Angle Vector and Prediction ===
                elbow_angle_simple = calculate_angle(l_shoulder, l_elbow, l_wrist)
                angle_vector = np.array([elbow_angle_simple]).reshape(1, -1)
                label = model.predict(angle_vector)[0]

                # === Rep Counting Logic ===
                if label == 0:
                    left_stage = "down"
                elif label == 1 and left_stage == "down":
                    left_stage = "up"
                    left_counter += 1

                # === Posture Error Detection ===
                l_hip_3d = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_HIP.value, use_z=True)
                l_shoulder_3d = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER.value, use_z=True)
                l_elbow_3d = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW.value, use_z=True)
                l_wrist_3d = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_WRIST.value, use_z=True)
                l_index_3d = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_INDEX.value, use_z=True)

                shoulder_angle = calculate_angle(l_hip_3d, l_shoulder_3d, l_elbow_3d)
                elbow_angle = calculate_angle(l_wrist_3d, l_elbow_3d, l_shoulder_3d)
                wrist_angle = calculate_angle(l_index_3d, l_wrist_3d, l_elbow_3d)

                # === Error Feedback ===
                warning_text = ""
                errors = False
                if shoulder_angle > 6:
                    warning_text = "Keep your shoulder stable!"
                    errors = True
                elif wrist_angle < 155:
                    warning_text = " Keep your wrist straight!"
                    errors = True

                # === Beep on Error ===
                if errors:
                    if warning_start_time is None:
                        warning_start_time = time.time()
                    elif time.time() - warning_start_time >= 0.5 and not warning_active:
                        warning_active = True
                        beep()
                        incorrect_reps += 1
                else:
                    warning_start_time = None
                    warning_active = False

                # === Display ===
                # Usage: Enhanced, spaced inline
                draw_text_with_bg(image, f'Left Reps: {left_counter}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), (0, 0, 0), 2)
                draw_text_with_bg(image, f'Incorrect Reps: {incorrect_reps}', (170, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), (0, 0, 0), 2)
                draw_text_with_bg(image, f'Posture: {label}', (385, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), (0, 0, 0), 2)

                if warning_text:
                    cv2.putText(image, warning_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # cv2.putText(image, f'Shoulder Angle: {int(shoulder_angle)}', (30, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                # cv2.putText(image, f'Elbow Angle: {int(elbow_angle)}', (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                # cv2.putText(image, f'Wrist Angle: {int(wrist_angle)}', (30, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                # Landmarks
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            except Exception:
                pass

            cv2.imshow('💪 Bicep Curl Tracker', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # === Final Accuracy ===
    total_reps = left_counter + incorrect_reps
    accuracy = (left_counter / total_reps) * 100 if total_reps > 0 else 0
    save_accuracy(accuracy)
    print(f"Accuracy: {accuracy:.2f}% | Data saved to {CSV_OUTPUT}")

    cap.release()
    cv2.destroyAllWindows()

# === Run ===
if __name__ == "__main__":
    run_bicep_curl_tracker()
