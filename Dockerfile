# Multi-stage build for production efficiency
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create application user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY manage.py .
COPY apiservices/ ./apiservices/
COPY .env.example ./.env

# Create necessary directories and set permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Environment variables
ENV PORT=8000 \
    WORKERS=4 \
    DEBUG=False

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health/ || exit 1

# Expose port
EXPOSE $PORT

# Start script
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py initadmin && \
    gunicorn apiservices.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --access-logfile - \
    --error-logfile - \
    --log-level info



# FROM mongo:3.2.6

# ENV PORT 27017:27017
# # EXPOSE 27017:27017
# RUN sudo service mongod start
# RUN mongo
