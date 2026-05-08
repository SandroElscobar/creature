from sqlite3 import IntegrityError

from .errors import Missing, Duplicate
from .init import conn, cursor
from model.creature import Creature

cursor.execute("""create table if not exists creature (
    name text primary key,
    description text,
    country text,
    area text,
    aka text)""")

def row_to_model(row: tuple) -> Creature | None:
    name, description, country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)

def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()

def get_one(name: str) -> Creature | None:
    qry = "select * from creature where name =:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"No creature with name {name}")

def get_all() -> list[Creature]:
    qry = "select * from creature"
    cursor.execute(qry)
    rows = cursor.fetchall()
    return [row_to_model(row) for row in cursor.fetchall()]

def create(creature: Creature) -> Creature | None:
    if not creature: return None
    qry = """insert into creature values (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Creature with name {creature.name} already exists")
    return get_one(creature.name)

def modify(creature: Creature):
    qry = """update creature
        set country = :country,
        name = :name,
        description = :description,
        area = :area,
        aka = :aka
        where name = :name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(msg=f"No creature with name {creature.name}")

def replace(creature: Creature) -> Creature | None:
    return creature

def delete(name):
    qry = """delete from creature where name = :name"""
    params = {"name": name}
    cursor.execute(qry, params)
    if cursor.rowcount != 1:
        raise Missing(msg=f"No creature with name {name}")

