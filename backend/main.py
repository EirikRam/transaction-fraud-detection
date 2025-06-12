import pandas as pd
from fastapi import FastAPI
from backend.model_loader import predict_transaction_batch
from backend.user_data_simulator import generate_transactions
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Serve static frontend assets
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve frontend page at root
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))

# Simulate transactions for UI
@app.get("/simulate")
def simulate_transactions(n: int = 25):
    df = generate_transactions(n)
    predictions = predict_transaction_batch(df)

    # Convert to serializable types
    for row in predictions:
        row["timestamp"] = str(row["timestamp"])  # convert datetime to string
        for key in row:
            if pd.isna(row[key]):
                row[key] = None  # Replace NaN with None for JSON serialization

    return JSONResponse(content=predictions)
