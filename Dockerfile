FROM python:3.13-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install only web dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only web --no-interaction --no-ansi

COPY ./app /app/app

# Create models directory
RUN mkdir -p /app/app/models

# Copy model files
COPY app/models/ /app/app/models/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 