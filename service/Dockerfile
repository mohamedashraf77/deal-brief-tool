# Use official Python image
FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Install system dependencies (optional)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["python", "main.py"]
