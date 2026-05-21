from flask import Flask
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

@app.route("/")
def home():
    login_url = kite.login_url()
    return f'<a href="{login_url}">Login to Zerodha</a>'
