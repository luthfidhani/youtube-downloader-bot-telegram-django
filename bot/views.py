import os
import time
import telebot
import yt_dlp
import glob
from telebot import types
from telebot.types import Update
from django.conf import settings
from django.views import View
from django.http.response import HttpResponse
from django.core.exceptions import PermissionDenied
from bot.models import Users


bot = telebot.TeleBot(settings.BOT_TOKEN)

class IndexView(View):
    def get(self, request):
        return HttpResponse("Why u here?")

    def post(self, request):
        if request.META["CONTENT_TYPE"] == "application/json":
            json_string = request.body.decode("utf-8")
            update = Update.de_json(json_string)
            bot.process_new_updates([update])
            return HttpResponse("")
        else:
            raise PermissionDenied


# Command Handler
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.from_user.id, "Bot Start, Just copy your youtube link in here")

def delete_history_files():
    for f in glob.glob("*.mp3"):
        os.remove(f)
    for f in glob.glob("*.ogg"):
        os.remove(f)
    for f in glob.glob("*.mp4"):
        os.remove(f)
    for f in glob.glob("*.mkv"):
        os.remove(f)
    for f in glob.glob("*.mov"):
        os.remove(f)

def button():
    types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("video", "audio")
    return markup

@bot.message_handler(content_types=["text"])
def send_welcome(message):
    delete_history_files()
    chat_id = message.chat.id
    url = message.text
    try:
        Users.objects.create(id=chat_id, url=url)
        msg = bot.reply_to(message, "Choose what you want to download", reply_markup=button())
        bot.register_next_step_handler(msg, download)
    except:
        msg = bot.reply_to(message, "Please wait until process finished")


def download(message):
    try:
        chat_id = message.chat.id
        choose = message.text
        user = Users.objects.filter(id=chat_id)
        user.update(status="downloading")
        bot.send_message(chat_id, "Please wait ...")
        video_info = yt_dlp.YoutubeDL().extract_info(
                url=user[0].url, download=False
            )
        
        if choose == "audio":
            filename = f"{video_info['title']}.mp3"
            options={
                'format':'bestaudio/best',
                'keepvideo':False,
                'outtmpl':filename,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])

            bot.send_audio(chat_id, audio=open(filename, 'rb'))

        if choose == "video":
            filename = f"{video_info['title']}.mp4"
            options={
                'outtmpl':filename,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])

            bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))

        user.delete()
    except Exception as e:
        user.delete()
        bot.send_message(chat_id, e)