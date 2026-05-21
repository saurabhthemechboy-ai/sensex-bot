from flask import Flask, request
import requests
app = Flask(__name__)
BOT_TOKEN = "8213688201:AAFJVt9dLyAUPfnh_eWetpMmzbaS_Nb4tk"
CHAT_ID = "-1003932123947"
@app.route('/')
def home():
  return "Bot is running"
@app.route('/webhook', methods=['POST'])
def webhook():
  data = request.json
  symbol = data.get("symbol", "SENSEX")
  signal = data.get("signal", "BUY")
  price = data.get("price", "0")
  message = f"""
  📊 Sensex Alert
  📈 Symbol: {symbol}
  🚀 Signal: {signal}
  💰 Price: {price} """
  telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {
    "chat_id": CHAT_ID,
    "text": message }
  requests.post(telegram_url, json=payload)
  return {"status": "success"}
