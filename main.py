from flask import Flask
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

kite = KiteConnect(
    api_key=os.getenv("KITE_API_KEY")
)

@app.route("/")
def home():
    return "Kite SDK Connected"
