# Verwenden Sie ein Python-Image als Basis
FROM python:3.8

# Legen Sie das Arbeitsverzeichnis im Container fest
WORKDIR /app

# Kopieren notwendiger Dateien
COPY reminders.json .
COPY settings.json .
COPY .env .

# Kopieren Sie die Anforderungen in den Container und installieren Sie sie
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopieren Sie Ihren Bot-Code in den Container
COPY . .

# Führen Sie den Bot aus, wenn der Container gestartet wird
CMD ["python", "main.py"]
