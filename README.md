# 🦴 Knee Osteoarthritis Risk Assessment System

🔗 **Live Deployment**: [https://osteo-care.onrender.com](https://osteo-care-qctw.onrender.com))

---

## 🌟 About the Project

**OsteoCare** is an AI-driven web application designed to assist in the early detection and severity assessment of **knee osteoarthritis**. The platform supports two diagnostic modes:

* **X-ray Image Classification** for Kellgren-Lawrence (KL) grading
* **Clinical Questionnaire** for risk assessment

This dual-mode system ensures that individuals without access to radiological imaging can still get personalized insights via a simple form.

---

## 🌟 Aim

To build an accessible and intelligent osteoarthritis screening system that can:

* Detect and classify OA severity from X-ray images.
* Offer clinical risk assessment without imaging.
* Provide instant feedback to assist early intervention.

---

## 🗺️ Scope

* Dual diagnostic approach: Image + Questionnaire
* Bilingual interface (English/Hindi)
* Real-time predictions
* Personalized user experience
* Google Drive model integration for efficient deployment

---

## ⚙️ Tech Stack

| Layer       | Technologies Used                  |
| ----------- | ---------------------------------- |
| Backend     | Python, Flask                      |
| Frontend    | HTML, CSS, Bootstrap, Jinja2       |
| AI Models   | TensorFlow, Keras                  |
| Image Proc. | OpenCV                             |
| Deployment  | Render (Free Tier Hosting)         |
| Storage     | Google Drive (for large ML models) |

---

## 🚀 Key Features

* 🔬 Deep learning model for grayscale knee X-ray KL grading
* 🧠 ML questionnaire model for risk prediction (Low/Moderate/High)
* 🌐 Language toggle: English ↔ Hindi
* 🔐 Secure dynamic model loading via Google Drive
* 📊 User-friendly results with severity explanation

---

## 🧪 How to Run Locally

> ⚠️ Python 3.7+ required

### 1. Clone the Repository

```bash
git clone https://github.com/komalg11/osteo-care.git
cd osteo-care
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask App

```bash
python app.py
```

### 5. Open in Browser

```
http://127.0.0.1:5000
```

---

## 🌍 Deployment Notes

* Hosted on **Render** (Free Tier)
* Models are not bundled in the repo due to large size
* **Google Drive** is used for on-the-fly model loading

---

## 🔒 Security Best Practices

* Use `.env` to store your `SECRET_KEY` and sensitive info
* Never hardcode secrets in source files (e.g., `app.py`)

---

## 📩 Contact

For feedback, suggestions, or collaboration:
**[komalgupta1157@gmail.com](mailto:komalgupta1157@gmail.com)**
