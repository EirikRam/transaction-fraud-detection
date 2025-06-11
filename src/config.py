# Thresholds for fraud classification
FRAUD_THRESHOLD_BASELINE = 0.7
FRAUD_THRESHOLD_V2 = 0.5

# Model file paths
MODEL_BASELINE = '../models/fraud_xgb_baseline.pkl'
MODEL_V2 = '../models/fraud_xgb_v2_with_anomaly.pkl'

# Features used in training (ordered)
FEATURE_COLUMNS = [
    'user_id', 'merchant_id', 'device_id', 'location',
    'amount', 'hour', 'day_of_week',
    'user_avg_amount', 'is_amount_high_for_user',
    'anomaly_score'
]

FEATURE_COLUMNS_V3 = [
    'user_id', 'merchant_id', 'device_id', 'location',
    'amount', 'hour', 'day_of_week',
    'user_avg_amount', 'is_amount_high_for_user'
]


