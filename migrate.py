import json
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

with open("pigs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

success_count = 0
error_count = 0

for user_id, pig_data in data.items():
    pig_data["user_id"] = int(user_id)
    try:
        response = supabase.table("pigs").upsert(pig_data).execute()
        if response.data:
            print(f"⬆ Завантажено хряка ID {user_id}")
            success_count += 1
        else:
            print(f"⚠️ Не вдалося вставити хряка ID {user_id}")
            error_count += 1
    except Exception as e:
        print(f"❌ Помилка для ID {user_id}: {e}")
        error_count += 1

print(f"\n✅ Готово: {success_count} успішно, {error_count} з помилками.")
