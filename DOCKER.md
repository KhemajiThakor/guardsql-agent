# Docker Deployment Guide

## Architecture

Single-container deployment with:
- **Backend**: FastAPI on port 8000
- **Frontend**: Streamlit on port 8501
- **Database**: PostgreSQL 16 (separate container)
- **Ollama**: Runs on host machine

Both backend and frontend run in the same container using supervisor.

## Prerequisites

1. **Docker & Docker Compose** installed
2. **Ollama** running on host machine:
   ```bash
   ollama serve
   ollama pull phi3:3.8b
   ```

## Quick Start

### 1. Configure Environment

```bash
# Copy environment template
cp .env.docker .env

# Edit if needed (default values work for most cases)
nano .env
```

### 2. Build and Run

```bash
# Build and start all services
docker compose up --build

# Or run in detached mode
docker compose up --build -d
```

### 3. Access Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Configuration

### Ollama Connection

The backend connects to Ollama on the host machine.

**For Linux:**
```env
OLLAMA_BASE_URL=http://172.17.0.1:11434
```

**For Mac/Windows:**
```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### Environment Variables

Edit `.env` file:

```env
# Database
POSTGRES_DB=guardsql_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=phi3:3.8b
OLLAMA_TIMEOUT=60

# API
LOG_LEVEL=INFO

# Auth (optional)
AUTH_ENABLED=false
AUTH_USERNAME=admin
AUTH_PASSWORD=changeme
```

## Docker Commands

### Start Services
```bash
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f app
docker compose logs -f postgres
```

### Rebuild
```bash
docker compose up --build -d
```

### Clean Up
```bash
# Stop and remove containers, networks
docker compose down

# Also remove volumes (deletes database data)
docker compose down -v
```

## Troubleshooting

### Ollama Connection Failed

**Check Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

**Update OLLAMA_BASE_URL:**
- Linux: `http://172.17.0.1:11434`
- Mac/Windows: `http://host.docker.internal:11434`

### Database Connection Failed

**Check PostgreSQL:**
```bash
docker compose logs postgres
```

**Verify connection:**
```bash
docker compose exec postgres psql -U postgres -d guardsql_db -c "SELECT 1;"
```

### Container Won't Start

**Check logs:**
```bash
docker compose logs app
```

**Rebuild from scratch:**
```bash
docker compose down -v
docker compose up --build
```

## Production Deployment

### Security Hardening

1. **Enable Authentication:**
   ```env
   AUTH_ENABLED=true
   AUTH_USERNAME=your_username
   AUTH_PASSWORD=strong_password
   ```

2. **Use Strong Database Password:**
   ```env
   POSTGRES_PASSWORD=strong_random_password
   ```

3. **Use Reverse Proxy:**
   - Add Nginx/Traefik in front
   - Enable SSL/TLS
   - Configure proper headers

### Scaling

For production, consider:
- Separate containers for backend/frontend
- Load balancer
- Database replication
- Monitoring (Prometheus/Grafana)

## File Structure

```
guardsql-agent/
├── Dockerfile              # Single multi-stage Dockerfile
├── docker-compose.yml      # Service orchestration
├── .env.docker            # Environment template
├── .dockerignore          # Docker ignore rules
└── complete_setup.sql     # Database initialization
```

## Health Checks

Both services have health checks:

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:8501/_stcore/health
```

## Ports

- `8000` - Backend API
- `8501` - Frontend UI
- `5432` - PostgreSQL (exposed for debugging)

## Volumes

- `postgres_data` - Persistent database storage

Data persists across container restarts.

---

**Ready to deploy! 🚀**
