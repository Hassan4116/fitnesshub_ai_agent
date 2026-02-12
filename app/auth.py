from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os

security = HTTPBearer()

def get_jwt_secret():
    """Lazy load JWT_SECRET to avoid Windows multiprocessing issues"""
    jwt_secret = os.getenv("JWT_SECRET")
    if not jwt_secret:
        raise Exception("JWT_SECRET environment variable not set")
    return jwt_secret

# Dependency to get the current user from JWT
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError as e:
        print("JWT error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {
        "id": payload["id"],
        "phoneNumber": payload.get("email"),
        "token": token
    }