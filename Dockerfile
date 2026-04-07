FROM python:3.11-slim

LABEL maintainer="HR-AI Team"
LABEL description="HR Interview Evaluator — OpenEnv"
LABEL version="1.0.0"

# No external pip packages needed (stdlib only)
WORKDIR /app

COPY . /app/

# Set Python path so imports resolve correctly
ENV PYTHONPATH=/app

# Default: run the agent
CMD ["python", "inference.py"]
