from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from bot_youtube import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('admin/', admin.site.urls),
    path("webhook/", views.set_webhook),
    path("", csrf_exempt(views.IndexView.as_view())),
    path(f"{settings.BOT_TOKEN}", csrf_exempt(views.IndexView.as_view())),
]
