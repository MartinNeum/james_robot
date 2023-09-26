# Verwenden Sie ein Python-Image als Basis
FROM python:3.8

# Legen Sie das Arbeitsverzeichnis im Container fest
WORKDIR /app

# Kopieren Sie die Anforderungen in den Container und installieren Sie sie
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopieren Sie Ihren Bot-Code in den Container
COPY . .

# JSON Dateien erstellen
RUN echo '[]' > settings.json
RUN echo '[]' > reminders.json
RUN echo '[]' > shoppinglist.json

# Führen Sie den Bot aus, wenn der Container gestartet wird
CMD ["python", "james.py"]
