import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, Message
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from textblob import TextBlob

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

KEYWORDS = [
    "نارضایتی", "استاد", "کورس", "ضعیف", "مشکل",
    "کیفیت پایین", "تاخیر", "عدم یادگیری", "اشتباه", "کند",
    "آکادمی تافل بدرد نمیخوره", "استاد ما یاد نداره", "ضعیف هست",
    "اداره اخلاق نداره", "مدیریت ضعیف هست", "صنف ما خراب هست",
    "ما امروز نمیاییم همه ما", "ما رخصتی میخواهیم",
    "ترک", "بیرون", "عوض", "رخصت", "قوی", "آرام"
]

def monitor(update: Update, context: CallbackContext):
    try:
        message: Message = update.message
        if not message:
            return

        text = message.text or message.caption
        if not text:
            return

        keyword_found = any(word in text for word in KEYWORDS)
        negative_sentiment = TextBlob(text).sentiment.polarity < 0

        if keyword_found or negative_sentiment:
            context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"پیام منفی یا کلیدی شناسایی شد:\n{text}\nاز گروه: {message.chat.title}"
            )

    except Exception as e:
        print(f"Error in monitor: {e}")

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.caption, monitor))

updater.start_polling()

# ----------- این قسمت برای Render است -------------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

updater.idle()
