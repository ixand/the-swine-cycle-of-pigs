import asyncio
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage import db
from services.pig_service import fight, check_level_up, get_rank
import random

# Тимчасова пам'ять активних спарингів
pending_sparrings = {}

async def sparring_request_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="Прийняти виклик 🐖", callback_data=f"accept_sparring:{user_id}")
    pending_sparrings[user_id] = True

    await message.answer(
        f"🐷 {pig.name} викликає на спаринг!\nНатисни кнопку, щоб прийняти виклик!",
        reply_markup=builder.as_markup()
    )

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
        await callback.answer("Цей виклик уже неактивний або був прийнятий.", show_alert=True)
        return

    pig1 = db.get_pig(opponent_id)
    pig2 = db.get_pig(challenger_id)

    if not pig1 or not pig2:
        await callback.answer("Один із учасників не має хряка!", show_alert=True)
        return

    if pig1.health < 13 or pig2.health < 13:
        await callback.answer("Обидва хряки повинні мати мінімум 13 ❤️!", show_alert=True)
        return

    # Відповідаємо Telegram'у миттєво, щоби уникнути timeouts
    await callback.answer("Суперник прийняв виклик! Починається бій...")

    # Видаляємо кнопку одразу після відповіді
    del pending_sparrings[opponent_id]
    await callback.message.edit_reply_markup(reply_markup=None)

    # Сценарії бою
    templates = [
        f"{pig1.name} зробив перший стрибок і вдарив рогом!",
        f"{pig2.name} ухилився і наніс контрудар!",
        f"{pig1.name} пробує психологічну атаку — ірже як скажений!",
        f"{pig2.name} кидає шматок буряка в обличчя супернику!",
        f"Обидва хряки кружляють у пошуках слабкого місця...",
        f"{pig1.name} втрачає рівновагу, але одразу відновлюється!",
        f"{pig2.name} заблокував удар в останній момент!",
        f"Битва переходить у затяжну боротьбу за домінування...",
        f"{pig1.name} використовує свою масу, щоб зіштовхнути суперника!",
        f"{pig2.name} демонструє неймовірну витривалість!",
        f"{pig1.name} вдається у відчайдушну атаку — і майже влучає!",
        f"{pig2.name} впадає у лють і не стримує себе!",
        f"Глядачі аплодують — такої битви ще не бачили!",
        f"{pig1.name} майстерно обманув рухом і наніс удар з флангу!",
        f"{pig2.name} піднімає клуб пилу і зникає на мить!",
        f"В обох на мордах — рішучість і злість!",
        f"{pig1.name} показує тактичне мислення і робить крок назад...",
        f"{pig2.name} заганяє суперника в кут!",
        f"Суддя (гусак) гучно кряче — битва триває!",
        f"{pig1.name} відволікає увагу, хрюкаючи на публіку!",
        f"{pig2.name} тисне силою, але втрачає пильність!",
        f"Битва досягла кульмінації — вирішальний момент наближається...",
        f"Здається, один з хряків починає втомлюватись...",
        f"{pig1.name} вичікує момент для останнього ривка!",
        f"{pig2.name} йде ва-банк!"
    ]

    selected_events = random.sample(templates, 5)
    for line in selected_events:
        await callback.message.answer(line)
        await asyncio.sleep(3)

    # Бій і результат
    winner, loser, xp_transfer = fight(pig1, pig2)
    db.save_pig(pig1)
    db.save_pig(pig2)

    if winner is None:
        await callback.message.answer("🤝 Бій закінчився нічиєю! Обидва хряки втомлені, але залишились гордими.")
        return


    result_text = (
        f"\n🏁 Спаринг завершено!\n"
        f"🏆 Переможець: {winner.name}\n"
        f"➕ +{xp_transfer} XP для {winner.name}\n"
        f"➖ -{xp_transfer} XP для {loser.name}"
    )

    level_ups = check_level_up(winner)
    if level_ups:
        result_text += f"\n📈 Рівень підвищено на {level_ups}!"
        if winner.level in (5, 10, 20):
            result_text += f"\n🎖️ Новий ранг: {get_rank(winner)}!"

    await callback.message.answer(result_text)
