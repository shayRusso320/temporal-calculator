FROM python:3.14-slim

WORKDIR /app

COPY src/operators/divide/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/operators/divide/worker.py /app/worker.py

ENV PYTHONPATH=/app

CMD ["python", "/app/worker.py"]