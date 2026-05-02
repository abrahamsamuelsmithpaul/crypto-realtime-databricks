import websocket
import json
from datetime import datetime
import os

OUTPUT_PATH = "data/crypto_stream.json"

def ensure_path():
    os.makedirs("data", exist_ok=True)

def on_message(ws, message):
    print("Received message")
    data = json.loads(message)

    record = {
        "trade_id": data["t"],
        "symbol": data["s"],
        "price": float(data["p"]),
        "quantity": float(data["q"]),
        "event_time": datetime.fromtimestamp(data["T"]/1000).isoformat()
    }

    with open(OUTPUT_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    print("Connected successfully")

def start_stream():
    ensure_path()
    socket = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    print("Connecting to stream...")

    ws = websocket.WebSocketApp(
        socket,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    start_stream()