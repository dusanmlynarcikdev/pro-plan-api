FROM python:3.14

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.0 /uv /bin/

# Force uv to use system environment
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

WORKDIR /code

COPY pyproject.toml uv.lock ./

# Install deps with dev
RUN uv sync --frozen

COPY ./app ./app
COPY ./tests ./tests
COPY .env ./
COPY .env.test ./
COPY Makefile ./
