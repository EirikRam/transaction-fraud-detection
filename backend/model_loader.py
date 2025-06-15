import shap
import pandas as pd
from src.model import predict_with_threshold, load_model, preprocess_data
from src.features import (
    add_anomaly_score,
    add_user_avg_amount,
    add_is_high_amount_for_user
)

FEATURE_COLUMNS_V3 = ['user_id', 'merchant_id', 'device_id', 'location', 'amount', 'hour', 'day_of_week', 'user_avg_amount', 'is_amount_high_for_user', 'anomaly_score']

model, threshold = load_model()

def predict_transaction_batch(df: pd.DataFrame):
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Add time features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    # Add engineered features
    df = add_user_avg_amount(df)
    df = add_is_high_amount_for_user(df)
    df = add_anomaly_score(df)

    df = preprocess_data(df)
    preds = predict_with_threshold(model, df, threshold)
    df["is_fraud"] = preds
    return df.to_dict(orient="records")

def explain_transaction(df_row):
    df_row["timestamp"] = pd.to_datetime(df_row["timestamp"])
    df_row["hour"] = df_row["timestamp"].dt.hour
    df_row["day_of_week"] = df_row["timestamp"].dt.dayofweek
    df_row = add_user_avg_amount(df_row)
    df_row = add_is_high_amount_for_user(df_row)
    df_row = add_anomaly_score(df_row)
    df_row = preprocess_data(df_row)

    X = df_row[FEATURE_COLUMNS_V3]

    explainer = shap.Explainer(model)
    shap_values = explainer(X)

    return shap_values