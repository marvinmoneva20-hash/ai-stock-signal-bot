import yfinance as yf
import pandas as pd
import numpy as np

def get_signal(symbol):
    symbol = symbol.upper()
    print(f"\nFetching data for {symbol}...")

    try:
        # Download 3 months of daily data
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)
        if df.empty:
            print("❌ No data found. Try another symbol.")
            return

        # --- Calculate indicators ---
        df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
        df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = df["EMA12"] - df["EMA26"]
        df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()

        # RSI calculation
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        RS = gain / loss
        df["RSI"] = 100 - (100 / (1 + RS))

        last = df.iloc[-1]

        # --- Generate AI signal ---
        if last["RSI"] < 30 and last["MACD"] > last["Signal_Line"]:
            signal = "BUY"
        elif last["RSI"] > 70 and last["MACD"] < last["Signal_Line"]:
            signal = "SELL"
        else:
            signal = "HOLD"

        # --- Show results ---
        print("\n📊 AI STOCK SIGNAL RESULT")
        print(f"Symbol: {symbol}")
        print(f"Price: ${round(last['Close'], 2)}")
        print(f"RSI: {round(last['RSI'], 2)}")
        print(f"MACD: {round(last['MACD'], 4)} | Signal Line: {round(last['Signal_Line'], 4)}")

        if signal == "BUY":
            print("💚 Recommendation: BUY")
        elif signal == "SELL":
            print("❤️ Recommendation: SELL")
        else:
            print("⚪ Recommendation: HOLD")

    except Exception as e:
        print("⚠️ Error:", e)

# --- Main loop ---
if __name__ == "__main__":
    print("=== AI STOCK SIGNAL BOT ===")
    while True:
        sym = input("\nEnter Stock Symbol (e.g. AAPL, TSLA, MSFT or 'exit'): ").strip()
        if sym.lower() == "exit":
            break
        get_signal(sym)
