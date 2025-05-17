import cv2
import mediapipe as mp
import numpy as np
import joblib
import time
import pandas as pd
import os
import csv
import platform
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def run_squat_tracker():
    model = joblib.load("D:/Minor Project-2/svm_model.pkl")
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    prev_label = None
    reps_correct = 0
    reps_incorrect = 0
    min_knee_angle = 180
    counting_active = False

    error_messages = []
    warning_start_time = None
    warning_active = False

    feedback_message = ""
    feedback_time = 0
    FEEDBACK_DURATION = 1.5

    TOO_LOW_THRESHOLD = 50
    HIP_ANGLE_THRESHOLD = 60
    ANKLE_ANGLE_THRESHOLD = 115
    BAD_HOLD_DURATION = 0.3

    reps_data = []

    def beep():
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 300)
        else:
            try:
                os.system('play -nq -t alsa synth 0.3 sine 1000')
            except:
                os.system('afplay /System/Library/Sounds/Ping.aiff')

    def calculate_angle(a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180 else angle

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        error_messages = []

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            def coord(i): return [lm[i].x, lm[i].y]

            LK, LH, LA = 25, 23, 27
            RK, RH, RA = 26, 24, 28
            LF, RF = 31, 32

            l_knee = calculate_angle(coord(LH), coord(LK), coord(LA))
            r_knee = calculate_angle(coord(RH), coord(RK), coord(RA))
            l_hip = calculate_angle(coord(LK), coord(LH), [coord(LH)[0], coord(LH)[1] - 1])
            r_hip = calculate_angle(coord(RK), coord(RH), [coord(RH)[0], coord(RH)[1] - 1])
            l_ankle = calculate_angle(coord(LK), coord(LA), coord(LF))
            r_ankle = calculate_angle(coord(RK), coord(RA), coord(RF))

            avg_knee = (l_knee + r_knee) / 2
            avg_hip = (l_hip + r_hip) / 2
            avg_ankle = (l_ankle + r_ankle) / 2
            knee_sym = abs(l_knee - r_knee)
            hip_sym = abs(l_hip - r_hip)

            input_features = np.array([[l_knee, l_hip, l_ankle,
                                        r_knee, r_hip, r_ankle,
                                        avg_knee, avg_hip, knee_sym, hip_sym]])
            label = model.predict(input_features)[0]

            if label == "down":
                counting_active = True
                min_knee_angle = min(min_knee_angle, avg_knee)

                if min_knee_angle < TOO_LOW_THRESHOLD:
                    error_messages.append("Squat too low!")
                if avg_hip < HIP_ANGLE_THRESHOLD:
                    error_messages.append("Leaning forward too much!")
                if l_ankle < ANKLE_ANGLE_THRESHOLD or r_ankle < ANKLE_ANGLE_THRESHOLD:
                    error_messages.append("Ankle too bent!")

                if error_messages:
                    if warning_start_time is None:
                        warning_start_time = time.time()
                    elif time.time() - warning_start_time >= BAD_HOLD_DURATION:
                        if not warning_active:
                            warning_active = True
                            # reps_incorrect += 1
                            beep()
                else:
                    warning_start_time = None
                    warning_active = False

            if prev_label == "down" and label == "up" and counting_active:
                if  warning_active:   #min_knee_angle > 160 or
                    reps_incorrect += 1
                else:
                    reps_correct += 1
                    feedback_message = "Good Job!"
                    feedback_time = time.time()

                min_knee_angle = 180
                counting_active = False
                warning_start_time = None
                warning_active = False

            prev_label = label

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.putText(frame, f'Label: {label}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(frame, f'Correct Reps: {reps_correct}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(frame, f'Incorrect Reps: {reps_incorrect}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            y_offset = 200
            for msg in error_messages:
                cv2.putText(frame, f"Error: {msg}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                y_offset += 30

            if feedback_message and time.time() - feedback_time <= FEEDBACK_DURATION:
                cv2.putText(frame, feedback_message, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            elif time.time() - feedback_time > FEEDBACK_DURATION:
                feedback_message = ""

        cv2.imshow("Squat Form Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    reps_data.append([reps_correct, reps_incorrect])
    df_reps = pd.DataFrame(reps_data, columns=["Correct Reps", "Incorrect Reps"])
    df_reps.to_csv("squats-reps.csv", index=False)

    total_reps = reps_correct + reps_incorrect
    accuracy = (reps_correct / total_reps) * 100 if total_reps > 0 else 0

    final_file = "squats-final.csv"
    file_exists = os.path.exists(final_file)
    is_empty = os.stat(final_file).st_size == 0 if file_exists else True

    with open(final_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if is_empty:
            writer.writerow(["Accuracy (%)"])
        writer.writerow([round(accuracy, 2)])

    print("Data saved successfully!")

run_squat_tracker()