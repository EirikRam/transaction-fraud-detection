import pandas as pd
import numpy as np
from faker import Faker
import uuid
import random
from datetime import datetime, timedelta

class FraudDataSimulator:
    def __init__(self, num_users=1000, num_merchants=500, num_transactions=100_000, fraud_ratio=0.03):
        self.num_users = num_users
        self.num_merchants = num_merchants
        self.num_transactions = num_transactions
        self.fraud_ratio = fraud_ratio
        self.fake = Faker()
        self.start_date = datetime.now() - timedelta(days=180)
        np.random.seed(42)
        random.seed(42)

    def generate(self):
        user_ids = [f'user_{i}' for i in range(self.num_users)]
        merchant_ids = [f'merchant_{i}' for i in range(self.num_merchants)]
        user_devices = {user: [str(uuid.uuid4()) for _ in range(random.randint(1, 3))] for user in user_ids}
        user_locations = {user: self.fake.city() for user in user_ids}

        def generate_transaction(user_id):
            return {
                "transaction_id": str(uuid.uuid4()),
                "user_id": user_id,
                "merchant_id": random.choice(merchant_ids),
                "amount": round(np.random.exponential(scale=50), 2),
                "timestamp": self.start_date + timedelta(seconds=random.randint(0, 180 * 24 * 60 * 60)),
                "device_id": random.choice(user_devices[user_id]),
                "location": user_locations[user_id],
                "is_fraud": 0
            }

        base_data = [generate_transaction(random.choice(user_ids)) for _ in range(self.num_transactions)]
        df = pd.DataFrame(base_data)

        # Fraud: Geolocation mismatch
        fraud_geo = df.sample(frac=self.fraud_ratio/3).copy()
        fraud_geo['location'] = fraud_geo['location'].apply(lambda x: self.fake.city())
        fraud_geo['is_fraud'] = 1

        # Fraud: Amount outlier
        fraud_amount = df.sample(frac=self.fraud_ratio/3).copy()
        fraud_amount['amount'] *= 20
        fraud_amount['is_fraud'] = 1

        # Fraud: Rapid-fire
        fraud_rapid = []
        for _ in range(int((self.fraud_ratio/3) * self.num_transactions // 5)):
            user = random.choice(user_ids)
            base_time = self.start_date + timedelta(seconds=random.randint(0, 180 * 24 * 60 * 60))
            for _ in range(5):
                tx = generate_transaction(user)
                tx['timestamp'] = base_time
                tx['is_fraud'] = 1
                fraud_rapid.append(tx)

        # Fraud: Location-Device Mismatch (2% of transactions)
        num_mismatch = int(self.num_transactions * 0.02)
        fraud_mismatch = df.sample(n=num_mismatch).copy()

        # Replace location and device with new unseen values
        fraud_mismatch['location'] = fraud_mismatch['location'].apply(lambda x: self.fake.city())
        fraud_mismatch['device_id'] = fraud_mismatch['device_id'].apply(lambda x: str(uuid.uuid4()))
        fraud_mismatch['is_fraud'] = 1

        df = pd.concat([df, fraud_geo, fraud_amount, pd.DataFrame(fraud_rapid), fraud_mismatch], ignore_index=True)
        df = df.sample(frac=1).reset_index(drop=True)
        return df

    def save_to_csv(self, path='data/simulated_fraud_transactions.csv'):
        df = self.generate()
        df.to_csv(path, index=False)
        print(f"Saved {len(df)} transactions to {path}")
