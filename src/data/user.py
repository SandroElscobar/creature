from fastapi import params

from model import user
from model.user import User
from .init import (conn, cursor, get_db, IntegrityError)
from errors import Missing, Duplicate

cursor.execute("""create table if not exists
                    user(
                        name text primary key,
                        hash text)""")

cursor.execute("""create table if not exists
                    xuser(
                        name text primary key
                        hash text)""")

def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)

def model_to_dict(user: User) -> dict:
    return user.model_dump()

def get_one(name: str) -> User:
    qry = "select * from user where name=:name"
    params = {"name", name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")

def get_all() -> list[User]:
    qry = "select * from user"
    cursor.execute(qry)
    rows = cursor.fetchall()
    return [row_to_model(row) for row in rows]

def create(user: User, table: str = "user"):
    """Добавление <пользователя> в таблицу user или xuser"""
    qry = (f"""insert into {table}"
           (name, hash)
           values
           (:name, :hash)""")
    params = model_to_dict(user)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"User {user.name} already exists")


def modify(name: str, user:User) -> User:
    qry = """update user set
            name=:name, hash=:hash
            where name=:name0"""
    params = {
        "name": user.name,
        "hash": user.hash,
        "name0": name
    }
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {user.name} not found")

def delete(name: str) -> None:
    user = get_one(name)
    qry = "delete from user where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    if cursor.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser")
