import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

TOKEN = "8636741867:AAF727V2SYfVUdV3_Lie2TRCuNKNInuk2Es"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("أهلاً بكِ يا سماح! أرسلي رابط الفيديو أو المسلسل لنبدأ التحميل.")
        return

    await update.message.reply_text("جاري جلب الفيديو، قليلاً من الوقت...")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_document(document=open('video.mp4', 'rb'))
        os.remove('video.mp4')
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء التحميل: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()


