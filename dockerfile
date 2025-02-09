FROM python:3.11-slim

WORKDIR /app

# Copy only the necessary files
COPY pyproject.toml ./
COPY app.py ./
COPY dashboard/ ./dashboard/
COPY optimisation/ ./optimisation/

# Install system dependencies and Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry \
    && poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-root

# Expose the port your app runs on
EXPOSE 8050

# Command to run the application
CMD ["poetry", "run", "python", "app.py"]