from pydantic import BaseModel

class Transaction(BaseModel):
    user_id: str
    merchant_id: str
    device_id: str
    location: str
    amount: float
    hour: int
    day_of_week: int
    user_avg_amount: float
    is_amount_high_for_user: int
