FROM python:3.14

# Force uv to use system environment
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.0 /uv /bin/

WORKDIR /code

COPY pyproject.toml uv.lock ./

# Install deps with dev
RUN uv sync --frozen

COPY . .
