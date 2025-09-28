from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/simulate")
async def simulate(
    ticker: str = Query(...),
    days: int = Query(30),
    paths: int = Query(5)
):
    # Download historical data
    data = yf.download(ticker, period="1y")['Close']
    
    # Flatten daily returns to 1D
    returns = data.pct_change().dropna().values.flatten()
    
    simulations = []

    for _ in range(paths):
        price = data.iloc[-1]
        path = []
        for _ in range(days):
            price *= (1 + np.random.choice(returns))
            path.append({ticker: float(price)})
        simulations.append(path)
    
    return {"ticker": ticker, "simulations": simulations}
