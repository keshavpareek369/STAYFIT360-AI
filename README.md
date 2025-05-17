# StaYFit-360AI 💪🧠

**StaYFit-360AI** is an AI-powered virtual fitness trainer that provides **real-time posture correction**, **rep counting**, **performance tracking**, and **personalized health recommendations** including **BMI-based diet and exercise plans**. Designed for individuals who work out at home or lack access to personal trainers, StaYFit-360AI bridges the gap between technology and fitness coaching.

---

## 🧠 Problem Statement

Despite increasing awareness around physical fitness, many people struggle with:

- Inconsistent routines due to work or travel
- Lack of access to trainers or fitness consultants
- Performing exercises with incorrect form, leading to injuries
- No tracking of progress over time
- Generic and ineffective diet plans

These challenges ultimately lead to stagnation and unhealthy lifestyles.

---

## 🎯 Objectives

- 🏋️‍♂️ Detect and correct user posture during key exercises in real time
- 📈 Track repetitions with correctness classification (correct/incorrect)
- 🧮 Calculate user BMI from provided parameters (height, weight, units)
- 🍎 Suggest personalized **diet** and **workout** plans
- 💡 Visualize progress using graphs and accuracy metrics
- 🧑‍💻 Build a user-friendly interface for smooth user interaction

---

## 📦 Dataset

- **Exercises Included:** Squats, Bicep Curls
- **Format:** Video files
- **Size:** ~10 GB
- **Sources:** YouTube, Kaggle
- **Structure:**
  - Labeled video clips per exercise type
  - Converted into frames for feature extraction

---

## ⚙️ Methodology

### 1. Preprocessing
- Videos labeled according to posture stages (e.g., Up/Down)
- Converted to frames using OpenCV
- Frames processed from BGR to RGB color format

### 2. Feature Extraction
- Pose landmarks extracted using **MediaPipe**
- Joint **angles** computed (e.g., shoulder-elbow-wrist)
- Features exported to CSV files for ML model training

### 3. Model Training
Trained and evaluated multiple classifiers to detect correct posture:
- ✅ Random Forest
- ✅ Logistic Regression
- ✅ Support Vector Machine (SVM)
- ✅ K-Nearest Neighbors (KNN)

### 4. Real-Time Implementation
- Pose detection with OpenCV + MediaPipe
- Instant feedback shown via overlay: pose status, rep count, posture errors

### 5. Progress Tracking
- Tracks:
  - `Correct Reps`
  - `Incorrect Reps`
  - `Total Reps = Correct Reps + Incorrect Reps`
  - `Accuracy (%) = (Correct Reps / Total Reps) × 100`
- Plots real-time graphs for progress monitoring

### 6. Intelligent Interface
- BMI calculator (based on weight, height, units)
- Personalized:
  - **Diet plans**
  - **Exercise routines**
- Parameters customizable per user

---

## 📽️ Demo Video

Click below to watch StaYFit-360AI in action:

[![StaYFit-360AI Demo](https://github.com/keshavpareek369/STAYFIT360-AI/blob/main/Coverphoto.png?raw=true)](https://youtu.be/8Dbi2HU3nHA?si=m0GPUsMB1jUq7Ggl)

---

## 📊 Model Evaluation

Machine learning models were tested using accuracy and classification metrics on posture labels:
- **Squat Postures:** Up, Down
- **Bicep Curl Postures:** Curl, Straight

---

## 🖥️ Real-Time Feedback Features

- Live pose tracking and overlay display
- Correct/Incorrect rep classification on-screen
- Warnings for improper form (e.g., incomplete curl, unstable knee)
- Repetition counter and accuracy monitor

---

## 🚀 Future Enhancements

- 🧠 Deep learning-based model for higher accuracy
- 🤝 Multi-exercise support: pushups, lunges, planks
- 🎧 Voice-based real-time guidance and corrections
- 📱 Android/iOS mobile app version with camera access
- 📊 Cloud-based user progress tracking and history

---

## 📌 Technologies Used

| Technology       | Purpose                          |
|------------------|----------------------------------|
| Python           | Core programming language        |
| OpenCV           | Frame extraction and visualization |
| MediaPipe        | Real-time pose estimation        |
| scikit-learn     | ML model training and evaluation |
| Pandas/NumPy     | Data preprocessing and analysis  |
| Matplotlib/Seaborn | Progress visualization         |
| CSV/JSON         | Data storage format              |

---

## 🙏 Acknowledgments

- **YouTube & Kaggle:** Data sources for exercise samples
- **OpenCV & MediaPipe:** Real-time pose estimation and visualization tools
- **scikit-learn:** Machine learning model development
- Community developers and researchers for fitness tracking insights

---

## 📬 Contact

Have suggestions, issues, or want to collaborate?

👉 Open an issue or contact [Keshav Pareek](https://github.com/keshavpareek369) directly on GitHub.

---

**Stay Fit, Stay Smart — StaYFit-360AI 💪**

---
