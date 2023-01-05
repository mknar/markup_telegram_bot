FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /markup_telegram_bot
COPY requirements.txt /markup_telegram_bot/
RUN pip install -r requirements.txt
COPY . /markup_telegram_bot