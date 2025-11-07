# app_simple_pretty.py
import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.exceptions import NotFittedError

st.set_page_config(page_title="💳 Fraud Detector (Simple & Pretty)", layout="wide")

# ---------------------------
# Simple CSS for nicer look
st.markdown("""
<style>
body {background: linear-gradient(160deg,#f8fbff,#ffffff);}
.card {
  background: black;
  padding: 18px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(16,24,40,0.06);
}
.center {text-align:center}
.small {color:#6b7280; font-size:13px}
.big-number {font-size:40px; font-weight:700}
.stButton>button {background-color:#0b69ff; color:white; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Google Drive file ID
file_id = "1lOh_Ue0BT_jyU503HJ_Dmha31Y505tda"
url = f"https://drive.google.com/uc?id={file_id}"
model_path = "stacking_fraud_model.pkl"

# Download model if missing
if not os.path.exists(model_path):
    st.write("📥 Downloading trained model from Google Drive...")
    gdowsn.download(url, model_path, quiet=False)

# Load model
try:
  with open(model_path, "rb") as f:
      pipe = pickle.load(f)
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()
 # Try loading df.pkl for dropdowns (optional)
try:
  with open("df.pkl", "rb") as f:
      df = pickle.load(f)
except Exception:
    df = pd.DataFrame()
# ---------------------------
# Header
st.markdown("<div class='card center'><h1>💳 Online Payment Fraud Detector</h1>"
            "<div class='small'>Simple interface — enter transaction details and get a fraud score</div></div>",
            unsafe_allow_html=True)
st.write("")

# ---------------------------
# Layout: Inputs (left) | Result (right)
left, right = st.columns([2, 1])

with left:
    st.markdown("### 🧾 Transaction Details")
    # quick presets to speed up testing
    preset = st.selectbox("Choose a preset", ["Custom", "Typical Transfer", "Large CashOut", "Small Payment"])
    if preset == "Typical Transfer":
        step = st.number_input("Step", 1, 744, value=200)
        amount = st.number_input("Amount (₹)", 0.0, value=1500.0, step=100.0)
        oldbalanceOrg = st.number_input("Old Balance (Sender)", 0.0, value=5000.0, step=100.0)
        newbalanceOrig = st.number_input("New Balance (Sender)", 0.0, value=3500.0, step=100.0)
        oldbalanceDest = st.number_input("Old Balance (Receiver)", 0.0, value=2000.0, step=100.0)
        newbalanceDest = st.number_input("New Balance (Receiver)", 0.0, value=3500.0, step=100.0)
        tx_type = st.selectbox("Type", ["TRANSFER","CASH_OUT","DEBIT","PAYMENT"])
    elif preset == "Large CashOut":
        step = st.number_input("Step", 1, 744, value=600)
        amount = st.number_input("Amount (₹)", 0.0, value=250000.0, step=100.0)
        oldbalanceOrg = st.number_input("Old Balance (Sender)", 0.0, value=300000.0, step=100.0)
        newbalanceOrig = st.number_input("New Balance (Sender)", 0.0, value=50000.0, step=100.0)
        oldbalanceDest = st.number_input("Old Balance (Receiver)", 0.0, value=1000.0, step=100.0)
        newbalanceDest = st.number_input("New Balance (Receiver)", 0.0, value=101000.0, step=100.0)
        tx_type = st.selectbox("Type", ["CASH_OUT","TRANSFER","DEBIT","PAYMENT"])
    elif preset == "Small Payment":
        step = st.number_input("Step", 1, 744, value=50)
        amount = st.number_input("Amount (₹)", 0.0, value=200.0, step=10.0)
        oldbalanceOrg = st.number_input("Old Balance (Sender)", 0.0, value=1000.0, step=10.0)
        newbalanceOrig = st.number_input("New Balance (Sender)", 0.0, value=800.0, step=10.0)
        oldbalanceDest = st.number_input("Old Balance (Receiver)", 0.0, value=400.0, step=10.0)
        newbalanceDest = st.number_input("New Balance (Receiver)", 0.0, value=600.0, step=10.0)
        tx_type = st.selectbox("Type", ["PAYMENT","TRANSFER","DEBIT","CASH_OUT"])
    else:
        # custom
        step = st.number_input("Step", 1, 744, value=100)
        amount = st.number_input("Amount (₹)", 0.0, value=10000.0, step=100.0)
        oldbalanceOrg = st.number_input("Old Balance (Sender)", 0.0, value=20000.0, step=100.0)
        newbalanceOrig = st.number_input("New Balance (Sender)", 0.0, value=10000.0, step=100.0)
        oldbalanceDest = st.number_input("Old Balance (Receiver)", 0.0, value=5000.0, step=100.0)
        newbalanceDest = st.number_input("New Balance (Receiver)", 0.0, value=15000.0, step=100.0)
        tx_type = st.selectbox("Type", ["TRANSFER","CASH_OUT","DEBIT","PAYMENT","OTHER"])

    st.write("")  # spacing
    detect = st.button("🔍 Detect Fraud")

with right:
    st.markdown("<div class='card center'><div class='small'>Result</div>", unsafe_allow_html=True)
    # placeholders
    status_placeholder = st.empty()
    prob_placeholder = st.empty()
    bar_placeholder = st.empty()
    explain_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Feature encoding (same order)
cash_out_val = 1 if tx_type == "CASH_OUT" else 0
transfer_val = 1 if tx_type == "TRANSFER" else 0
debit_val = 1 if tx_type == "DEBIT" else 0

feature_cols = [
    'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
    'oldbalanceDest', 'newbalanceDest', 'CASH_OUT', 'TRANSFER', 'DEBIT'
]
features = pd.DataFrame([[
    step, amount, oldbalanceOrg, newbalanceOrig,
    oldbalanceDest, newbalanceDest, cash_out_val, transfer_val, debit_val
]], columns=feature_cols)

# ---------------------------
# Predict and show simple, pretty output
if detect:
    if pipe is None:
        status_placeholder.error("❌ Model not loaded. Put 'stacking_fraud_model.pkl' in the app folder.")
    else:
        try:
            pred = pipe.predict(features)[0]
            prob = pipe.predict_proba(features)[0][1]
            pct = int(round(prob * 100))

            # Status
            if pred == 1:
                status_placeholder.markdown("<h2 style='color:#b00020; text-align:center;'>⚠️ Suspicious Transaction</h2>", unsafe_allow_html=True)
            else:
                status_placeholder.markdown("<h2 style='color:#0a8a3f; text-align:center;'>✅ Transaction appears valid</h2>", unsafe_allow_html=True)

            # Big probability number
            prob_placeholder.markdown(f"<div class='center'><div class='big-number'>{pct}%</div>"
                                     f"<div class='small'>Probability of fraud</div></div>", unsafe_allow_html=True)

            # Progress bar with color (Streamlit progress is neutral; use emoji + bar)
            bar_fill = min(max(pct, 0), 100)
            bar_placeholder.progress(bar_fill)

            # quick explain (top features simple heuristic)
            top_feats = [
                ("Amount", f"₹{amount:,.2f}"),
                ("Sender balance change", f"₹{oldbalanceOrg - newbalanceOrig:,.2f}"),
                ("Receiver balance change", f"₹{newbalanceDest - oldbalanceDest:,.2f}"),
                ("Type", tx_type)
            ]
            explain_text = " | ".join([f"{k}: {v}" for k, v in top_feats])
            explain_placeholder.info(explain_text)

            # celebration for very safe
            if pct < 20 and pred == 0:
                st.balloons()
        except NotFittedError:
            status_placeholder.error("❌ Model not fitted properly. Retrain or check pickle.")
        except Exception as e:
            status_placeholder.error(f"❌ Error during prediction: {e}")

# ---------------------------
# Footer
st.write("---")
st.markdown("<div class='small center'>Developed by <b>Ashutosh Yadav</b> | IET Lucknow</div>", unsafe_allow_html=True)
