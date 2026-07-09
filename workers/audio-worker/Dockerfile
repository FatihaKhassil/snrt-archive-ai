FROM python:3.12-slim

WORKDIR /app

# Installer ffmpeg nécessaire pour Whisper
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "consumer.py"]