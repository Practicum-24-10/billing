FROM python:3.10
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend

ENV PYTHONPATH=/app/

COPY backend/requirements.txt requirements.txt

COPY database/requirements.txt requirements_database.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt \
     && pip install --no-cache-dir -r requirements_database.txt

COPY database /app/database
COPY backend /app/backend
COPY migration /app/migration
COPY alembic.ini /app/alembic.ini

WORKDIR /app

CMD alembic upgrade head && gunicorn backend.src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
