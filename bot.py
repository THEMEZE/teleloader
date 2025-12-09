import logging
import os
import nest_asyncio
import yt_dlp
import time

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from dotenv import load_dotenv

# ------------------------------------------------
# Chargement des variables secrètes
# ------------------------------------------------
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")          # récupéré depuis .env
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

nest_asyncio.apply()

# ------------------------------------------------
# LOGGER
# ------------------------------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# États de la conversation
URL, FORMAT = range(2)

# ------------------------------------------------
# Fonction yt-dlp
# ------------------------------------------------
def download_with_ytdlp(url: str, format_choice: str) -> tuple[str, dict]:
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True
    }

    if format_choice == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title")
        uploader = info.get("uploader")
        duration = info.get("duration")

        ydl.download([url])

        filename = ydl.prepare_filename(info)
        if format_choice == "mp3":
            filename = filename.rsplit(".", 1)[0] + ".mp3"

    return filename, {"title": title, "uploader": uploader, "duration": duration}

# ------------------------------------------------
# BOT TELEGRAM
# ------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("👋 Envoie-moi une URL YouTube / Instagram / TikTok / etc.")
    return URL

async def receive_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['url'] = update.message.text.strip()

    await update.message.reply_text(
        "🎯 Choisis un format :\n"
        "1️⃣ Vidéo MP4\n"
        "2️⃣ Audio MP3"
    )
    return FORMAT

async def receive_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text.strip()

    if choice == "1":
        format_choice = "mp4"
    elif choice == "2":
        format_choice = "mp3"
    else:
        await update.message.reply_text("❌ Choix invalide. Tape 1 ou 2.")
        return FORMAT

    url = context.user_data['url']
    await update.message.reply_text("⏳ Téléchargement en cours...")

    try:
        file_path, info = download_with_ytdlp(url, format_choice)

        await update.message.reply_text(
            f"📹 Titre : {info['title']}\n"
            f"📺 Uploader : {info['uploader']}\n"
            f"⏱️ Durée : {info['duration']} sec"
        )

        await update.message.reply_text("📤 Envoi du fichier...")

        with open(file_path, "rb") as f:
            await update.message.reply_document(f)

        await update.message.reply_text("✅ Terminé ! Tape /start pour recommencer.")

    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"❌ Erreur : {e}")
        await update.message.reply_text("Réessaie avec une autre URL.")

    return ConversationHandler.END


# ------------------------------------------------
# MAIN
# ------------------------------------------------
def main():
    if not TOKEN:
        print("❌ ERREUR : Le TOKEN n'est pas dans .env")
        return

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_url)],
            FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_format)]
        },
        fallbacks=[]
    )

    app.add_handler(conv)

    print("🤖 Bot lancé.")
    app.run_polling()


if __name__ == "__main__":
    main()
