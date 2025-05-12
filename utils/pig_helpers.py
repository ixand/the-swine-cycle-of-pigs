from aiogram import types
from storage import supabase_storage as db

async def ensure_pig_exists(message: types.Message, user_id: int):
    pig = db.get_pig(user_id)
    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return None
    return pig


def get_health_percent(pig) -> float:
    return round((pig.health / pig.max_health) * 100, 2)