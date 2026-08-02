FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY agents/day_01_structured_output /app/agents/day_01_structured_output

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "agents.day_01_structured_output.agent"]
