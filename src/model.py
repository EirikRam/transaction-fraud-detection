import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

from src.config import (
    MODEL_BASELINE, MODEL_V2,
    FRAUD_THRESHOLD_BASELINE, FRAUD_THRESHOLD_V2,
    FEATURE_COLUMNS_V3
)
from src.features import add_anomaly_score

def preprocess_data(df):
    # Label encode categorical columns
    for col in ['user_id', 'merchant_id', 'device_id', 'location']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    return df

def train_model(df, save_path=MODEL_V2):
    df = add_anomaly_score(df)
    df = preprocess_data(df)

    # Define X and y
    X = df[FEATURE_COLUMNS_V3 + ['anomaly_score']]
    y = df['is_fraud']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Train XGBoost
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")

    return model

def predict_with_threshold(model, df, threshold):
    df = add_anomaly_score(df)
    df = preprocess_data(df)
    X = df[FEATURE_COLUMNS_V3 + ['anomaly_score']]
    probs = model.predict_proba(X)[:, 1]
    return (probs > threshold).astype(int)

def load_model(version='v2'):
    if version == 'baseline':
        model = joblib.load(MODEL_BASELINE)
        threshold = FRAUD_THRESHOLD_BASELINE
    else:
        model = joblib.load(MODEL_V2)
        threshold = FRAUD_THRESHOLD_V2
    return model, threshold

if __name__ == "__main__":
    df = pd.read_csv('../data/simulated_fraud_transactions_features.csv')
    train_model(df)
