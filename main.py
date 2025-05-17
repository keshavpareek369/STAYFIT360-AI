import streamlit as st
import google.generativeai as genai
import subprocess  # To run external Python scripts
import time
import os
import platform
import csv
    
# Configure API Key
genai.configure(api_key="XXXXXXXXXXXXXXXX")  # Replace with your actual API key

def calculate_bmi(weight, height, units="metric"):
    if units == "metric":
        return weight / (height ** 2)
    elif units == "imperial":
        return 703 * weight / (height ** 2)
    else:
        raise ValueError("Invalid unit system. Use 'metric' or 'imperial'.")

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 25:
        return "normal weight"
    elif 25 <= bmi < 30:
        return "overweight"
    else:
        return "obese"
    

def generate_plan(weight, height, units, preferences, age, gender, activity_level, medical_conditions):
    bmi = calculate_bmi(weight, height, units)
    bmi_category = get_bmi_category(bmi)

    prompt = f"""
   Generate a structured 7-day meal and exercise plan for an individual with a BMI of {bmi:.2f} ({bmi_category}).
    
    - Dietary preferences: {preferences}.
    - Age: {age}, Gender: {gender}, Activity Level: {activity_level}.
    - Medical Conditions: {medical_conditions}.
    
    Include:    
    1. Three meals and two snacks per day with approximate calorie counts.
    2. An exercise routine per day (Squats, Bicep Curls).
    Format:
    
    **Day 1**  
    - **Meals:** [Breakfast, Snack, Lunch, Snack, Dinner]  
    - **Exercise:** [Squats, Bicep Curls,running,stretching]  
    """


# gemini-1.5-pro  (Old model)
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-001")
        response = model.generate_content(prompt)
        return f"### BMI: {bmi:.2f} ({bmi_category})\n\n" + response.text
    except Exception as e:
        return f"Error generating plan: {e}"

# Streamlit UI
st.title("Diet & Exercise Plan Generator 🥗💪")
st.write("Enter your details below to generate a personalized **7-day meal and exercise plan**.")

# User Inputs
units = st.radio("Select Units:", ["Metric (kg, m)", "Imperial (lbs, inches)"])
weight = st.number_input("Weight:", min_value=30.0, max_value=300.0, step=0.1)
height = st.number_input("Height:", min_value=1.0, max_value=2.5, step=0.01)
# preferences = st.text_input("Dietary Preferences (e.g., Vegetarian, Keto, Gluten-Free)")
preferences = st.selectbox("Dietary Preferences:", ["Select Preferences","Vegetarian", "Keto", "Gluten-Free","NON-Vegetarian"])


age = st.number_input("Age:", min_value=10, max_value=100, step=1)
gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
activity_level = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
medical_conditions = st.text_area("Medical Conditions (if any):")

if st.button("Generate Plan"):
    unit_system = "metric" if "Metric" in units else "imperial"
    plan = generate_plan(weight, height, unit_system, preferences, age, gender, activity_level, medical_conditions)
    st.markdown(plan)

st.subheader("Start Your Exercise Routine 🏋️‍♂️")

def run_exercise(script_name):
    try:
        subprocess.Popen(["python", script_name])
        st.success(f"{script_name} started successfully!")
    except Exception as e:
        st.error(f"Error starting {script_name}: {e}")

# col1= st.columns(2)

# with col1:
if st.button("Start Bicep Curl"):
    run_exercise("Bicep.py")

if st.button("Start Squats"):
    run_exercise("Squat.py")

# Additional functionality if needed
st.subheader("Additional Functions")
import Graph  # Ensure Graph.py is in the same directory
if st.button("Generate Graphs"):
    Graph.show_graphs()


# import streamlit as st
# import openai
# import subprocess  # To run external Python scripts
# import os

# import streamlit as st
# import openai
# import subprocess

# # Set your OpenAI API key here
# openai.api_key = "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"  # Replace with your real key

# def calculate_bmi(weight, height, units="metric"):
#     if units == "metric":
#         return weight / (height ** 2)
#     elif units == "imperial":
#         return 703 * weight / (height ** 2)
#     else:
#         raise ValueError("Invalid unit system. Use 'metric' or 'imperial'.")

# def get_bmi_category(bmi):
#     if bmi < 18.5:
#         return "underweight"
#     elif 18.5 <= bmi < 25:
#         return "normal weight"
#     elif 25 <= bmi < 30:
#         return "overweight"
#     else:
#         return "obese"

# def generate_plan(weight, height, units, preferences, age, gender, activity_level, medical_conditions):
#     bmi = calculate_bmi(weight, height, units)
#     bmi_category = get_bmi_category(bmi)

#     prompt = f"""
#     Generate a structured 7-day meal and exercise plan for an individual with a BMI of {bmi:.2f} ({bmi_category}).

#     - Dietary preferences: {preferences}
#     - Age: {age}, Gender: {gender}, Activity Level: {activity_level}
#     - Medical Conditions: {medical_conditions}

#     Include:
#     1. Three meals and two snacks per day with calorie counts.
#     2. An exercise routine per day (Push-ups, Squats, Bicep Curls, Tricep Pushdowns)

#     Format:

#     **Day 1**
#     - **Meals:** [Breakfast, Snack, Lunch, Snack, Dinner]
#     - **Exercise:** [Push-ups, Squats, Bicep Curls, Tricep Pushdowns]
#     """

#     try:
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",  # or "gpt-4" if you have access
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7
#         )
#         return f"### BMI: {bmi:.2f} ({bmi_category})\n\n" + response.choices[0].message.content
#     except Exception as e:
#         return f"Error generating plan: {e}"

# # Streamlit UI
# st.title("Diet & Exercise Plan Generator 🥗💪")
# units = st.radio("Select Units:", ["Metric (kg, m)", "Imperial (lbs, inches)"])
# weight = st.number_input("Weight:", min_value=30.0, max_value=300.0, step=0.1)
# height = st.number_input("Height:", min_value=1.0, max_value=2.5, step=0.01)
# preferences = st.selectbox("Dietary Preferences:", ["Select Preferences", "Vegetarian", "Keto", "Gluten-Free", "NON-Vegetarian"])
# age = st.number_input("Age:", min_value=10, max_value=100, step=1)
# gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
# activity_level = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
# medical_conditions = st.text_area("Medical Conditions (if any):")

# if st.button("Generate Plan"):
#     unit_system = "metric" if "Metric" in units else "imperial"
#     plan = generate_plan(weight, height, unit_system, preferences, age, gender, activity_level, medical_conditions)
#     st.markdown(plan)

# # Exercise script starter
# st.subheader("Start Your Exercise Routine 🏋️‍♂️")

# def run_exercise(script_name):
#     try:
#         subprocess.Popen(["python", script_name])
#         st.success(f"{script_name} started successfully!")
#     except Exception as e:
#         st.error(f"Error starting {script_name}: {e}")

# if st.button("Start Bicep Curl"):
#     run_exercise("Bicep.py")

# if st.button("Start Squats"):
#     run_exercise("Squat.py")

# st.subheader("Additional Functions")
# import Graph
# if st.button("Generate Graphs"):
#     Graph.show_graphs()

