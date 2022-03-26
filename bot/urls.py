from bot import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

app_name = "bot"
urlpatterns = [
    path("", csrf_exempt(views.IndexView.as_view()), name="index"),
    path("/", csrf_exempt(views.IndexView.as_view()), name="index"),
]
