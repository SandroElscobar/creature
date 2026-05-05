from fastapi import params

from model.creature import Creature
from web import explorer
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
    return row_to_model(cursor.fetchone())

def get_all() -> list[Explorer | None]:
    qry = "select * from explorer"
    cursor.execute(qry)
    return [row_to_model(row) for row in cursor.fetchall()]

def create(explorer: Explorer) -> Explorer | None:
    qry = """insert into explorer (name, country, description) values (:name, :country, :description)"""
    params = model_to_dict(explorer)
    _ = cursor.execute(qry, params)
    return get_one(explorer.name)

    return get_one(explorer.name)

def modify(name: str, explorer: Explorer) -> Explorer:
    qry = """update explorer set country = :country, name = :name, description = :description where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = cursor.execute(qry, params)
    explorer2 = get_one(explorer.name)
    return explorer2

def delete(explorer: Explorer) -> bool:
    qry = """delete from explorer where name = :name"""
    params = {"name": explorer.name}
    res = cursor.execute(qry, params)
    return bool(res)