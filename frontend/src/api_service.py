import requests
from typing import Dict, Optional, Tuple

from config import API_BASE_URL, REQUEST_TIMEOUT

class APIService:
    @staticmethod
    def check_health() -> Tuple[bool, str]:
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                return True, "Online"
            return False, f"Error {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Offline"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def execute_query(question: str, auth: Optional[Tuple[str, str]] = None) -> Dict:
        try:
            response = requests.post(
                f"{API_BASE_URL}/query",
                json={"question": question},
                auth=auth,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            elif response.status_code == 401:
                return {"success": False, "error": "Authentication required", "code": 401}
            elif response.status_code == 503:
                return {"success": False, "error": "Service unavailable. Check if Ollama is running.", "code": 503}
            else:
                error_detail = response.json().get("detail", "Unknown error")
                return {"success": False, "error": error_detail, "code": response.status_code}
                
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Cannot connect to backend API", "code": 0}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out", "code": 0}
        except Exception as e:
            return {"success": False, "error": str(e), "code": 0}
