import pandas as pd
from src.model import train_model

if __name__ == "__main__":
    df = pd.read_csv('../../data/simulated_fraud_transactions_features.csv')
    train_model(df)


