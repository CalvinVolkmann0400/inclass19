import os

import yfinance as yf
from supabase import create_client
from datetime import datetime, timedelta

# The secret key from .env (loaded with uv run --env-file .env)
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SECRET_KEY"])

def ingest_stock_data(symbol: str):
    # 1. Setup Dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # 2. Fetch from yfinance
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)

    if not df.empty:
        initial_p = float(df['Close'].iloc[0])
        final_p = float(df['Close'].iloc[-1])

        # 3. TASK: Save to Supabase table 'stock_records'
        # Do NOT calculate the signal here. Just save the raw prices.
        data = {
            "ticker": symbol.upper(),
            "initial_price": initial_p,
            "final_price": final_p
        }
        supabase.table("stock_records").insert(data).execute()
        print(f"Successfully ingested {symbol}")

# Run it for a few stocks
ingest_stock_data("AAPL")
ingest_stock_data("TSLA")
ingest_stock_data("MSFT")
ingest_stock_data("NVDA")
ingest_stock_data("AMZN")
