import random
from models.pig import Pig

def init_pig(user_id: int) -> Pig:
    return Pig(user_id=user_id)

def feed_pig(pig: Pig):
    pig.weight += random.randint(1, 5)
    if random.randint(0, 9) < 2:  # 20% шанс підняти силу
        pig.strength += 1

def fight(pig1: Pig, pig2: Pig):
    """Повертає переможця"""
    health1 = pig1.health
    health2 = pig2.health

    while health1 > 0 and health2 > 0:
        health2 -= pig1.strength * random.uniform(0.8, 1.2)
        if health2 <= 0:
            return pig1
        health1 -= pig2.strength * random.uniform(0.8, 1.2)
    return pig2
