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
        text += f"\n📈 Рівень підвищено на {level_ups} для {pig.name}!"

        # Якщо ранг змінився, додаємо відповідне повідомлення
        if rank_before != rank_after:
            rank_change_message = f"\n🎖️ Ранг змінено: {rank_before} ➔ {rank_after}"

    return level_ups, text + rank_change_message



def get_rank(pig: Pig) -> str:
    if pig.level >= 100:
        return "🌟 Верховний Хряк"
    elif pig.level >= 90:
        return "👑 Свинячий Імператор"
    elif pig.level >= 80:
        return "🔥 Повелитель Кабанів"
    elif pig.level >= 70:
        return "⚡ Міфічний Хряк"
    elif pig.level >= 60:
        return "🐲 Герой Свиноферми"
    elif pig.level >= 50:
        return "🦾 Легендарний Кабан"
    elif pig.level >= 40:
        return "🛡️ Бойовий Ветеран"
    elif pig.level >= 30:
        return "🥇 Чемпіон Арени"
    elif pig.level >= 20:
        return "💪 Досвідчений Кабан"
    elif pig.level >= 10:
        return "🐗 Молодий Борцівник"
    elif pig.level >= 5:
        return "🐖 Амбітне Поросятко"
    else:
        return "🐷 Маленьке Поросятко"



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
    if pig.health <= 0 or pig.weight < 1:
        pig.level = 1
        pig.xp = 10
        pig.health = 100
        pig.max_health = 100
        pig.weight = 10  # відновлюємо базову масу
        return f"☠️ {pig.name} помер {'від виснаження' if pig.weight < 1 else 'у бою'} і був відроджений на рівні 1!"
    return ""

def check_level_down(pig: Pig) -> str:
    """Знижує рівень, якщо XP стало менше 0. Не дозволяє рівень нижче 1."""
    message = ""
    while pig.xp < 0 and pig.level > 1:
        pig.level -= 1
        pig.xp += 100  # умовна кількість XP, яка потрібна на кожен рівень
        message += f"⬇️ Хряк втратив рівень! Тепер рівень: {pig.level}\n"

    # Обмежуємо XP мінімумом 0 на 1 рівні
    if pig.level == 1 and pig.xp < 0:
        pig.xp = 0

    return message

def is_valid_change(field: str, current_value: int, delta: int) -> bool:
    """Перевіряє, чи дозволено змінювати значення поля на delta."""
    new_value = current_value + delta

    # нижні межі
    min_limits = {
        "strength": 1,
        "mind": 1,
        "gold": 0,
        "level": 1,
        "weight": 1,
    }

    # верхня межа для integer (max int32)
    MAX_INT32 = 2_147_483_647
    max_limits = {
        "strength": MAX_INT32,
        "mind": MAX_INT32,
        "gold": MAX_INT32,
        "level": MAX_INT32,
        "weight": MAX_INT32,
    }

    if field in min_limits and new_value < min_limits[field]:
        return False

    if field in max_limits and new_value > max_limits[field]:
        return False

    return True

MAX_INT32 = 2_147_483_647

def exceeds_max_int(field: str, current_value: int, delta: int) -> bool:
    """Повертає True, якщо результат зміни перевищує максимум int32."""
    return (current_value + delta) > MAX_INT32
