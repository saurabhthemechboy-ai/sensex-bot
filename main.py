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

    profile = kite.profile()

    return (
        f"Connected Successfully<br><br>"
        f"User Name: {profile['user_name']}<br>"
        f"User ID: {profile['user_id']}"
    )
