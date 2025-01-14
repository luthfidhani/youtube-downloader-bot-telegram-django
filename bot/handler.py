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

    def choose_button(self):
        types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("mp4", "mp3")
        return markup
    
    def cancel_button(self):
        types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("cancel")
        return markup
    
    def start_button(self):
        types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("start")
        return markup
    
    def text(self):
        try:
            Users.objects.create(id=self.id, url=self.message, status="pending")
            bot.send_message(self.id, "Choose what you want to download", reply_markup=self.choose_button())
        except:
            bot.send_message(self.id, "Please wait until process finished", reply_markup=self.cancel_button())
    
    def mp3(self):
        try:
            user = Users.objects.filter(id=self.id)
            user.update(status="downloading")
            bot.send_message(self.id, "Please wait ...", reply_markup=self.cancel_button())
            
            options = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                info = yt_dlp.YoutubeDL().extract_info(url=user[0].url) # It will also automatically download the mp3
                
            filename = info["title"]+".mp3"
            bot.send_audio(self.id, audio=open(filename, 'rb'), reply_markup=self.start_button())
            user.delete() # Delete user from database
            os.remove(filename) # Delete file from local
        except Exception as e:
            user.delete()
            bot.send_message(self.id, e)

    def mp4(self):
        try:
            user = Users.objects.filter(id=self.id)
            user.update(status="downloading")
            bot.send_message(self.id, "Please wait ...", reply_markup=self.cancel_button())
            
            options = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': '%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                info = yt_dlp.YoutubeDL().extract_info(url=user[0].url) # It will also automatically download the mp3
                
            filename = info["title"]+".mp4"

            bot.send_video(chat_id=self.id, video=open(filename, 'rb'), reply_markup=self.start_button())
            user.delete() # Delete user from database
            os.remove(filename) # Delete file from local
        except Exception as e:
            user.delete()
            bot.send_message(self.id, e)
    
    def cancel(self):
        try:
            Users.objects.filter(id=self.id).delete()
            bot.send_message(self.id, "Canceled")
        except Exception as e:
            bot.send_message(self.id, e)
