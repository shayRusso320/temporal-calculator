FROM python:3.14-slim

WORKDIR /app

COPY src/workflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/workflow/ /app/src/workflow/

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.workflow.main"]