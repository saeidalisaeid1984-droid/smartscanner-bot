import time
import requests
from datetime import datetime
import os

# ================= CONFIG =================
BOT_TOKEN = os.getenv("8319981273:AAFxxGWig3lHrVgi6FnK8hPkq3ume8HghSA")
CHAT_ID = os.getenv("5837332461")

DEX_URL = "https://api.dexscreener.com/latest/dex/search?q=BSC"

MIN_VOLUME = 400_000
MIN_CHANGE = 1.2
SLEEP_TIME = 60

sent_pairs = set()

# ============== TELEGRAM ==================
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# ============== START MESSAGE =============
send("🚀 SmartScannerLY NEW CORE is LIVE\n🔍 Scanning BSC markets...")

# ============== MAIN LOOP =================
while True:
    try:
        r = requests.get(DEX_URL, timeout=10)
        data = r.json().get("pairs", [])

        for p in data:
            pair = p.get("pairAddress")
            if not pair or pair in sent_pairs:
                continue

            vol = p.get("volume", {}).get("h24", 0)
            change = p.get("priceChange", {}).get("h24", 0)
            name = p.get("baseToken", {}).get("symbol", "UNKNOWN")

            if vol >= MIN_VOLUME and abs(change) >= MIN_CHANGE:
                msg = (
                    f"🔥 *Market Move Detected*\n"
                    f"🪙 {name}\n"
                    f"📊 24h Volume: {vol:,.0f}$\n"
                    f"📈 Change: {change}%\n"
                    f"⏰ {datetime.utcnow()} UTC"
                )
                send(msg)
                sent_pairs.add(pair)

        time.sleep(SLEEP_TIME)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
