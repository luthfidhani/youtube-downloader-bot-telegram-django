import os
import yt_dlp
from telebot import TeleBot, types
from django.conf import settings
from bot.models import Users



bot = TeleBot(settings.BOT_TOKEN)


class Handler:
    def __init__(self, message):
        self.id = message.chat.id
        self.message = message.text

    def button(self):
        types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("mp4", "mp3")
        return markup
    
    def text(self):
        try:
            Users.objects.create(id=self.id, url=self.message, status="pending")
            bot.send_message(self.id, "Choose what you want to download", reply_markup=self.button())
        except:
            bot.send_message(self.id, "Please wait until process finished")
    
    def mp3(self):
        try:
            user = Users.objects.filter(id=self.id)
            user.update(status="downloading")
            bot.send_message(self.id, "Please wait ...")
            video_info = yt_dlp.YoutubeDL().extract_info(
                url=user[0].url, download=False
            )
            filename = f"{video_info['title']}.mp3"
            options={
                'format':'bestaudio/best',
                'keepvideo':False,
                'outtmpl':filename,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])
            bot.send_audio(self.id, audio=open(filename, 'rb'))
            user.delete()
            os.remove(filename)
        except Exception as e:
            user.delete()
            bot.send_message(self.id, e)

    def mp4(self):
        try:
            user = Users.objects.filter(id=self.id)
            user.update(status="downloading")
            bot.send_message(self.id, "Please wait ...")
            video_info = yt_dlp.YoutubeDL().extract_info(
                url=user[0].url, download=False
            )
            filename = f"{video_info['title']}.mp4"
            options={
                'outtmpl':filename,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])

            bot.send_video(chat_id=self.id, video=open(filename, 'rb'))
            user.delete()
            os.remove(filename)
        except Exception as e:
            user.delete()
            bot.send_message(self.id, e)