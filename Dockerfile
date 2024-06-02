FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install --no-cache-dir -r requirements.txt 

COPY src/ src/
COPY data/ data/

CMD ["python", "src/utils/kafka_consumer.py"]