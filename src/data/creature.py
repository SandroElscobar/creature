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
    return row_to_model(row)

def get_all() -> list[Creature]:
    qry = "select * from creature"
    cursor.execute(qry)
    rows = cursor.fetchall()
    return [row_to_model(row) for row in cursor.fetchall()]

def create(creature: Creature) -> Creature | None:
    qry = """insert into creature values (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    cursor.execute(qry, params)
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
    _ = cursor.execute(qry, params)
    return get_one(creature.name)

def replace(creature: Creature) -> Creature | None:
    return creature

def delete(creature: Creature):
    qry = """delete from creature where name = :name"""
    params = {"name": creature.name}
    res = cursor.execute(qry, params)
    return bool(res)

