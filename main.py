from flask import Flask
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

@app.route("/")
def home():

    api_key = os.getenv("KITE_API_KEY")

    kite = KiteConnect(api_key=api_key)

    login_url = kite.login_url()

    return f'<a href="{login_url}">Login to Zerodha</a>'
