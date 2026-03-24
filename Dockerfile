FROM python:3.14

WORKDIR /code

# Copy source code
COPY ./app .
COPY pyproject.toml .
COPY uv.lock .

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uv uses system environment
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Install dependencies
RUN uv sync --frozen --no-cache

