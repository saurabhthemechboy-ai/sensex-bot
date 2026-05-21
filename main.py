from flask import Flask
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")

ACCESS_TOKEN = "f3yAMI1PMBgORimWDAQS0ViEGk4WmT36"

kite = KiteConnect(api_key=API_KEY)

kite.set_access_token(ACCESS_TOKEN)

@app.route("/")
def home():

    data = kite.quote("BSE:SENSEX")

    last_price = data["BSE:SENSEX"]["last_price"]

    return f"Live Sensex Price: {last_price}"
