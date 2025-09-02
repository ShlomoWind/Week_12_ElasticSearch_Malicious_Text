FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY data_files/ ./data_files/
COPY config/ ./config/
RUN python -m nltk.downloader vader_lexicon -q
ENV PYTHONPATH=/app
CMD ["python", "src/main.py"]