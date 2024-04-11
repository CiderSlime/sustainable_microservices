FROM python:3.11-slim

WORKDIR .

ENV DB_HOST=postgres

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY alchemy ./alchemy
COPY wallet_processor ./wallet_processor

CMD ["python", "/wallet_processor/main.py"]