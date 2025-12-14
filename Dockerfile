FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "python -m database.init_db && python -m database.load_json && python -m main"]