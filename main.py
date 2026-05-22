from flask import Flask
from kiteconnect import KiteConnect
import os
import pandas as pd
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")

ACCESS_TOKEN = "nRKXTtc2ryCVxsUdwwIZf2DLGMoIiwjs"

kite = KiteConnect(api_key=API_KEY)

kite.set_access_token(ACCESS_TOKEN)

last_signal = None


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

    global last_signal

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
        from_date="2026-05-21",
        to_date="2026-05-22",
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

    # BUY
    if (
        previous["EMA9"] < previous["EMA21"]
        and latest["EMA9"] > latest["EMA21"]
        and latest["close"] > latest["VWAP"]
        and latest["close"] > latest["open"]
    ):
        signal = "BUY"

    # SELL
    elif (
        previous["EMA9"] > previous["EMA21"]
        and latest["EMA9"] < latest["EMA21"]
        and latest["close"] < latest["VWAP"]
        and latest["close"] < latest["open"]
    ):
        signal = "SELL"

    sensex_price = latest["close"]

    atm_strike = round(sensex_price / 100) * 100

    option_signal = ""

    stop_loss = 0

    target = 0

    if signal == "BUY":

        option_signal = f"{atm_strike} CE"

        stop_loss = previous["low"]

        risk = latest["close"] - stop_loss

        target = latest["close"] + (risk * 2)

    elif signal == "SELL":

        option_signal = f"{atm_strike} PE"

        stop_loss = previous["high"]

        risk = stop_loss - latest["close"]

        target = latest["close"] - (risk * 2)

    message = f"""
SENSEX {signal} SIGNAL

Option: {option_signal}

Spot Price: {latest['close']}

Stop Loss: {stop_loss}

Target: {target}

EMA9: {latest['EMA9']}
EMA21: {latest['EMA21']}

VWAP: {latest['VWAP']}
"""

    if signal != "NO SIGNAL" and signal != last_signal:

        send_telegram_message(message)

        last_signal = signal

    return f"""
    Signal: {signal}<br><br>

    Option: {option_signal}<br><br>

    Spot Price: {latest['close']}<br>

    Stop Loss: {stop_loss}<br>

    Target: {target}<br>

    EMA9: {latest['EMA9']}<br>

    EMA21: {latest['EMA21']}<br>

    VWAP: {latest['VWAP']}
    """


if __name__ == "__main__":
    app.run()
