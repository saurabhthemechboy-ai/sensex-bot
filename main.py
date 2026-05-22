from flask import Flask, request
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

@app.route("/")
def home():

    request_token = request.args.get("request_token")

    if request_token:

        data = kite.generate_session(
            request_token,
            api_secret=API_SECRET
        )

        access_token = data["access_token"]

        return f"ACCESS TOKEN:<br><br>{access_token}"

    return f'<a href="{kite.login_url()}">Login to Zerodha</a>'
