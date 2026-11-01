FROM python:3.14.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

# сначала только зависимости — этот слой кешируется
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# потом код
COPY manage.py ./
COPY config/ ./config/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
