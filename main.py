from flask import Flask
from kiteconnect import KiteConnect
import os
import pandas as pd

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")

ACCESS_TOKEN = "f3yAMI1PMBgORimWDAQS0ViEGk4WmT36"

kite = KiteConnect(api_key=API_KEY)

kite.set_access_token(ACCESS_TOKEN)

@app.route("/")
def home():

    # Get historical data
    data = kite.historical_data(
        instrument_token=265,
        from_date="2026-05-20",
        to_date="2026-05-21",
        interval="5minute"
    )

    df = pd.DataFrame(data)

    # EMA calculations
    df["EMA9"] = df["close"].ewm(span=9).mean()
    df["EMA21"] = df["close"].ewm(span=21).mean()

    latest = df.iloc[-1]

    signal = "NO SIGNAL"

    if latest["EMA9"] > latest["EMA21"]:
        signal = "BUY"

    elif latest["EMA9"] < latest["EMA21"]:
        signal = "SELL"

    return f"""
    Signal: {signal}<br><br>
    Price: {latest['close']}<br>
    EMA9: {latest['EMA9']}<br>
    EMA21: {latest['EMA21']}
    """
