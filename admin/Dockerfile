FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

ENV PYTHONPATH=/app/

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . ./admin

WORKDIR /app

RUN apt-get update -y && apt-get install gettext -y

RUN msgfmt admin/locales/ru/LC_MESSAGES/base.po -o admin/locales/ru/LC_MESSAGES/base.mo

CMD gunicorn admin.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

