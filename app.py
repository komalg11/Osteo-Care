from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
import os
import cv2
import tensorflow as tf
import numpy as np
from werkzeug.utils import secure_filename
from datetime import timedelta
import gdown 

app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")
app.permanent_session_lifetime = timedelta(days=7)

UPLOAD_FOLDER = "static/img/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# === MODEL SETUP ===
MODEL_PATH = "models/model_4_8200.h5"
QUESTIONNAIRE_MODEL_PATH = "models/questionnaire_model.h5"
os.makedirs("models", exist_ok=True)

# Download models from Google Drive if not present
if not os.path.exists(MODEL_PATH):
    gdown.download(id="1wTHYfDJAr4ClcOvv5u9XqHVlB9t3Woiv", output=MODEL_PATH, quiet=False)
if not os.path.exists(QUESTIONNAIRE_MODEL_PATH):
    gdown.download(id="1zUpR7GhFc3rl8Sr25N7gu87wV4kZqX6e", output=QUESTIONNAIRE_MODEL_PATH, quiet=False)

# Load models
model = tf.keras.models.load_model(MODEL_PATH)
questionnaire_model = tf.keras.models.load_model(QUESTIONNAIRE_MODEL_PATH)

# === Helpers ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Failed to read image. The file might be corrupted or invalid.")
    image = cv2.resize(image, (200, 200))
    image = image / 255.0
    image = np.expand_dims(image, axis=(0, -1))
    return image

# === Routes ===
@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/questionnaire_option')
def questionnaire_option():
    return render_template('option.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        answers = [
            1 if request.form.get(f'q{i}') == 'yes' else 0
            for i in range(1, 7)
        ]
        padded_input_data = answers + [0, 0]
        input_data = np.array(padded_input_data).reshape(1, 8).astype(np.float32)
        prediction = questionnaire_model.predict(input_data)

        risk_level = np.argmax(prediction) if prediction.ndim == 2 and prediction.shape[1] == 3 else 0
        risk_labels = ['Low Risk', 'Moderate Risk', 'High Risk']
        risk_level_label = risk_labels[risk_level]

        answers_display = ['Yes' if answer == 1 else 'No' for answer in answers]
        session.update({
            'risk_level': risk_level_label,
            'answers': answers_display,
            'name': request.form.get('name', 'Unknown'),
            'gender': request.form.get('gender', 'Not Specified'),
            'age': request.form.get('age', 'Not Specified')
        })

        return redirect(url_for('result'))

    return render_template('questionnaire.html')

@app.route('/result')
def result():
    risk_level = session.get('risk_level', 'Not Available')
    answers = session.get('answers', [])
    name = session.get('name', 'Unknown')
    gender = session.get('gender', 'Not Specified')
    age = session.get('age', 'Not Specified')

    return render_template('result.html', risk_level=risk_level, answers=answers, name=name, gender=gender, age=age)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                image = preprocess_image(file_path)
                prediction_result = model.predict(image)

                if prediction_result.size == 0:
                    return jsonify({'error': 'Empty prediction result'}), 500

                severity = int(np.argmax(prediction_result))
                classes = ['Normal', 'Low Risk', 'Moderate Risk', 'High Risk', 'Severe Risk']
                severity_label = classes[severity] if severity < len(classes) else "Unknown"

                return jsonify({
                    'kl_grade': severity,
                    'severity_label': severity_label
                })
            except Exception as e:
                print(f"Error during prediction: {e}")
                return jsonify({'error': 'Error occurred during prediction'}), 500
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))