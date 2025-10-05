FROM python:3.11-slim

WORKDIR /app

COPY script/requirements.txt .
COPY script/watch.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "watch.py"]
