import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


MODEL_PATH = Path(__file__).resolve().parent / "churn_model_pipeline.pkl"

@st.cache_resource
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()


st.set_page_config(page_title="Customer Churn Prediction", layout="centered")
st.title("📊 Telco Customer Churn Prediction")
st.write("Predict whether a telecom customer is likely to churn based on their details.")


st.header("🔧 Enter Customer Details")

col1, col2 = st.columns(2)

yes_no_cols = [
    'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies',
    'PaperlessBilling'
]

yes_no_inputs = {}

with col1:
    for col in yes_no_cols[:6]:
        yes_no_inputs[col] = st.selectbox(col, ["Yes", "No"])

with col2:
    for col in yes_no_cols[6:]:
        yes_no_inputs[col] = st.selectbox(col, ["Yes", "No"])

with col1:
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    payment_method = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )

with col1:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=70.0)

with col2:
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=1000.0)

if st.button("🔍 Predict Churn"):
    try:
    
        binary_mapped = {k: 1 if v == "Yes" else 0 for k, v in yes_no_inputs.items()}

        input_data = pd.DataFrame({
            'gender': [gender],
            'SeniorCitizen': [0],
            'Partner': [binary_mapped['Partner']],
            'Dependents': [binary_mapped['Dependents']],
            'tenure': [tenure],
            'PhoneService': [binary_mapped['PhoneService']],
            'MultipleLines': [binary_mapped['MultipleLines']],
            'InternetService': [internet_service],
            'OnlineSecurity': [binary_mapped['OnlineSecurity']],
            'OnlineBackup': [binary_mapped['OnlineBackup']],
            'DeviceProtection': [binary_mapped['DeviceProtection']],
            'TechSupport': [binary_mapped['TechSupport']],
            'StreamingTV': [binary_mapped['StreamingTV']],
            'StreamingMovies': [binary_mapped['StreamingMovies']],
            'Contract': [contract],
            'PaperlessBilling': [binary_mapped['PaperlessBilling']],
            'PaymentMethod': [payment_method],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges]
        })

        
        prediction = model.predict(input_data)
        pred_proba = model.predict_proba(input_data)[0][1]

        churn_label = (
            "❌ Customer will likely **CHURN**"
            if prediction[0] == 1
            else "✅ Customer will **NOT** churn"
        )

        st.subheader(churn_label)
        st.write(f"**Churn Probability:** {pred_proba:.2%}")

        with st.expander("📋 Input Data Preview"):
            st.dataframe(input_data)

    except Exception as e:
        st.error(f"Error during prediction: {e}")
