from dataclasses import dataclass
from datetime import datetime

@dataclass
class Pig:
    user_id: int
    name: str = "Безіменний"
    weight: int = 10
    strength: int = 5
    health: int = 100
    level: int = 1
    xp: int = 0
    birth_date: str = datetime.now().strftime("%Y-%m-%d")
    feeds_today: int = 0
    last_feed_time: str = ""
    fights_today: int = 0  # Додаємо рахунок боїв
    last_fight_date: str = ""  # Дата останнього бою
