import streamlit as st
import mysql.connector
import tensorflow as tf
import numpy as np
import cv2
import os
from werkzeug.security import generate_password_hash, check_password_hash

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'osteo'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Load models
MODEL_PATH = "D:/osteo-care/finalfrontend/model/model_4_8200.h5"
QUESTIONNAIRE_MODEL_PATH = "D:/osteo-care/finalfrontend/model/questionnaire_model.h5"

model = tf.keras.models.load_model(MODEL_PATH)
questionnaire_model = tf.keras.models.load_model(QUESTIONNAIRE_MODEL_PATH)

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (200, 200))
    image = image / 255.0
    image = np.expand_dims(image, axis=(0, -1))
    return image

# Streamlit App
st.title("Osteo Care - Knee Osteoarthritis Prediction")

menu = ["Home", "Sign Up", "Login", "Questionnaire", "Upload X-ray", "About Us"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("Welcome to Osteo Care")
    st.write("An AI-based platform for knee osteoarthritis prediction and risk assessment.")

elif choice == "Sign Up":
    st.subheader("User Registration")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        hashed_password = generate_password_hash(password)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
                           (full_name, email, hashed_password))
            connection.commit()
            st.success("Registration successful! Please log in.")
        except mysql.connector.IntegrityError:
            st.error("Email is already registered.")
        finally:
            cursor.close()
            connection.close()

elif choice == "Login":
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            st.success(f"Welcome {user['full_name']}!")
        else:
            st.error("Invalid email or password.")
        cursor.close()
        connection.close()

elif choice == "Questionnaire":
    st.subheader("Knee Osteoarthritis Risk Assessment")
    questions = [
        "Do you feel knee pain often?",
        "Do you experience stiffness in the knee?",
        "Do you have difficulty climbing stairs?",
        "Do you have swelling around your knee?",
        "Do you experience knee buckling?",
        "Are you above 50 years of age?"
    ]
    responses = [1 if st.radio(q, ("Yes", "No")) == "Yes" else 0 for q in questions]
    
    if st.button("Submit"):
        input_data = np.array(responses + [0, 0]).reshape(1, 8).astype(np.float32)
        prediction = questionnaire_model.predict(input_data)
        risk_level = np.argmax(prediction)
        risk_labels = ['Low Risk', 'Moderate Risk', 'High Risk']
        st.success(f"Risk Level: {risk_labels[risk_level]}")

elif choice == "Upload X-ray":
    st.subheader("Upload Knee X-ray for OA Severity Prediction")
    uploaded_file = st.file_uploader("Choose an X-ray image...", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        severity = np.argmax(prediction)
        classes = ['Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe']
        st.success(f"Predicted Severity: {classes[severity]}")

elif choice == "About Us":
    st.subheader("About Osteo Care")
    st.write("This platform provides AI-based assessment for knee osteoarthritis risk and severity based on X-ray images and questionnaires.")
