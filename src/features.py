import pandas as pd
from sklearn.ensemble import IsolationForest

def add_user_avg_amount(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(['user_id', 'timestamp'])
    df['user_avg_amount'] = (
        df.groupby('user_id')['amount']
        .expanding()
        .mean()
        .shift()
        .reset_index(level=0, drop=True)
    )
    return df

def add_is_high_amount_for_user(df: pd.DataFrame) -> pd.DataFrame:
    def rolling_user_95th(group):
        return group['amount'].expanding().quantile(0.95).shift()

    df['amount_95th'] = (
        df.groupby('user_id', group_keys=False)
        .apply(rolling_user_95th)
        .reset_index(drop=True)
    )
    df['is_amount_high_for_user'] = (df['amount'] > df['amount_95th']).astype(int)
    return df

def add_anomaly_score(df, contamination=0.02):
    iso = IsolationForest(contamination=contamination, random_state=42)
    df['anomaly_score'] = iso.fit_predict(df[['amount', 'user_avg_amount']])
    df['anomaly_score'] = (df['anomaly_score'] == -1).astype(int)
    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/simulated_fraud_transactions.csv')

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['user_id', 'timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    df['user_avg_amount'] = (
        df.groupby('user_id')['amount']
        .expanding()
        .mean()
        .shift()
        .reset_index(level=0, drop=True)
    )


    def rolling_user_95th(group):
        return group['amount'].expanding().quantile(0.95).shift()


    df['amount_95th'] = (
        df.groupby('user_id', group_keys=False)
        .apply(rolling_user_95th)
        .reset_index(drop=True)
    )

    df['is_amount_high_for_user'] = (df['amount'] > df['amount_95th']).astype(int)

    df = add_anomaly_score(df)

    df.to_csv('../data/simulated_fraud_transactions_features.csv', index=False)
    print("✅ Features created and saved.")
