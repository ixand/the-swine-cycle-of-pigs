import random
from datetime import datetime
from services.pig_service import check_level_up
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
    # Нові квести
    {
        "title": "Мисливський день 🦌",
        "description": "Твій хряк попав на полювання і принесло багато м'яса!",
        "effects": {"strength": 2, "gold": 10}
    },
    {
        "title": "Магічна трава 🌱",
        "description": "Знайшов магічну траву, яка дає додаткові сили!",
        "effects": {"xp": 25, "health": 10}
    },
    {
        "title": "Спортивний турнір 🏆",
        "description": "Ти став переможцем турніру серед свиней!",
        "effects": {"xp": 30, "strength": 3}
    },
    {
        "title": "Тренування у лісі 🌲",
        "description": "Твій хряк зайнявся фізичними вправами в лісі.",
        "effects": {"strength": 4, "health": 3}
    },
    {
        "title": "Відкриття скарбу 💎",
        "description": "Твій хряк знайшов скарб із золотими монетами та магічними предметами.",
        "effects": {"gold": 20, "xp": 40}
    }
]

def apply_quest(pig: Pig):
    quest = random.choice(QUESTS)
    for key, value in quest["effects"].items():
        setattr(pig, key, getattr(pig, key) + value)
    
    # Викликаємо check_level_up і отримуємо повідомлення
    level_ups, rank_msg = check_level_up(pig)

    # Збереження останнього часу квесту
    pig.last_quest_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return quest, level_ups, rank_msg  # Повертаємо результат, включаючи повідомлення
