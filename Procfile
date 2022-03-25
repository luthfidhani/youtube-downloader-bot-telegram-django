config:set DISABLE_COLLECTSTATIC=1
release: python manage.py migrate
web: gunicorn bot_telegram.wsgi:application --log-file - --log-level debug