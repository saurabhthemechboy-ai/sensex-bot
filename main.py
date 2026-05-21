from flask import Flask
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")

kite = KiteConnect(api_key=API_KEY)

@app.route("/")
def home():
    return f'<a href="{kite.login_url()}">Login to Zerodha</a>'
