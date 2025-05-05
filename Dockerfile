FROM python:3.12-slim

EXPOSE 8000

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the application dependencies.
WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./uv.lock /code/uv.lock

RUN uv sync --frozen --no-cache

# Copy the application into the container.
COPY /src /code/src

# Run the application.

CMD [".venv/bin/uvicorn", "src.app.main:app", "--host", "127.0.0.1", "--port", "8000"]