FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CMAKE_BUILD_PARALLEL_LEVEL=1
ENV MAKEFLAGS="-j1"
ENV CMAKE_ARGS="-DDLIB_USE_CUDA=0 -DDLIB_NO_GUI_SUPPORT=ON"

# Install system dependencies for OpenCV and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install pre-compiled dlib wheel + face-recognition without compiling from source
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir dlib-bin && \
    pip install --no-cache-dir --no-deps face-recognition

# Copy and install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY . .

# Ensure storage directories exist
RUN mkdir -p dataset models

EXPOSE 10000

# Start application using Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 4 --timeout 180 'app:app'"]
