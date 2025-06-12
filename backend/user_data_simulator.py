import random
import pandas as pd
from datetime import datetime, timedelta
from src.features import add_anomaly_score

USER_IDS = [f"user_{i}" for i in range(1, 6)]
MERCHANT_IDS = [f"merchant_{i}" for i in range(1, 6)]
DEVICE_IDS = [f"device_{i}" for i in range(1, 6)]
LOCATIONS = ["NY", "CA", "TX", "FL", "WA"]

def generate_transactions(n=25):
    now = datetime.now()
    data = []

    for _ in range(n):
        user_id = random.choice(USER_IDS)
        merchant_id = random.choice(MERCHANT_IDS)
        device_id = random.choice(DEVICE_IDS)
        location = random.choice(LOCATIONS)
        amount = round(random.uniform(5, 500), 2)
        timestamp = now - timedelta(minutes=random.randint(0, 10000))

        data.append({
            "user_id": user_id,
            "merchant_id": merchant_id,
            "device_id": device_id,
            "location": location,
            "amount": amount,
            "timestamp": timestamp.isoformat()
        })

    df = pd.DataFrame(data)

    # Feature engineering
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by=["user_id", "timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    df["user_avg_amount"] = (
        df.groupby("user_id")["amount"]
        .expanding()
        .mean()
        .shift()
        .reset_index(level=0, drop=True)
    )
    df["user_avg_amount"].fillna(df["amount"].mean(), inplace=True)

    def rolling_user_95th(group):
        return group["amount"].expanding().quantile(0.95).shift()

    df["amount_95th"] = (
        df.groupby("user_id", group_keys=False)
        .apply(rolling_user_95th)
        .reset_index(drop=True)
    )
    df["is_amount_high_for_user"] = (df["amount"] > df["amount_95th"]).astype(int)

    # Add anomaly score
    df = add_anomaly_score(df)

    return df
