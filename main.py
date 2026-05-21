from flask import Flask
from kiteconnect import KiteConnect

app = Flask(__name__)

@app.route("/")
def home():
    kite = KiteConnect(api_key="test")
    return "Kite SDK Working"
