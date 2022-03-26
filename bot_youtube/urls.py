from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from bot_youtube import views



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("webhook/", views.set_webhook),
    path(f"{settings.BOT_TOKEN}", include("bot.urls", namespace="bot")),
]
