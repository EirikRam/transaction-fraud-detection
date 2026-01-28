
# AI-Powered Fraud Detection Dashboard

![AI-Powered Fraud Detection Dashboard](backend/assets/fraud-detection-dashboard.png)

*Real-time transaction monitoring dashboard with ML-driven fraud classification and SHAP-based explainability.*

## Transaction Fraud Detection System Architecture

![Transaction Fraud Detection System Architecture](https://github.com/user-attachments/assets/912fa15e-da2f-4584-b80a-030efe13d7df)


## Project Summary
This project is a **full-stack AI-powered fraud detection system** that simulates financial transactions in real time, detects fraudulent behavior using a custom-trained machine learning model, and explains the model’s decisions with SHAP interpretability. It serves as an end-to-end demonstration of real-world fraud detection — from data simulation, feature engineering, model training, MLOps best practices, to a user-friendly web dashboard.

## What It Does
- Simulates account transaction data on demand.
- Uses a trained XGBoost-based fraud detection model to classify each transaction as **Fraud** or **Safe**.
- Provides an **Explain** feature powered by SHAP values to show users the top factors behind each prediction.
- Visualizes key stats: total transactions, fraud count, and total spend.

This framework mirrors what financial institutions use to prevent fraudulent activity, protecting user funds and reducing risk.

---

## ⚙️ How It Works (Technical Overview)

1️⃣ **Data Simulation:**  
A Python backend generates realistic transaction data with user IDs, merchant IDs, device, location, time features, and spending patterns.

2️⃣ **Feature Engineering:**  
We engineered powerful fraud signals:
   - Rolling user averages.
   - High-value transaction flags.
   - Time-based patterns.
   - **Anomaly detection:** using Isolation Forest to score suspiciousness.

3️⃣ **Model Training:**  
Using the engineered features, we trained an **XGBoost decision tree ensemble**, fine-tuned thresholds for fraud classification, and validated it with metrics such as:
   - Accuracy
   - Precision
   - Recall
   - F1 Score

4️⃣ **Explainability:**  
SHAP (SHapley Additive exPlanations) interprets how each feature influences a prediction, enhancing transparency.

5️⃣ **Full-Stack Dashboard:**  
- **Backend:** FastAPI serves the ML predictions & SHAP explanations.
- **Frontend:** HTML, CSS & JavaScript render a dynamic table and handle user interactions like Explain pop-ups.

---

## 🧩 Project Breakdown

### ✅ **1️⃣ Data & Feature Engineering**
- Created a custom dataset simulating real spending behavior.
- Engineered multiple behavioral and temporal features.
- Applied anomaly detection for additional fraud signals.


### ✅ 3️⃣ Model Development & Tuning

- **Classifier:** XGBoost
- **Evaluation:** Precision, recall, F1.
- **Threshold tuning:** Tested 0.3 → 0.7.
- **Final:** 0.5

| Metric              | Value  |
| ------------------- | ------ |
| Precision (fraud)   | ~0.54  |
| Recall (fraud)      | ~0.28  |
| F1-Score (fraud)    | ~0.37  |
| Accuracy (overall)  | ~0.87  |

- Applied continuous improvement loop: adjusted features, thresholds, and hyperparameters.**

### ✅ **3️⃣ User Interface & Deployment**
- Developed a responsive frontend dashboard.
- Integrated real-time backend predictions.
- Implemented SHAP explanations to provide clear reasoning for each prediction.

---

## 📊 Example Explainability

![SHAP Popup.png](backend/assets/SHAP%20Popup.png)

Each **Explain** pop-up shows the top factors contributing to the fraud score for a transaction.  
**Positive values** push towards "Fraud"; **Negative values** push towards "Safe".

---

## 🔬 Techniques Used
- ✅ **Decision Trees (XGBoost)** for robust pattern recognition.
- ✅ **Anomaly Detection (Isolation Forest)** to capture outliers in spending.
- ✅ **Rolling statistical features** for user behavior trends.
- ✅ **Explainability (SHAP)** for transparent AI.

---

## 👨‍💻 Created By

**Eric Ramirez | AI/ML Engineer**

© 2024 Eric Ramirez. All rights reserved.

---

## 📂 File Structure

```
├── backend/
│   ├── main.py           # FastAPI backend routes
│   ├── model_loader.py   # ML model load & explain logic
│   ├── user_data_simulator.py  # Transaction simulator
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
├── models/               # Trained fraud detection models
├── data/                 # Simulated data
```

---

## ✅ MLOps Highlights
This project demonstrates core **MLOps principles**:
- Data versioning (simulated data pipelines)
- Feature store (engineered features reused in training & inference)
- Model versioning & threshold tuning
- Production-ready API with FastAPI
- Frontend for user transparency & trust

---

## 📌 How To Run
1. Clone the repo.
2. Train or load the prebuilt model.
3. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. Open the dashboard in your browser:
   ```
   http://127.0.0.1:8000
   ```
