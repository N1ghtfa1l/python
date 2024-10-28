from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from src.config import SECRET_KEY
from fastapi import HTTPException
import jwt
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Токен недействителен")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Токен недействителен")
