FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies (fonts for Pillow text overlay)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY alembic.ini .
COPY fonts ./fonts
COPY app ./app

# Create pipeline data directory with default sources
RUN mkdir -p /app/pipeline_data
COPY pipeline_data/sources.json /app/pipeline_data/sources.json

# Run migrations then start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
