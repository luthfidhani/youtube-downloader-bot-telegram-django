# syntax=docker/dockerfile:1
FROM python:3.11.8-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV APP_WORKERS 2
ENV APP_THREADS 2

# Copy local code to the container image.
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# num workers = (2 x CPU) + 1
CMD exec gunicorn --bind :8000 --workers $APP_WORKERS --threads $APP_THREADS --timeout 300 bot_youtube.wsgi:application
