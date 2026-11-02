FROM python:3.10

# Setting environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV POETRY_VIRTUALENVS_PATH=/opt/poetry-venvs

# Installing dependencies
RUN apt update && apt install -y \
    dos2unix \
    && apt clean

# Install Poetry
RUN python -m pip install --upgrade pip && \
    python -m pip install poetry

# Copy dependency files
COPY ./poetry.lock /usr/src/poetry/poetry.lock
COPY ./pyproject.toml /usr/src/poetry/pyproject.toml

# Selecting a working directory
WORKDIR /usr/src/poetry

# Install dependencies in the project virtual environment
RUN python -m poetry config virtualenvs.create true && \
    python -m poetry config virtualenvs.in-project false && \
    python -m poetry env use /usr/local/bin/python && \
    python -m poetry install --no-root --only main --no-interaction --no-ansi && \
    poetry_env="$(python -m poetry env info --path)" && \
    "$poetry_env/bin/python" -c "import sqlalchemy, uvicorn" && \
    ln -s "$poetry_env" /opt/app-venv

# Selecting a working directory
WORKDIR /usr/src/fastapi
ENV PATH="/opt/app-venv/bin:${PATH}"

# Copy the source code
COPY ./src .

# Copy commands
COPY ./commands /commands

# Ensure Unix-style line endings for scripts
RUN dos2unix /commands/*.sh

# Add execute bit to commands files
RUN chmod +x /commands/*.sh
