import os
import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from apscheduler.schedulers.background import BackgroundScheduler

# ================= CONFIG =================
BOT_TOKEN = os.getenv("8319981273:AAFxxGWig3lHrVgi6FnK8hPkq3ume8HghSA")
CHAT_ID = os.getenv("5837332461")

DEX_API = "https://api.dexscreener.com/latest/dex/pairs/bsc"
SCAN_INTERVAL = 300  # كل 5 دقائق
MIN_LIQUIDITY = 15000
MIN_VOLUME_5M = 8000
MIN_PRICE_CHANGE_5M = 3  # %

# ================= LOGGING =================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= GLOBAL =================
last_sent_pairs = set()

# ================= HELPERS =================
def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def fetch_pairs():
    try:
        r = requests.get(DEX_API, timeout=15)
        return r.json().get("pairs", [])
    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return []

def is_good_pair(p):
    try:
        liquidity = float(p["liquidity"]["usd"])
        vol5m = float(p["volume"]["m5"])
        change5m = float(p["priceChange"]["m5"])

        if liquidity >= MIN_LIQUIDITY and vol5m >= MIN_VOLUME_5M and change5m >= MIN_PRICE_CHANGE_5M:
            return True
        return False
    except:
        return False

def format_alert(p):
    return f"""
🚨 *Aggressive Signal*

🪙 *{p['baseToken']['symbol']}*
💧 Liquidity: ${p['liquidity']['usd']:,}
📊 Vol 5m: ${p['volume']['m5']:,}
📈 Change 5m: {p['priceChange']['m5']}%
💲 Price: {p['priceUsd']}

🧠 Reason:
- Liquidity OK
- Volume Spike
- Price Moving

🕒 {now()}
"""

# ================= SCANNER =================
async def scan_market(app):
    pairs = fetch_pairs()
    sent_now = 0

    for p in pairs:
        pair_id = p.get("pairAddress")
        if not pair_id or pair_id in last_sent_pairs:
            continue

        if is_good_pair(p):
            try:
                await app.bot.send_message(
                    chat_id=CHAT_ID,
                    text=format_alert(p),
                    parse_mode="Markdown"
                )
                last_sent_pairs.add(pair_id)
                sent_now += 1
            except Exception as e:
                logger.error(e)

    if sent_now == 0:
        logger.info("No aggressive signals this round")

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 SmartScanner Bot شغّال\n"
        "/status الحالة\n"
        "/ping اختبار\n"
        "/time الوقت\n"
        "/id Chat ID\n"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"✅ شغّال\n⏱ آخر فحص: {now()}\n📡 Mode: Aggressive"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong")

async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(now())

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_chat.id))

# ================= MAIN =================
async def main():
    if not BOT_TOKEN or not CHAT_ID:
        raise Exception("BOT_TOKEN or CHAT_ID missing")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("time", time_cmd))
    app.add_handler(CommandHandler("id", id_cmd))

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: scan_market(app), "interval", seconds=SCAN_INTERVAL)
    scheduler.start()

    logger.info("Bot running in Aggressive Mode")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
