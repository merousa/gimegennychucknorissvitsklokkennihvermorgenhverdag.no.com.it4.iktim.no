FROM python:3.14.7-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync --no-install-project

COPY src/ .
COPY jokeVault ./jokeVault

EXPOSE 5000

CMD ["uv", "run", "python", "-m", "gimegennychucknorissvitsklokkennihvermorgenhverdag_no_com_it4_iktim_no.app"]
