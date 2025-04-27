# Python slim imajı kullan
FROM python:3.9-slim

# Çalışma dizini
WORKDIR /app

# Gerekli paketler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY app/ .

# Port aç
EXPOSE 5000

# Başlangıç komutu
CMD ["python", "main.py"]
