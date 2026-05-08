from model.user import User
from data.errors import Missing, Duplicate

fakes = [
    User(name=" kwijobo", hash="abc"),
    User(name=" ermager", hash="xyz"),
    User(name=" mbape", hash="qwe")
]

def find(name: str) -> User | None:
    for e in fakes:
        if e.name == name:
            return e
    return None

def check_missing(name: str):
    if not find(name):
        raise Missing(msg=f"User {name} missing")

def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"User {name} duplicate")

def get_all():
    return fakes

def get_one(name: str):
    check_missing(name)
    return find(name)

def create(user: User):
    check_missing(user.name)
    return user

def modify(name:str, user: User) -> User:
    check_missing(name)
    return user

def delete(name: str) -> None:
    check_missing(name)
    return None
