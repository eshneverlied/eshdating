FROM python:3.11-slim

WORKDIR /app

RUN pip install uv
COPY pyproject.toml .
RUN uv sync

COPY . .

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
