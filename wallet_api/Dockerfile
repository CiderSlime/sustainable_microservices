FROM python:3.11-slim

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY alchemy ./alchemy
COPY wallet_api ./wallet_api

CMD ["python", "/wallet_api/main.py"]