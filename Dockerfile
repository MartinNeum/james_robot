# Verwenden Sie ein Basisimage, das Git enthält
FROM ubuntu:20.04

# Installieren Sie Git im Container (wenn es nicht bereits im Basisimage vorhanden ist)
RUN apt-get update && apt-get install -y git

# Legen Sie das Arbeitsverzeichnis im Container fest
WORKDIR /app

# Klone das Git-Repository in das Arbeitsverzeichnis
RUN git clone https://github.com/MartinNeum/james_robot.git

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
