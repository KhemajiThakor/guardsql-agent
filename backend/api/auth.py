import secrets
import logging
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from backend.core.config import get_settings

logger = logging.getLogger(__name__)
security = HTTPBasic(auto_error=False)

def verify_credentials(credentials: Optional[HTTPBasicCredentials] = Security(security)):
    settings = get_settings()
    
    if not settings.auth_enabled:
        return True
    
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    correct_username = secrets.compare_digest(credentials.username, settings.auth_username)
    correct_password = secrets.compare_digest(credentials.password, settings.auth_password)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
