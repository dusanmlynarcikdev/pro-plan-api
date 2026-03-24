FROM python:3.14

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uv uses system environment
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

WORKDIR /code

COPY pyproject.toml uv.lock ./

# Install deps with dev
RUN uv sync --frozen

COPY ./app ./app
COPY ./tests ./tests
COPY Makefile ./
