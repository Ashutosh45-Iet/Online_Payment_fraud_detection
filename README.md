# 🔐 Online Payment Fraud Detection

A Machine Learning project that detects fraudulent online payment transactions in real time. This system helps financial institutions and payment platforms minimize financial loss and enhance security.

---

## 📝 Project Overview

The model analyzes transactional and behavioral features such as transaction type, amount, and account balance changes to determine whether a transaction is genuine or fraudulent.

Designed for banks, digital wallets, payment gateways, and cybersecurity platforms.

---

## 📂 Dataset

The model is trained on a real-world online payment transaction dataset.

- **Dataset Link:** https://www.kaggle.com/datasets/rupakroy/online-payments-fraud-detection-dataset
- **Size:** ~493 MB
- **Important Features**
  - type
  - amount
  - oldbalanceOrg
  - newbalanceOrg
  - oldbalanceDest
  - newbalanceDest
- **Target Column:** `isFraud`

---

## ⚙️ Key Features

- Machine learning-based fraud classification  
- Behavioral feature engineering  
- Imbalanced class handling with SMOTE / Class Weights  
- High recall and ROC-AUC focus for fraud detection  
- Real-time prediction using Streamlit  
- Modular and reusable pipeline  

---

## 🛠️ Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- SMOTE / Imbalanced-learn
- Jupyter Notebook
- Streamlit

---

## ✅ Model Evaluation

| Model                          | Accuracy | ROC-AUC | Key Observation |
|-------------------------------|:--------:|:------:|----------------|
| Logistic Regression           | 96.15%   | 97.23% | Good baseline model |
| Support Vector Machine (SVM)  | 96.70%   | 97.40% | Works well for high-dimensional data |
| Decision Tree Classifier      | 97.00%   | 97.55% | Simple and interpretable |
| Random Forest Classifier      | 97.43%   | 97.78% | Strong on non-linear data |
| XGBoost Classifier            | 97.89%   | 98.05% | Handles imbalance effectively |
| **Gradient Boosting Classifier** | **98.46%** ✅ | **98.62%** | Best performing model |
| Stacking Ensemble Model       | 90.00%   | 98.10% | Strong ROC-AUC score |

➡️ Gradient Boosting achieved the highest performance.

---

## 📊 Results & Insights

- Gradient Boosting achieved **98.46% accuracy**
- Stacking model showed strong ROC-AUC performance
- Transaction amount and balance differences are key fraud indicators
- Effective for real-time fraud detection in online payments 🚀

---

## ▶️ How to Run (PyCharm + Streamlit)

```bash
# Step 1: Clone the repository
git clone https://github.com/your-username/online-payment-fraud-detection.git
cd online-payment-fraud-detection

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the Streamlit App
streamlit run app.py


```
## ✍️ Author

**Ashutosh Yadav**  
B.Tech CSE (AI) | Institute of Engineering & Technology, Lucknow  

📧 [ashutosh.iet26.student@gmail.com](mailto:ashutosh.iet26.student@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/ashutosh-yadav-93b303263/)

