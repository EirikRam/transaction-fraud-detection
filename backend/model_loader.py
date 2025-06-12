import pandas as pd
from src.model import predict_with_threshold, load_model
from src.model import preprocess_data
from src.features import (
    add_anomaly_score,
    add_user_avg_amount,
    add_is_high_amount_for_user
)

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

