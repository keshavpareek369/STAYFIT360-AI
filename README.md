# StaYFit-360AI

**StaYFit-360AI** is an AI-driven fitness assistant that delivers real-time exercise correction, performance tracking, and personalized diet and workout plans based on user-specific information like BMI, age, and activity level. This project is designed to help users maintain fitness and form, especially in environments where personal trainers or gyms may not be accessible.

---

## 🧠 Problem Statement

Many individuals struggle to stay fit due to:

- Irregular routines
- Frequent travel
- Lack of access to personal trainers
- Incorrect exercise form
- No progress tracking
- Unstructured diet plans

This leads to inconsistent habits and an unhealthy lifestyle.

---

## 🎯 Objectives

- Provide real-time feedback and form correction during exercises
- Track correct and incorrect repetitions to monitor progress
- Suggest personalized diet plans using BMI, age, and activity level
- Build a user-friendly interface to enhance engagement

---

## 📦 Dataset

- **Exercises:** Squats, Bicep Curls
- **Format:** Video
- **Size:** ~10 GB
- **Sources:** YouTube, Kaggle

---

## ⚙️ Methodology

### 1. Preprocessing
- Videos are labeled and converted to frames using OpenCV
- Frames converted from BGR to RGB

### 2. Feature Extraction
- Keypoint coordinates and joint angles extracted
- Data stored in CSV format for training

### 3. Model Training
- Tested multiple ML models:
  - Random Forest
  - Logistic Regression
  - Support Vector Machine (SVM)
  - K-Nearest Neighbors (KNN)

### 4. Implementation
- Real-time pose detection using OpenCV
- Visual feedback for form correction
- Rep counting and error display

### 5. Progress Visualization
- Plots progress based on:
  - Correct Reps
  - Incorrect Reps
  - Total Reps = Correct Reps + Incorrect Reps
  - Accuracy (%) = (Correct Reps / Total Reps) × 100


### 6. Interface
- BMI calculator using user info (weight, height, units)
- Suggests diet and workout plans based on user profile

### 7. Project Demonstration
## 📽️ Demo Video
Click the image below to watch the demo of StaYFit-360AI in action:

[![StaYFit-360AI Demo](https://github.com/keshavpareek369/STAYFIT360-AI/blob/main/Coverphoto.png?raw=true)](https://youtu.be/8Dbi2HU3nHA?si=m0GPUsMB1jUq7Ggl)


---

## 📊 Model Evaluation

Models were evaluated based on their accuracy in classifying exercise stages:
- **Squats:** Up / Down
- **Bicep Curls:** Curl / Straight

---

## 🖥️ Real-Time Feedback

Real-time feedback includes:
- User pose with overlay
- Repetition counter
- Error detection and correction suggestions
- Visual display of progress metrics

---

## 🚀 Future Enhancements

- Extend to more exercises (e.g., pushups, planks)
- Integrate wearable data for more accuracy
- Add voice feedback
- Mobile app version

---

## 📌 Technologies Used

- Python
- OpenCV
- MediaPipe
- scikit-learn
- Matplotlib / Seaborn (for visualization)

---

## 🙏 Acknowledgments

- YouTube and Kaggle for dataset videos
- OpenCV and MediaPipe for pose estimation
- scikit-learn for model development

---

## 📬 Contact

For suggestions, collaboration, or queries, feel free to open an issue or contact the contributors.

---

**Stay Fit, Stay Smart — StaYFit-360AI 💪**
