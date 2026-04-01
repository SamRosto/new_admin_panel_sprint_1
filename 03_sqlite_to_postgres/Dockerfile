FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir python-dotenv psycopg2-binary

COPY . .

CMD ["python", "main.py"]