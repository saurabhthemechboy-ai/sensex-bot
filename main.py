from flask import Flask
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = "PASTE_YOUR_ACCESS_TOKEN"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

@app.route("/")
def home():

    profile = kite.profile()

    return f"""
    Connected Successfully<br><br>
    User Name: {profile['user_name']}<br>
    User ID: {profile['user_id']}
    """login_url()}">Login to Zerodha</a>'
