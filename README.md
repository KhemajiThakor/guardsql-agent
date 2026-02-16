# GuardSQL Agent

🛡️ **Secure SQL query generator from natural language using AI**

Transform natural language questions into SQL queries with built-in security, validation, and a clean dark-theme UI.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🤖 **AI-Powered**: Uses Llama/Phi models via Ollama for natural language to SQL conversion
- 🛡️ **Secure**: Read-only database access, SQL validation, forbidden keyword detection
- 🎨 **Modern UI**: Clean dark-theme chatbot interface
- 📊 **Interactive Results**: View, download, and analyze query results
- 🔄 **Error Recovery**: Automatic retry with error context
- 📝 **Audit Logging**: All queries logged to database
- 🐳 **Docker Ready**: Single-command deployment with Docker Compose

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/guardsql-agent.git
cd guardsql-agent

# 2. Start Ollama on host
ollama serve
ollama pull phi3:3.8b

# 3. Run with Docker
docker compose up --build
```

**Access:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

### Option 2: Local Development

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi3:3.8b

# 2. Setup database
sudo -u postgres psql -f complete_setup.sql

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Run services
# Terminal 1: Ollama
ollama serve

# Terminal 2: Backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 3: Frontend
streamlit run frontend/src/app.py
```

## 📁 Project Structure

```
guardsql-agent/
├── backend/              # FastAPI backend
│   ├── api/             # Routes, schemas, auth
│   ├── core/            # Config, logging, exceptions
│   ├── db/              # Database connection
│   ├── services/        # Business logic (LLM, validator, executor)
│   └── main.py          # Entry point
├── frontend/            # Streamlit frontend
│   ├── .streamlit/      # Streamlit config
│   └── src/
│       ├── app.py       # Main UI
│       ├── api_service.py
│       └── config.py
├── tests/               # Unit & integration tests
├── .github/             # GitHub Actions CI
├── Dockerfile           # Multi-stage Docker build
├── docker-compose.yml   # Service orchestration
├── complete_setup.sql   # Database schema & sample data
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎯 Usage

### Example Queries

```
Show me all customers from Texas
List products under $100
How many orders are completed?
Show top 5 most expensive products
List customers with their order totals
```

### API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Execute Query:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all customers"}'
```

## 🔒 Security Features

### Database Level
- Read-only user with SELECT-only permissions
- No DDL/DML access
- Connection pooling with limits

### Application Level
- SQL validation using sqlglot
- Forbidden keyword detection (INSERT, UPDATE, DELETE, DROP, etc.)
- SELECT-only enforcement
- Auto-LIMIT injection (100 rows)
- Multiple statement blocking
- System table access prevention

### LLM Level
- Strict system prompt
- Anti prompt-injection rules
- Schema-only context
- Temperature set to 0.1

## ⚙️ Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://readonly_user:readonly_pass@localhost:5432/guardsql_db

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:3.8b
OLLAMA_TIMEOUT=60

# API
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# Auth (optional)
AUTH_ENABLED=false
AUTH_USERNAME=admin
AUTH_PASSWORD=changeme
```

### Docker Configuration

For Docker deployment, Ollama runs on host:
- **Linux**: `OLLAMA_BASE_URL=http://172.17.0.1:11434`
- **Mac/Windows**: `OLLAMA_BASE_URL=http://host.docker.internal:11434`

## 🐳 Docker Deployment

### Quick Start

```bash
# Start Ollama on host
ollama serve
ollama pull phi3:3.8b

# Build and run
docker compose up --build
```

### Docker Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Clean up (including volumes)
docker compose down -v
```

### Architecture

- **Single Container**: Backend (FastAPI) + Frontend (Streamlit) using supervisor
- **PostgreSQL**: Separate container with persistent volume
- **Ollama**: Runs on host machine
- **Ports**: 8000 (API), 8501 (UI), 5433 (DB)

See [DOCKER.md](DOCKER.md) for detailed deployment guide.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend tests/

# Test specific module
pytest tests/test_validator.py
```

See [TEST_QUERIES.md](TEST_QUERIES.md) for comprehensive test cases.

## 📊 Database Schema

Sample e-commerce database includes:
- **customers**: Customer information
- **products**: Product catalog
- **orders**: Order records
- **order_items**: Order line items
- **query_logs**: Query audit trail

## 🐛 Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Verify model
ollama list
```

### Database Connection Error
```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Test connection
psql -U readonly_user -d guardsql_db -h localhost
```

### Memory Issues
If using llama3.1:8b and getting memory errors, switch to phi3:3.8b:
```bash
ollama pull phi3:3.8b
# Update OLLAMA_MODEL in .env
```

### Docker Port Conflict
If port 5432 is in use, the docker-compose uses 5433 instead.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/guardsql-agent/issues)
- **Documentation**: See docs in repository
- **Test Queries**: See [TEST_QUERIES.md](TEST_QUERIES.md)

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- LLM via [Ollama](https://ollama.ai/)
- SQL validation by [sqlglot](https://github.com/tobymao/sqlglot)

---

**Made with ❤️ for secure database querying**
