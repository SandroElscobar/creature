from model.creature import Creature
from service import creature as code

sample = Creature(
    name="Yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman"
)

def test_create():
    response = code.create(sample)
    assert response == sample

def test_get_exist():
    response = code.get_one("Yeti")
    assert response == sample

def test_get_missing():
    response = code.get_one("boxturtle")
    assert response is None