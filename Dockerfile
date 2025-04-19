FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Create a writable cache directory
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Set environment variables for cache
ENV TRANSFORMERS_CACHE=/app/cache \
    HF_HOME=/app/cache \
    SENTENCE_TRANSFORMERS_HOME=/app/cache \
    PORT=7860 \
    PYTHONUNBUFFERED=1

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
