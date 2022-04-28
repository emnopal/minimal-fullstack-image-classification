FROM python:3.9

ADD requirements.txt /
RUN pip install -r /requirements.txt

ADD . /app
WORKDIR /app

EXPOSE 5000
CMD gunicorn --worker-class gevent --workers 8 --bind ${APP_HOST}:${APP_PORT} wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
