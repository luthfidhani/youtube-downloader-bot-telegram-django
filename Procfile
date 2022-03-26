release: python manage.py migrate
web: gunicorn bot_youtube.wsgi:application --log-file - --log-level debug --preload --workers 4