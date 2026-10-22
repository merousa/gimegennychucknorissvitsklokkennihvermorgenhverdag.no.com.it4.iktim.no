FROM python:3.14.7-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync --no-install-project

COPY src/ ./src/
COPY templates/ ./src/gimegennychucknorissvitsklokkennihvermorgenhverdag_no_com_it4_iktim_no/templates/
COPY paywall/ ./paywall/
COPY jokeVault ./jokeVault
EXPOSE 5000
CMD ["/app/.venv/bin/python", "src/gimegennychucknorissvitsklokkennihvermorgenhverdag_no_com_it4_iktim_no/app.py"]