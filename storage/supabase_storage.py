from supabase import create_client, Client
from models.pig import Pig
from typing import Optional
from dataclasses import asdict
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_pig(user_id: int) -> Optional[Pig]:
    response = supabase.table("pigs").select("*").eq("user_id", int(user_id)).execute()
    if response.data:
        return Pig(**response.data[0])
    return None

def save_pig(pig: Pig):
    data = asdict(pig)
    data["user_id"] = int(pig.user_id)  # гарантуємо тип
    print("🔁 Збереження хряка в Supabase:", data)  # ТИМЧАСОВО для дебагу
    supabase.table("pigs").upsert(data).execute()

def get_all_pigs() -> list[Pig]:
    response = supabase.table("pigs").select("*").execute()
    return [Pig(**row) for row in response.data]
