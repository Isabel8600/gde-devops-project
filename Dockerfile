FROM python:3.11-slim as base

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Konténer Konfigurálása
EXPOSE ${PORT}

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
