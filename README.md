# Liver Disease Prediction System

🏥 Liver Disease Predictor powered by Logistic Regression.

## Overview
This is a Streamlit web application that predicts whether a patient has liver disease based on their medical history and blood test results. It uses a Logistic Regression model trained on the Indian Liver Patient Dataset.

## Features
- **Interactive UI:** A premium-looking dashboard to input patient metrics.
- **Real-time Prediction:** Uses the trained ML model to output prediction results and probability confidence.
- **Model Peformance:** Displays model accuracy, confusion matrix, and a classification report dynamically. 

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd "LIVER DISEASE"
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Files
- `app.py`: Streamlit main application script and ML prediction flow.
- `model.PY`: Script for Data visualization and EDA (Exploratory Data Analysis).
- `updated_indian_liver_patient_final.csv`: The dataset used to train the model.
- `requirements.txt`: Python package dependencies.
