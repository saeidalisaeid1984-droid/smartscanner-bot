import os
import asyncio
import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8319981273:AAFxxGWig3lHrVgi6FnK8hPkq3ume8HghSA")
CHAT_ID = os.getenv("5837332461")

DEX_API = "https://api.dexscreener.com/latest/dex/pairs/bsc"
SCAN_INTERVAL = 300

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sent_pairs = set()

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def fetch_pairs():
    try:
        r = requests.get(DEX_API, timeout=15)
        return r.json().get("pairs", [])
    except Exception as e:
        logger.error(e)
        return []

def good(p):
    try:
        return (
            float(p["liquidity"]["usd"]) >= 15000 and
            float(p["volume"]["m5"]) >= 8000 and
            float(p["priceChange"]["m5"]) >= 3
        )
    except:
        return False

def msg(p):
    return f"""
🚨 Signal

🪙 {p['baseToken']['symbol']}
💧 Liquidity: ${p['liquidity']['usd']}
📊 Vol 5m: ${p['volume']['m5']}
📈 +{p['priceChange']['m5']}%

🕒 {now()}
"""

async def scanner(app):
    while True:
        pairs = fetch_pairs()
        for p in pairs:
            pid = p.get("pairAddress")
            if not pid or pid in sent_pairs:
                continue
            if good(p):
                await app.bot.send_message(
                    chat_id=CHAT_ID,
                    text=msg(p)
                )
                sent_pairs.add(pid)

        await asyncio.sleep(SCAN_INTERVAL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 SmartScanner شغّال")

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_chat.id))

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_cmd))

    asyncio.create_task(scanner(app))
    logger.info("Bot running stable mode")

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
