from sqlite3 import IntegrityError

from fastapi import params

from model.creature import Creature
from web import explorer
from .errors import Missing, Duplicate
from .init import cursor
from model.explorer import Explorer

cursor.execute("""create table if not exists explorer(
                    name text primary key,
                    country text,
                    description text)""")

def row_to_model(row: tuple) -> Explorer | None:
    return Explorer(name=row[0], country=row[1], description=row[2])

def model_to_dict(model: Explorer) -> dict:
    return model.model_dump()

def get_one(name: str) -> Explorer | None:
    qry = "select * from explorer where name = :name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name } not found")

def get_all() -> list[Explorer | None]:
    qry = "select * from explorer"
    cursor.execute(qry)
    return [row_to_model(row) for row in cursor.fetchall()]

def create(explorer: Explorer) -> Explorer | None:
    if not explorer: return None
    qry = """insert into explorer (name, country, description) values (:name, :country, :description)"""
    params = model_to_dict(explorer)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    return get_one(explorer.name)

    return get_one(explorer.name)

def modify(name: str, explorer: Explorer) -> Explorer | None:
    if not (name and explorer): return None
    qry = """update explorer set country = :country, name = :name, description = :description where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name } not found")

    return explorer2

def delete(name: str):
    if not str: return False
    qry = """delete from explorer where name = :name"""
    params = {"name": name}
    cursor.execute(qry, params)
    if cursor.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
    else:
        return True