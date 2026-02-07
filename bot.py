import time
import logging
from datetime import datetime, timezone

from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===============================
# 🔐 ضع بياناتك هنا فقط
# ===============================

BOT_TOKEN = "8319981273:AAFxxGWig3lHrVgi6FnK8hPkq3ume8HghSA"
OWNER_ID = 5837332461  # ضع Chat ID متاعك (رقم فقط)

# ===============================
# ⚙️ إعداد اللوق
# ===============================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===============================
# 📌 أوامر البوت
# ===============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 SmartScanner Bot شغّال\n\n"
        "الأوامر:\n"
        "/status - حالة البوت\n"
        "/ping - اختبار فوري\n"
        "/time - وقت السيرفر\n"
        "/help - جميع الأوامر\n"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 جميع الأوامر المتاحة:\n\n"
        "/start - بدء البوت\n"
        "/status - حالة البوت\n"
        "/ping - اختبار سريع\n"
        "/time - وقت Railway\n"
        "/echo - يكرر آخر رسالة\n"
        "/id - يعرض Chat ID\n"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل بدون أخطاء")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong")

async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    await update.message.reply_text(f"⏰ الوقت الحالي:\n{now}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await update.message.reply_text(update.message.text)

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Chat ID:\n{update.message.chat_id}")

# ===============================
# 🚀 رسالة إجبارية عند التشغيل
# ===============================

async def startup_message(app):
    try:
        await app.bot.send_message(
            chat_id=OWNER_ID,
            text="🚀 البوت اشتغل بنجاح على Railway\n"
                 f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
        logging.info("Startup message sent")
    except Exception as e:
        logging.error(f"Startup message FAILED: {e}")

# ===============================
# 🧠 التشغيل الرئيسي
# ===============================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("time", time_cmd))
    app.add_handler(CommandHandler("id", show_id))
    app.add_handler(CommandHandler("echo", echo))

    # أي رسالة عادية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # رسالة تشغيل
    app.post_init = startup_message

    logging.info("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
