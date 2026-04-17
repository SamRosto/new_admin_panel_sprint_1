FROM python:3.12-slim

WORKDIR /opt/etl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONPATH=/opt/etl
CMD ["python", "-m", "app.main"]