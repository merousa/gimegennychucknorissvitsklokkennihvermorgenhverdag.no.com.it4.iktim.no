FROM python:3.14.7-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
copy pyproject.toml .

RUN uv sync

COPY src/ .

EXPOSE 5000

CMD ["uv", "run", "app.py"]
