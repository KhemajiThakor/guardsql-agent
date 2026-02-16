import os

API_BASE_URL = os.getenv("GUARDSQL_API_URL", "http://localhost:8000")
REQUEST_TIMEOUT = int(os.getenv("GUARDSQL_TIMEOUT", "70"))
