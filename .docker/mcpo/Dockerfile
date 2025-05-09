FROM python:3.11-slim
WORKDIR /app
RUN pip install mcpo uv

CMD ["uvx", "mcpo", "--host", "0.0.0.0", "--port", "8000", "--config", "/config.json"]
