from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Pig:
    user_id: int
    name: str = "Безіменний"
    weight: int = 1
    mind: int = 1
    strength: int = 1
    health: int = 100
    max_health: int = 100
    level: int = 1
    xp: int = 1
    gold: int = 0  # нове поле для нагород з квестів
    feeds_today: int = 0
    last_feed_time: str = ""
    fights_today: int = 0
    last_fight_date: str = ""
    last_quest_date: str = ""
    last_mining_time: str = ""
