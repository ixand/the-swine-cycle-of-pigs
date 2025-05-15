from dataclasses import dataclass, field
from datetime import datetime
import random

@dataclass
class Pig:
    user_id: int
    name: str = "Безіменний"
    weight: int = random.randint(1,5)
    mind: int = random.randint(1,5)
    strength: int = random.randint(1,5)
    max_health: int = random.randint(10,15) * 10
    health: int = max_health
    level: int = 1
    xp: int = 0
    gold: int = 0
    feeds_today: int = 0
    last_feed_time: str = ""
    fights_today: int = 0
    last_fight_date: str = ""
    last_quest_date: str = ""
    last_mining_time: str = ""