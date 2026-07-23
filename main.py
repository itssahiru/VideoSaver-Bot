import os
import telebot
import yt_dlp

# आपका Telegram Bot Token
TOKEN = "8430517375:AAHD-kuAKvQgBdfyTOQQQFSq851hZSPezuo"
bot = telebot.TeleBot(TOKEN)

# नया चैनल यूजरनेम
CHANNEL_USERNAME = "@VideoSaverHub"


def is_user_subscribed(user_id):
  try:
    member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status in ["member", "administrator", "creator"]:
      return True
  except Exception as e:
    print(f"Error checking subscription: {e}")
  return False


@bot.message_handler(commands=["start"])
def start(message):
  user_id = message.from_user.id
  if is_user_subscribed(user_id):
    bot.reply_to(
        message,
        "नमस्ते! 🚀 स्वागत है। अब आप किसी भी वीडियो का लिंक भेज सकते हैं,"
        " मैं उसे डाउनलोड कर दूंगा।",
    )
  else:
    bot.reply_to(
        message,
        "⚠️ **रुकिए पहले!**\n\nइस बॉट को फ्री में इस्तेमाल करने के लिए हमारे"
        f" ऑफिशियल चैनल को ज्वाइन करना ज़रूरी है:\n👉"
        f" {CHANNEL_USERNAME}\n\nचैनल ज्वाइन करने के बाद दोबारा ** /start **"
        " दबाएं!",
    )


@bot.message_handler(func=lambda message: True)
def download_video(message):
  user_id = message.from_user.id

  if not is_user_subscribed(user_id):
    bot.reply_to(
        message,
        "⚠️ कृपया वीडियो डाउनलोड करने से पहले हमारा ऑफिशियल चैनल ज्वाइन करें:\n👉"
        f" {CHANNEL_USERNAME}\n\nचैनल ज्वाइन करने के बाद दोबारा लिंक भेजें!",
    )
    return

  url = message.text
  if "http" not in url:
    bot.reply_to(message, "कृपया सही लिंक भेजें!")
    return

  bot.reply_to(message, "🔍 वीडियो डाउनलोड हो रहा है, कृपया प्रतीक्षा करें...")

  try:
    ydl_opts = {
        "format": "best",
        "outtmpl": "video.mp4",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

    bot.send_video(message.chat.id, open("video.mp4", "rb"))
    os.remove("video.mp4")
  except Exception as e:
    bot.reply_to(message, f"डाउनलोड करने में एरर आया: {str(e)}")


bot.infinity_polling()
