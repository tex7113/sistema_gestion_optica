from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload decodificado:", payload)
        return payload
    except JWTError as e:
        print("Error JWT:", e)
        return None