import telebot
import time
from django.http.response import HttpResponse
from django.conf import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)


def index(request):
    return HttpResponse("Sorry! not much to see here.")


def set_webhook(request):
    try:
        bot.remove_webhook()
        time.sleep(0.1)
        bot.set_webhook(url=settings.WEBHOOK_URL)
        return HttpResponse("Webhook was set")
    except Exception as err:
        return HttpResponse(err)
