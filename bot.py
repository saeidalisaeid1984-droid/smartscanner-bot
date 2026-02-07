import time
import logging
from datetime import datetime

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# =========================
# بيانات البوت (حطهم هنا)
# =========================
BOT_TOKEN = "8319981273:AAFxxGWig3lHrVgi6FnK8hPkq3ume8HghSA"
CHAT_ID = 5837332461  # بدون ""

# =========================
# لوق
# =========================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# أوامر
# =========================
def start(update, context):
    update.message.reply_text(
        "🤖 SmartScanner Bot شغال\n"
        "/status - الحالة\n"
        "/ping - اختبار\n"
        "/time - الوقت\n"
        "/id - Chat ID"
    )

def status(update, context):
    update.message.reply_text("✅ البوت يعمل بدون مشاكل")

def ping(update, context):
    update.message.reply_text("🏓 Pong")

def time_cmd(update, context):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    update.message.reply_text(f"🕒 {now}")

def show_id(update, context):
    update.message.reply_text(f"🆔 Chat ID: {update.message.chat_id}")

def echo(update, context):
    update.message.reply_text(update.message.text)

# =========================
# تشغيل
# =========================
def main():
    bot = telegram.Bot(token=BOT_TOKEN)

    # رسالة إجبارية عند التشغيل
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text="🚀 SmartScanner Bot اشتغل بنجاح على Railway"
        )
    except Exception as e:
        logging.error(f"Startup message failed: {e}")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("time", time_cmd))
    dp.add_handler(CommandHandler("id", show_id))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    logging.info("Bot running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
