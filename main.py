from flask import Flask
from kiteconnect import KiteConnect
import os
import pandas as pd
import requests

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")

ACCESS_TOKEN = "f3yAMI1PMBgORimWDAQS0ViEGk4WmT36"

kite = KiteConnect(api_key=API_KEY)

kite.set_access_token(ACCESS_TOKEN)

# ADD TELEGRAM FUNCTION HERE
    if signal != "NO SIGNAL":
    send_telegram_message(message)

    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=payload)

# BELOW THIS
@app.route("/")
def home():

    data = kite.historical_data(
        instrument_token=265,
        from_date="2026-05-20",
        to_date="2026-05-21",
        interval="5minute"
    )

    df = pd.DataFrame(data)

    df["EMA9"] = df["close"].ewm(span=9).mean()
    df["EMA21"] = df["close"].ewm(span=21).mean()

latest = df.iloc[-1]
previous = df.iloc[-2]

signal = "NO SIGNAL"

# BUY crossover
if (
    previous["EMA9"] < previous["EMA21"]
    and latest["EMA9"] > latest["EMA21"]
):
    signal = "BUY"

# SELL crossover
elif (
    previous["EMA9"] > previous["EMA21"]
    and latest["EMA9"] < latest["EMA21"]
):
    signal = "SELL"
    
    message = f"""
SENSEX {signal} SIGNAL

Price: {latest['close']}
EMA9: {latest['EMA9']}
EMA21: {latest['EMA21']}
"""

    send_telegram_message(message)

    return f"""
    Signal: {signal}<br><br>
    Price: {latest['close']}<br>
    EMA9: {latest['EMA9']}<br>
    EMA21: {latest['EMA21']}
    """
