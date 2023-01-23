from passlib.context import CryptContext
from .schemas import Token
from jose import JWTError, jwt
from .settings import jwtsettings
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwtsettings().access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, key=jwtsettings().secret_key, algorithm=jwtsettings().algorithm)
    return encode_jwt
    