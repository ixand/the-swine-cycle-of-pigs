import asyncio
import random
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage import supabase_storage as db
from services.pig_service import fight, check_level_up, get_rank
from utils.pig_helpers import ensure_pig_exists
from utils.fight_templates import get_fight_templates

# Зберігаємо: {opponent_id: (chat_id, message_id)}
pending_sparrings = {}

async def sparring_request_handler(message: types.Message):
    user_id = message.from_user.id
    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="Прийняти виклик 🐖", callback_data=f"accept_sparring:{user_id}")

    sent_message = await message.answer(
        f"🐷 {pig.name} викликає на спаринг!\nНатисни кнопку, щоб прийняти виклик!",
        reply_markup=builder.as_markup()
    )

    # Зберігаємо chat_id та message_id повідомлення з кнопкою
    pending_sparrings[user_id] = (sent_message.chat.id, sent_message.message_id)

async def sparring_accept_handler(callback: types.CallbackQuery):
    data = callback.data
    if not data.startswith("accept_sparring:"):
        return

    opponent_id = int(data.split(":")[1])
    challenger_id = callback.from_user.id

    if opponent_id == challenger_id:
        await callback.answer("Не можна приймати свій власний виклик!", show_alert=True)
        return

    if opponent_id not in pending_sparrings:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            pass
        return

    pig1 = db.get_pig(opponent_id)
    pig2 = db.get_pig(challenger_id)

    if not pig1 or not pig2:
        await callback.answer("Один із учасників не має хряка!", show_alert=True)
        return

    if pig1.health < 13 or pig2.health < 13:
        await callback.answer("Обидва хряки повинні мати мінімум 13 ❤️!", show_alert=True)
        return

    await callback.answer("Суперник прийняв виклик! Починається бій...")

    # Видаляємо кнопку з усіх чатів
    chat_id, message_id = pending_sparrings.pop(opponent_id)
    try:
        await callback.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
    except:
        pass

    # Видаляємо кнопку і з поточного повідомлення (на випадок, якщо це інший користувач)
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    templates = get_fight_templates(pig1.name, pig2.name)
    selected_events = random.sample(templates, k=5)
    for line in selected_events:
        await callback.message.answer(line)
        await asyncio.sleep(2)

    winner, loser, xp_transfer, death_message = fight(pig1, pig2)
    db.save_pig(pig1)
    db.save_pig(pig2)

    if not winner:
        await callback.message.answer("🤝 Бій закінчився нічиєю! Обидва хряки втомлені, але залишились гордими.")
        return

    result_text = (
        f"\n🏁 Спаринг завершено!\n"
        f"🏆 Переможець: {winner.name}\n"
        f"➕ +{xp_transfer} XP для {winner.name}\n"
        f"➖ -{xp_transfer} XP для {loser.name}"
    )

    if death_message:
        result_text += f"\n{death_message}"

    level_ups, level_text = check_level_up(winner)
    if level_ups:
        result_text += level_text
        if winner.level in (5, 10, 20):
            result_text += f"\n🎖️ Новий ранг: {get_rank(winner)}!"
        db.save_pig(winner)

    await callback.message.answer(result_text)
