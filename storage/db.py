import json
import os
from models.pig import Pig

DB_FILE = "pigs.json"
pigs = {}

def load_db():
    global pigs
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            pigs = {int(k): Pig(**v) for k, v in data.items()}

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({k: vars(v) for k, v in pigs.items()}, f, ensure_ascii=False, indent=4)

def get_pig(user_id: int) -> Pig | None:
    return pigs.get(user_id)

def save_pig(pig: Pig):
    pigs[pig.user_id] = pig
    save_db()

def get_all_pigs():
    return list(pigs.values())
