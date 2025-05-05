import random
from datetime import datetime
from models.pig import Pig

QUESTS = [
    {
        "title": "Розгріб смітник 🗑️",
        "description": "Твій хряк знайшов щось смачне!",
        "effects": {"xp": 15, "gold": 5}
    },
    {
        "title": "Перегони з кабанами 🐗",
        "description": "Швидкість — це сила!",
        "effects": {"xp": 20}
    },
    {
        "title": "Хряк-детектив 🕵️",
        "description": "Хто вкрав моркву?..",
        "effects": {"xp": 10, "strength": 1}
    },
    {
        "title": "День сну 😴",
        "description": "Відпочинок — найкращий тренінг.",
        "effects": {"health": 5}
    },
    {
        "title": "Розмова з шаманом 🐗🔮",
        "description": "Шаман передрік новий рівень!",
        "effects": {"level": 1}
    },
]

def apply_quest(pig: Pig):
    quest = random.choice(QUESTS)
    for key, value in quest["effects"].items():
        setattr(pig, key, getattr(pig, key) + value)
    pig.last_quest_date = datetime.now().strftime("%Y-%m-%d")
    return quest
