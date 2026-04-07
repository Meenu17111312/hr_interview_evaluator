FROM python:3.11-slim

LABEL maintainer="HR-AI Team"
LABEL description="HR Interview Evaluator — OpenEnv"
LABEL version="1.0.0"

# No external pip packages needed (stdlib only)
WORKDIR /app

COPY . /app/

# Set Python path so imports resolve correctly
ENV PYTHONPATH=/app

RUN pip install fastapi uvicorn

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
