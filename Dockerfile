# Single-container Dockerfile for GuardSQL Agent
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt streamlit pandas requests

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create supervisor configuration
RUN echo '[supervisord]' > /etc/supervisor/conf.d/guardsql.conf && \
    echo 'nodaemon=true' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'user=root' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo '' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo '[program:backend]' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'command=python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'directory=/app' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stdout_logfile=/dev/stdout' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stdout_logfile_maxbytes=0' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stderr_logfile=/dev/stderr' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stderr_logfile_maxbytes=0' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo '' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo '[program:frontend]' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'command=streamlit run frontend/src/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'directory=/app' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stdout_logfile=/dev/stdout' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stdout_logfile_maxbytes=0' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stderr_logfile=/dev/stderr' >> /etc/supervisor/conf.d/guardsql.conf && \
    echo 'stderr_logfile_maxbytes=0' >> /etc/supervisor/conf.d/guardsql.conf

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health && curl -f http://localhost:8501/_stcore/health || exit 1

# Run supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/guardsql.conf"]
