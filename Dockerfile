FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for dlib, opencv, and cmake
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Ensure storage directories exist
RUN mkdir -p dataset models

EXPOSE 10000

# Start application with Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 4 --timeout 180 'app:app'"]
