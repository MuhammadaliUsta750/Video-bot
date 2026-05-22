import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men Video Yuklovchi Botman!\n\n"
        "📥 Menga link yuboring:\n"
        "▶️ YouTube\n"
        "🎵 TikTok\n"
        "📸 Instagram\n"
        "📌 Pinterest\n\n"
        "Va men yuklab beraman! 🚀"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id

    if not ("youtube.com" in url or "youtu.be" in url or 
            "tiktok.com" in url or "instagram.com" in url or 
            "pinterest.com" in url):
        await update.message.reply_text("❌ Iltimos to'g'ri link yuboring!")
        return

    await update.message.reply_text("⏳ Yuklanmoqda... Kuting!")

    try:
        ydl_opts = {
            'format': 'best[filesize<50M]',
            'outtmpl': f'{chat_id}_video.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            await context.bot.send_video(
                chat_id=chat_id,
                video=video,
                caption="✅ Mana videongiz!"
            )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi!")

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.replace("/music ", "")
    chat_id = update.message.chat_id

    await update.message.reply_text("🎵 Musiqa yuklanmoqda...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{chat_id}_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{chat_id}_audio.mp3"

        with open(filename, 'rb') as audio:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=audio,
                caption="🎵 Mana musiqangiz!"
            )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("❌ Musiqa yuklab bo'lmadi!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.add_handler(CommandHandler("music", download_music))
    print("Bot ishlamoqda...")
    app.run_polling()

if __name__ == "__main__":
    main()
