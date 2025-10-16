import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model pipeline
MODEL_PATH = "/ml-model/churn_model_pipeline.pkl"

@st.cache_resource
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

st.title("📊 Telco Customer Churn Prediction")
st.write("This app predicts whether a customer is likely to churn based on their details.")

# ---------------------------
# Input Form
# ---------------------------

st.header("🔧 Enter Customer Details")

# Create two columns
col1, col2 = st.columns(2)

# Yes/No fields (binary features)
yes_no_cols = [
    'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies',
    'PaperlessBilling'
]

yes_no_inputs = {}

# Distribute yes/no fields across two columns
with col1:
    for col in yes_no_cols[:6]:
        yes_no_inputs[col] = st.selectbox(f"{col}", ["Yes", "No"])

with col2:
    for col in yes_no_cols[6:]:
        yes_no_inputs[col] = st.selectbox(f"{col}", ["Yes", "No"])

# Categorical features (non-binary) in two columns
with col1:
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    payment_method = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
    ])

# Numerical inputs in two columns
with col1:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=70.0)

with col2:
    total_charges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=1000.0)

# ---------------------------
# Prepare DataFrame for Prediction
# ---------------------------

if st.button("🔍 Predict Churn"):
    try:
        # Combine all inputs into a DataFrame
        input_data = {
            'gender': [gender],
            'SeniorCitizen': [0],  # default (optional field, not user-input)
            'Partner': [yes_no_inputs['Partner']],
            'Dependents': [yes_no_inputs['Dependents']],
            'tenure': [tenure],
            'PhoneService': [yes_no_inputs['PhoneService']],
            'MultipleLines': [yes_no_inputs['MultipleLines']],
            'InternetService': [internet_service],
            'OnlineSecurity': [yes_no_inputs['OnlineSecurity']],
            'OnlineBackup': [yes_no_inputs['OnlineBackup']],
            'DeviceProtection': [yes_no_inputs['DeviceProtection']],
            'TechSupport': [yes_no_inputs['TechSupport']],
            'StreamingTV': [yes_no_inputs['StreamingTV']],
            'StreamingMovies': [yes_no_inputs['StreamingMovies']],
            'Contract': [contract],
            'PaperlessBilling': [yes_no_inputs['PaperlessBilling']],
            'PaymentMethod': [payment_method],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges]
        }

        input_df = pd.DataFrame(input_data)

        # Map Yes/No to 1/0 (must match training)
        binary_yes_no = [
            'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
            'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling'
        ]
        for c in binary_yes_no:
            if c in input_df.columns:
                input_df[c] = input_df[c].map({'Yes': 1, 'No': 0})

        # Predict
        prediction = model.predict(input_df)
        pred_proba = model.predict_proba(input_df)[0][1]

        churn_label = "❌ Customer will likely CHURN" if prediction[0] == 1 else "✅ Customer will NOT churn"
        st.subheader(churn_label)
        st.write(f"**Churn Probability:** {pred_proba:.2%}")

        # Show data for reference
        with st.expander("See Input Data"):
            st.dataframe(input_df)

    except Exception as e:
        st.error(f"Error during prediction: {e}")