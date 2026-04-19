import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Liver Disease Predictor",
    page_icon="🏥",
    layout="wide",
)

# ──────────────────────────────────────────────
# Custom CSS for premium look
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #a5b4fc;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        padding: 1.5rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    .metric-card h3 {
        color: #c4b5fd;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    .metric-card p {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.4rem 0 0 0;
    }

    .result-positive {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        padding: 2rem;
        border-radius: 14px;
        text-align: center;
        border: 1px solid #dc2626;
        box-shadow: 0 4px 24px rgba(220, 38, 38, 0.2);
    }
    .result-positive h2 { color: #fca5a5; margin: 0; font-size: 1.6rem; }
    .result-positive p  { color: #fecaca; margin: 0.5rem 0 0 0; font-size: 1rem; }

    .result-negative {
        background: linear-gradient(135deg, #064e3b, #065f46);
        padding: 2rem;
        border-radius: 14px;
        text-align: center;
        border: 1px solid #10b981;
        box-shadow: 0 4px 24px rgba(16, 185, 129, 0.2);
    }
    .result-negative h2 { color: #6ee7b7; margin: 0; font-size: 1.6rem; }
    .result-negative p  { color: #a7f3d0; margin: 0.5rem 0 0 0; font-size: 1rem; }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29, #1e1b4b);
    }
    div[data-testid="stSidebar"] label {
        color: #c4b5fd !important;
        font-weight: 500;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Load and train model (cached)
# ──────────────────────────────────────────────
@st.cache_resource
def load_and_train():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "updated_indian_liver_patient_final.csv")
    df = pd.read_csv(csv_path)

    # Encode Gender: In this CSV, 2=Male → 1, 3=Female → 0
    df["Gender"] = df["Gender"].map({2: 1, 3: 0})

    # Target: 1 → liver disease (positive), 2 → no disease (negative)
    # Convert to binary: 1 = disease, 0 = no disease
    df["Dataset"] = df["Dataset"].apply(lambda x: 1 if x == 1 else 0)

    # Drop any rows with NaN after all transformations
    df = df.dropna()

    feature_cols = [
        "Age", "Gender",
        "Total_Bilirubin", "Direct_Bilirubin",
        "Alkaline_Phosphotase",
        "Alamine_Aminotransferase", "Aspartate_Aminotransferase",
        "Total_Protiens", "Albumin",
        "Albumin_and_Globulin_Ratio",
    ]

    X = df[feature_cols]
    y = df["Dataset"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["No Disease", "Liver Disease"])
    cm = confusion_matrix(y_test, y_pred)

    return model, scaler, feature_cols, acc, report, cm, df


model, scaler, feature_cols, accuracy, report, cm, df = load_and_train()

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏥 Liver Disease Prediction System</h1>
    <p>Powered by Logistic Regression &mdash; trained on Indian Liver Patient Dataset</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Model metrics row
# ──────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Accuracy</h3>
        <p>{accuracy * 100:.1f}%</p>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Training Samples</h3>
        <p>{int(len(df) * 0.8)}</p>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Test Samples</h3>
        <p>{int(len(df) * 0.2)}</p>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Features Used</h3>
        <p>{len(feature_cols)}</p>
    </div>""", unsafe_allow_html=True)

st.write("")

# ──────────────────────────────────────────────
# Sidebar – Patient input form
# ──────────────────────────────────────────────
st.sidebar.markdown("## 📋 Enter Patient Details")
st.sidebar.markdown("Fill in the blood‑test values below and click **Predict**.")

age = st.sidebar.slider("Age", 4, 90, 45)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
total_bilirubin = st.sidebar.number_input("Total Bilirubin", 0.0, 80.0, 1.0, 0.1)
direct_bilirubin = st.sidebar.number_input("Direct Bilirubin", 0.0, 20.0, 0.3, 0.1)
alkaline_phosphotase = st.sidebar.number_input("Alkaline Phosphotase", 50, 2200, 200, 10)
alamine_aminotransferase = st.sidebar.number_input("Alamine Aminotransferase (ALT)", 5, 2000, 25, 5)
aspartate_aminotransferase = st.sidebar.number_input("Aspartate Aminotransferase (AST)", 5, 5000, 30, 5)
total_protiens = st.sidebar.number_input("Total Proteins (g/dL)", 1.0, 10.0, 6.8, 0.1)
albumin = st.sidebar.number_input("Albumin (g/dL)", 0.5, 6.0, 3.5, 0.1)
ag_ratio = st.sidebar.number_input("Albumin / Globulin Ratio", 0.1, 3.0, 0.9, 0.05)

gender_enc = 1 if gender == "Male" else 0

predict_btn = st.sidebar.button("🔍  Predict")

# ──────────────────────────────────────────────
# Prediction
# ──────────────────────────────────────────────
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("### 🧪 Prediction Result")
    if predict_btn:
        input_data = np.array([[
            age, gender_enc,
            total_bilirubin, direct_bilirubin,
            alkaline_phosphotase,
            alamine_aminotransferase, aspartate_aminotransferase,
            total_protiens, albumin,
            ag_ratio,
        ]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]

        if prediction == 1:
            st.markdown(f"""
            <div class="result-positive">
                <h2>⚠️ Liver Disease Detected</h2>
                <p>Confidence: {probability[1] * 100:.1f}%</p>
                <p style="margin-top:1rem;font-size:0.85rem;color:#fecaca;">
                    The model predicts this patient <strong>may have liver disease</strong>.
                    Please consult a medical professional for further diagnosis.
                </p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-negative">
                <h2>✅ No Liver Disease Detected</h2>
                <p>Confidence: {probability[0] * 100:.1f}%</p>
                <p style="margin-top:1rem;font-size:0.85rem;color:#a7f3d0;">
                    The model predicts this patient <strong>does not have liver disease</strong>.
                    Continue regular health check‑ups.
                </p>
            </div>""", unsafe_allow_html=True)

        st.write("")
        st.markdown("#### 📊 Input Summary")
        input_df = pd.DataFrame({
            "Feature": [
                "Age", "Gender",
                "Total Bilirubin", "Direct Bilirubin",
                "Alkaline Phosphotase",
                "ALT", "AST",
                "Total Proteins", "Albumin",
                "A/G Ratio",
            ],
            "Value": [
                age, gender,
                total_bilirubin, direct_bilirubin,
                alkaline_phosphotase,
                alamine_aminotransferase, aspartate_aminotransferase,
                total_protiens, albumin,
                ag_ratio,
            ],
        })
        st.dataframe(input_df, use_container_width=True, hide_index=True)
    else:
        st.info("👈 Enter patient details in the sidebar and click **Predict**.")

with right_col:
    st.markdown("### 📈 Model Performance")

    st.markdown("**Confusion Matrix**")
    cm_df = pd.DataFrame(
        cm,
        index=["Actual: No Disease", "Actual: Liver Disease"],
        columns=["Pred: No Disease", "Pred: Liver Disease"],
    )
    st.dataframe(cm_df, use_container_width=True)

    st.markdown("**Classification Report**")
    st.code(report)

    st.markdown("### 📂 Dataset Overview")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
