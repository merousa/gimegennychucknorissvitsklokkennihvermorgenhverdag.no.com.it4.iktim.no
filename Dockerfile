FROM python:3.14.7-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project

COPY src/ .
COPY jokeVault ./jokeVault

EXPOSE 5000

CMD ["uv", "run", "python", "-m", "gimegennychucknorissvitsklokkennihvermorgenhverdag_no_com_it4_iktim_no.app"]
