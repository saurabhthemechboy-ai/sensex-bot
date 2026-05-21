from flask import Flask
from kiteconnect import KiteConnect
from datetime import datetime
import os
import pandas as pd
import requests

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")

ACCESS_TOKEN = "f3yAMI1PMBgORimWDAQS0ViEGk4WmT36"

kite = KiteConnect(api_key=API_KEY)

kite.set_access_token(ACCESS_TOKEN)


def send_telegram_message(message):

	token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

	url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
    	"chat_id": chat_id,
    	"text": message
    }

    requests.post(url, data=payload)

@app.route("/")
def home():

	current_time = datetime.now().time()

	market_start = datetime.strptime(
    "09:20",
    "%H:%M"
).time()

	market_end = datetime.strptime(
    "14:30",
    "%H:%M"
).time()

if (
    current_time < market_start
    or current_time > market_end
):
	return "Market Closed"
    	data = kite.historical_data(
        instrument_token=265,
        from_date="2026-05-20",
        to_date="2026-05-21",
        interval="5minute"
    )

    df = pd.DataFrame(data)
	df["EMA9"] = df["close"].ewm(span=9).mean()
    df["EMA21"] = df["close"].ewm(span=21).mean()
    df["cum_volume"] = df["volume"].cumsum()
    df["cum_vol_price"] = (
    (df["close"] * df["volume"]).cumsum()
	)
    df["VWAP"] = (
    df["cum_vol_price"] / df["cum_volume"]
	)	

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    signal = "NO SIGNAL"

    # BUY crossover
    if (
        previous["EMA9"] < previous["EMA21"]
        and latest["EMA9"] > latest["EMA21"]
        and latest["close"] > latest["VWAP"]
    ):
    signal = "BUY"
   
    # SELL crossover
    elif (
        previous["EMA9"] > previous["EMA21"]
        and latest["EMA9"] < latest["EMA21"]
        and latest["close"] < latest["VWAP"]
    ):
    signal = "SELL"
 
    message = f"""
	SENSEX {signal} SIGNAL

	Price: {latest['close']}
	EMA9: {latest['EMA9']}
	EMA21: {latest['EMA21']}
	"""

    if signal != "NO SIGNAL":
        send_telegram_message(message)

    	return f"""
    		Signal: {signal}<br><br>
    		Price: {latest['close']}<br>
    		EMA9: {latest['EMA9']}<br>
    		EMA21: {latest['EMA21']}
    	""" 
