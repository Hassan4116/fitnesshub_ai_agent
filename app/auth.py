from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise Exception("JWT_SECRET environment variable not set")

security = HTTPBearer()

# Dependency to get the current user from JWT
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
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