from models.pig import Pig
from datetime import datetime
import random

def init_pig(user_id: int) -> Pig:
    return Pig(user_id=user_id)

def feed_pig(pig: Pig):
    pig.weight += random.randint(1, 11)
    if random.randint(0, 9) < 2:
        pig.strength += 1
     # При годуванні додаємо здоров'я
    health_increase = random.randint(5, 15) 
    pig.health = min(pig.health + health_increase, get_max_health(pig))
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
    """Функція для проведення бою між двома хряками. Повертає переможця."""
    return random.choice([pig1, pig2])

def check_level_up(pig: Pig):
    """Перевіряє і підвищує рівень хряка, якщо накопичено достатньо XP."""
    level_ups = 0

    while pig.xp >= 100:
        pig.level += 1
        pig.xp -= 100
        level_ups += 1

         # Бонус за кожен рівень
        pig.strength += 1
        pig.health += 10

    return level_ups

def get_rank(pig: Pig) -> str:
    """Повертає ранг хряка залежно від його рівня."""
    if pig.level >= 20:
        return "Легенда ферми 🐲"
    elif pig.level >= 10:
        return "Могутній хряк 🐽"
    elif pig.level >= 5:
        return "Молодий кабан 🐗"
    else:
        return "Маленьке поросятко 🐖"
    
def get_max_health(pig: Pig) -> int:
    """Розраховує максимальне здоров'я хряка залежно від рівня."""
    return 100 + (pig.level - 1) * 10

def fight(pig1: Pig, pig2: Pig):
    """Проводить спаринг за спеціальною формулою і повертає (переможця, програвшого, переданий XP)."""
    score1 = pig1.level * pig1.strength * random.choice([0.5, 17.5]) + pig1.health
    score2 = pig2.level * pig2.strength * random.choice([0.5, 17.5]) + pig2.health

    if score1 > score2:
        winner, loser = pig1, pig2
    else:
        winner, loser = pig2, pig1

    xp_transfer = max(5, min(15, loser.xp // 5))  # передається від 5 до 15 XP

    winner.xp += xp_transfer
    loser.xp = max(0, loser.xp - xp_transfer)

    return winner, loser, xp_transfer
