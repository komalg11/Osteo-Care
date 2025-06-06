# 🦴 Knee Osteoarthritis Risk Assessment System

🔗 **Live Deployment**: [https://osteo-care.onrender.com](https://osteo-care.onrender.com)

---

## 🎯 Aim

To develop an AI-based web application that can assess the severity of **knee osteoarthritis** either through **X-ray image classification** or a **clinical questionnaire**, offering accessible and early screening support.

---

## 🧭 Scope

- Two diagnostic modes:
  - **Image-Based Prediction**: Upload knee X-rays for KL grade classification.
  - **Questionnaire-Based Prediction**: Answer clinical questions to assess risk.
- Real-time and personalized results (Age, Gender, Risk Level).
- Multi-language interface (English & Hindi).
- Frontend integrated with backend for seamless UX.
- Model loading optimized via **Google Drive** integration.

---

## ⚙️ Tech Stack

| Layer       | Technologies Used                        |
|-------------|-------------------------------------------|
| Backend     | Python, Flask                            |
| Frontend    | HTML, CSS, Bootstrap, Jinja2             |
| AI Models   | TensorFlow, Keras                        |
| Image Proc. | OpenCV                                   |
| Deployment  | Render (Free Tier Hosting)               |
| Storage     | Google Drive (for large ML models)       |

---

## 🚀 Key Features

- 🔬 Deep learning model for KL grade prediction from grayscale X-rays.
- 🧠 ML-based risk classification via questionnaire (Low, Moderate, High).
- 🌐 Language switch: English ↔ Hindi.
- 🔐 Secure large-model handling using Google Drive at runtime.
- 📊 Instant feedback with informative severity labels.

---

## 🧪 How to Run Locally

> ⚠️ Make sure Python 3.7+ is installed on your machine.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Saee-Surve/osteo-care.git
   cd osteo-care
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Run the Flask App**:
   ```bash
   python app.py
5. **Open your browser and go to the local server**:
   http://127.0.0.1:5000

---

## 🌍 Deployment

This project is deployed for free using Render. To handle large ML models, they are not stored in the repo or Render server — instead, they are downloaded dynamically at runtime from Google Drive.

## 🔐 Security Notes

The SECRET_KEY used in Flask is required for managing sessions securely.
For production environments, store secrets in environment variables instead of hardcoding them.

---

## 📬 Contact

For any queries, please contact: saeesurve7@gmail.com
