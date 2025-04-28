from models.pig import Pig
from datetime import datetime
import random

def init_pig(user_id: int) -> Pig:
    return Pig(user_id=user_id)

def feed_pig(pig: Pig):
    pig.weight += random.randint(1, 5)
    if random.randint(0, 9) < 2:
        pig.strength += 1

def calculate_age_in_months(birth_date: str) -> int:
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    now = datetime.now()
    return (now.year - birth.year) * 12 + now.month - birth.month

def get_allowed_feedings(pig: Pig) -> int:
    months = calculate_age_in_months(pig.birth_date)

    if months < 2:
        return 5  # Поросята до 2 місяців
    elif 2 <= months < 4:
        return 4  # Підсвинки 2-4 міс
    elif 4 <= months < 6:
        return 3  # Свині на відгодівлі
    else:
        return 2  # Дорослі свині
    
def fight(pig1: Pig, pig2: Pig) -> Pig:
    """Функція для проведення бою між двома хряками. Повертає переможця."""
    health1 = pig1.health
    health2 = pig2.health

    while health1 > 0 and health2 > 0:
        # Перший атакує другого
        damage1 = max(1, pig1.strength * random.uniform(0.7, 7.3))
        health2 -= damage1
        if health2 <= 0:
            return pig1
        
        # Другий атакує першого
        damage2 = max(1, pig2.strength * random.uniform(0.7, 7.3))
        health1 -= damage2
        if health1 <= 0:
            return pig2

    return pig1 if health1 > health2 else pig2

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
        return "Маленький поросятко 🐖"
