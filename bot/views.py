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
from bot.handler import Handler


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


@bot.message_handler(func=lambda call: call.text == "mp3")
def mp3_handler(message):
    Handler(message).mp3()


@bot.message_handler(func=lambda call: call.text == "mp4")
def mp4_handler(message):
    Handler(message).mp4()


@bot.message_handler(content_types=["text"])
def text_handler(message):
    Handler(message).text()