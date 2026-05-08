from datetime import timedelta, datetime, UTC
import os
from  jose import jwt, JWTError
from model.user import User

if os.getenv("CRYPTID_NIT_TEST"):
    from fake import user as data
else:
    from data import user as data

# Новые данные auth

from passlib.context import CryptContext

SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verifi_password(plain: str, hash: str) -> bool:
    """Хэширование строки <plain> и сравнение с записью <hash> из базы данных"""
    return pwd_context.verify(plain, hash)

def get_jwt_username(token: str) -> str | None:
    """Возврат имени пользователя из JWT-доступа <token>"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except JWTError:
        return None
    return username

def get_current_user(token: str) -> User | None:
    """Декодирование токена <token> доступа OAuth и возврат объекта User"""
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user
    return None

def lookup_user(username: str) -> User | None:
    """Возврат совпадающего пользователя из базы данных для строки <name>"""
    if user := data.get_one(username):
        return user
    return None

def auth_user(name: str, plain: str) -> User | None:
    """Аутентификация пользователя <name> и <plain> пароль"""
    if not (user := lookup_user(name)):
        return None
    if not verifi_password(plain, user.hash):
        return None
    return user

def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    """Возвращение токена доступа JWT"""
    src = data.copy()
    now = datetime.now(UTC)
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encode_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


# CRUD - пассивный материал

def get_all() -> list[User]:
    return data.get_all()

def get_one(name: str) -> User:
    return data.get_one(name)

def create(user: User) -> User:
    return data.create(user)

def modify(name: str, user: User) -> User:
    return data.modify(name, user)

def delete(name: str) -> None:
    return data.delete(name)



