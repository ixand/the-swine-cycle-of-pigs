from models.pig import Pig
from typing import Tuple
from datetime import datetime
import random

def init_pig(user_id: int) -> Pig:
    return Pig(user_id=user_id)

def feed_pig(pig: Pig) -> Tuple[int, str | None]:
    pig.weight += random.randint(1, 11)

    if random.randint(0, 9) < 2:
        pig.strength += 1

    health_increase = random.randint(5, 15)
    pig.health = min(pig.health + health_increase, pig.max_health)

    pig.xp += 10 + random.randint(1, 5)
    level_ups, rank_msg = check_level_up(pig)  # Тепер отримуємо повідомлення про підвищення рівня

    return level_ups, rank_msg



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


def check_level_up(pig: Pig) -> Tuple[int, str]:
    """Підвищує рівень, якщо вистачає XP. Рандомно додає або силу, або розум."""
    level_ups = 0
    rank_change_message = ""  # Змінна для зберігання повідомлень про зміну рангу
    text = ""  # Ініціалізація змінної 'text'
    
    while pig.xp >= 100:
        # Визначаємо ранг до підвищення рівня
        rank_before = get_rank(pig)
        
        pig.max_health = (pig.level * 10) + 100
        pig.level += 1
        pig.xp -= 100

        # Випадковий бонус: або сила, або розум
        if random.choice([True, False]):
            pig.strength += 1
        else:
            pig.mind += 1

        level_ups += 1

        # Отримуємо ранг після підвищення рівня
        rank_after = get_rank(pig)

        # Формуємо повідомлення про підвищення рівня
        text += f"\n📈 Рівень підвищено на {level_ups}!"

        # Якщо ранг змінився, додаємо відповідне повідомлення
        if rank_before != rank_after:
            rank_change_message = f"\n🎖️ Ранг змінено: {rank_before} ➔ {rank_after}"

    return level_ups, text + rank_change_message



def get_rank(pig: Pig) -> str:
    if pig.level >= 20:
        return "Легенда ферми 🐲"
    elif pig.level >= 10:
        return "Могутній хряк 🐽"
    elif pig.level >= 5:
        return "Молодий кабан 🐗"
    else:
        return "Маленьке поросятко 🐖"

def fight(pig1: Pig, pig2: Pig) -> Tuple[Pig | None, Pig | None, int]:
    score1 = pig1.strength * 1.5 + pig1.mind + (pig1.weight / 10)+ pig1.health / 10 + random.uniform(0, 5)
    score2 = pig2.strength * 1.5 + pig2.mind + (pig2.weight / 10) + pig2.health / 10 + random.uniform(0, 5)

    if abs(score1 - score2) < 0.1:
        return None, None, 0  # нічия

    winner, loser = (pig1, pig2) if score1 > score2 else (pig2, pig1)
    xp_transfer = max(5, min(15, loser.xp // 5))
    winner.xp += xp_transfer
    loser.xp = max(0, loser.xp - xp_transfer)

    death_message = handle_death(loser)
    
    return winner, loser, xp_transfer, death_message

def handle_death(pig: Pig) -> str:
    """Обробляє смерть хряка і відродження на рівні 1."""
    if pig.health <= 0:
        pig.level = 1
        pig.xp = 10
        pig.health = 100
        return f"☠️ {pig.name} помер і був відроджений на рівні 1!"
    return ""
