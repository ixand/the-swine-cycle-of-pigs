from models.pig import Pig
from typing import Tuple
from datetime import datetime
import random

def init_pig(user_id: int) -> Pig:
    return Pig(user_id=user_id)

def feed_pig(pig: Pig):
    pig.weight += random.randint(1, 11)

    # Іноді дає бонус до сили
    if random.randint(0, 9) < 2:
        pig.strength += 1

    # Відновлення здоров’я
    health_increase = random.randint(5, 15)
    pig.health = min(pig.health + health_increase, pig.max_health)

    # Досвід
    pig.xp += 10 + random.randint(1, 5)

    check_level_up(pig)

def get_allowed_feedings(pig: Pig) -> int:
    """Повертає кількість дозволених годувань на день залежно від рангу (рівня)."""
    if pig.level < 5:
        return 5  # Маленьке поросятко 🐖
    elif 5 <= pig.level < 10:
        return 4  # Молодий кабан 🐗
    elif 10 <= pig.level < 20:
        return 3  # Могутній хряк 🐽
    else:
        return 2  # Легенда ферми 🐲

def attack(pig1: Pig, pig2: Pig) -> Pig:
    """Нечесна атака — тут розум має більше значення."""
    score1 = pig1.mind * 1.5 + pig1.level + random.uniform(0, 5)
    score2 = pig2.mind * 1.5 + pig2.level + random.uniform(0, 5)
    return pig1 if score1 > score2 else pig2


def check_level_up(pig: Pig) -> int:
    """Підвищує рівень, якщо вистачає XP. Рандомно додає або силу, або розум."""
    level_ups = 0
    while pig.xp >= 100:
        pig.max_health = (pig.level * 10) + 100
        pig.level += 1
        pig.xp -= 100
       
        

        # Випадковий бонус: або сила, або розум
        if random.choice([True, False]):
            pig.strength += 1
        else:
            pig.mind += 1

        level_ups += 1
    return level_ups

def get_rank(pig: Pig) -> str:
    if pig.level >= 20:
        return "Легенда ферми 🐲"
    elif pig.level >= 10:
        return "Могутній хряк 🐽"
    elif pig.level >= 5:
        return "Молодий кабан 🐗"
    else:
        return "Маленьке поросятко 🐖"

def fight(pig1: Pig, pig2: Pig) -> Tuple[Pig, Pig, int]:
    """Чесний спаринг — сила важливіша, але розум теж враховується."""
    score1 = pig1.strength * 1.5 + pig1.mind + pig1.weight + pig1.health / 10 + random.uniform(0, 5)
    score2 = pig2.strength * 1.5 + pig2.mind + pig2.weight + pig2.health / 10 + random.uniform(0, 5)
    
    if score1 > score2:
        winner, loser = pig1, pig2
    else:
        winner, loser = pig2, pig1

    xp_transfer = max(5, min(15, loser.xp // 5))
    winner.xp += xp_transfer
    loser.xp = max(0, loser.xp - xp_transfer)
    return winner, loser, xp_transfer

