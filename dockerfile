FROM python:3.11-slim-buster

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000

CMD ["gunicorn", "main:createApp()", "-b", "0.0.0.0:9000"]