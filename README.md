# 🏥 Liver Disease Prediction System

Welcome to the Liver Disease Prediction System. This Streamlit web application predicts whether a patient has liver disease based on their medical history and blood test results, powered by a robust Logistic Regression model trained on the Indian Liver Patient Dataset.

---

## 1. Overview & Features

### 🌟 Features
* **Interactive UI:** A premium-looking dashboard to seamlessly input patient metrics.
* **Real-time Prediction:** Utilizes a trained Machine Learning model to output prediction results and probability confidence instantly.
* **Model Performance:** Dynamically displays model accuracy, a confusion matrix, and a detailed classification report.

---

## 2. Project Files

* `app.py`: The main Streamlit application script and ML prediction flow.
* `model.py`: Script dedicated to Data Visualization and EDA (Exploratory Data Analysis).
* `updated_indian_liver_patient_final.csv`: The core dataset utilized to train the model.
* `requirements.txt`: Python package dependencies necessary to run the project.

---

## 3. Getting Started

### Prerequisites
1. Python 3.8+
2. Git installed on your machine.

### Installation & Running Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/sunilrangappa903/Liver-Disease-Prediction.git
   cd Liver-Disease-Prediction
   ```

2. **Install the required dependencies:**
   *(It is recommended to use a virtual environment)*
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

Once running, the application will automatically open in your default web browser!
