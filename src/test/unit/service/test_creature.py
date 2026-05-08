import os
import pytest
os.environ["CRYPTID_UNIT_TEST"]= "true"

from model.creature import Creature
from service import creature
from data.errors import Missing, Duplicate
os.environ["CRYPTID_SQLITE_DB"] = ":memory"

@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman"
    )

def test_create(sample):
    response = creature.create(sample)
    assert response == sample

def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)

def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("boxturtle")

def test_modify(sample):
    sample.area = "Sesame Street"
    resp = creature.modify(sample)
    assert resp == sample

def test_modify_missing():
    thing: Creature = Creature(name="snurfle", country="RU", area="", description="something", aka="")
    with pytest.raises(Missing):
        _ = creature.modify(thing)

def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is None

def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = creature.delete(sample.name)