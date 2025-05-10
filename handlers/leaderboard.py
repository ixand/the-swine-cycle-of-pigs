from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage import db
from typing import List
import re
from utils.constants import LEADERBOARD_SORT_FIELDS

ITEMS_PER_PAGE = 5

def sanitize_text(text: str) -> str:
    return re.sub(r'[�-�]', '', text)

def format_leaderboard(pigs: List, sort_key: str, page: int, sort_name: str) -> str:
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    visible_pigs = pigs[start:end]
    
    text = f"\U0001F3C6 Топ хряків за: {sort_name}\n\n"
    if not visible_pigs:
        text += "Немає хряків на цій сторінці."
    for idx, pig in enumerate(visible_pigs, start=1+start):
        value = getattr(pig, sort_key)
        text += f"{idx}. {pig.name} — {sort_name}: {value}\n"
    return text

def get_leaderboard_keyboard(sort_index: int, current_page: int, max_page: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    next_sort = (sort_index + 1) % len(LEADERBOARD_SORT_FIELDS)
    builder.button(
        text=LEADERBOARD_SORT_FIELDS[sort_index][1],
        callback_data=f"leaderboard_sort:{next_sort}:{current_page}"
    )
    if current_page > 0:
        builder.button(text="⬅ Назад", callback_data=f"leaderboard_page:{sort_index}:{current_page - 1}")
    if current_page < max_page:
        builder.button(text="➡ Далі", callback_data=f"leaderboard_page:{sort_index}:{current_page + 1}")
    builder.adjust(1, 2)
    return builder.as_markup()

async def leaderboard_handler(message: types.Message):
    sort_index = 0
    sort_key, sort_name = LEADERBOARD_SORT_FIELDS[sort_index]
    page = 0
    all_pigs = db.get_all_pigs()
    if not all_pigs:
        await message.answer("Поки що немає жодного хряка у грі!")
        return

    if sort_key == "level":
        pigs_sorted = sorted(all_pigs, key=lambda p: (p.level, p.xp), reverse=True)
    else:
        pigs_sorted = sorted(all_pigs, key=lambda p: getattr(p, sort_key), reverse=True)

    max_page = max(0, (len(pigs_sorted) - 1) // ITEMS_PER_PAGE)
    text = format_leaderboard(pigs_sorted, sort_key, page, sort_name)
    keyboard = get_leaderboard_keyboard(sort_index, page, max_page)
    await message.answer(sanitize_text(text), reply_markup=keyboard)

async def leaderboard_callback_handler(callback: types.CallbackQuery):
    all_pigs = db.get_all_pigs()
    if not all_pigs:
        await callback.answer("Немає даних.", show_alert=True)
        return

    data = callback.data
    if data.startswith("leaderboard_sort"):
        _, sort_index_str, page_str = data.split(":")
    elif data.startswith("leaderboard_page"):
        _, sort_index_str, page_str = data.split(":")
    else:
        await callback.answer("Невідома дія.", show_alert=True)
        return

    sort_index = int(sort_index_str)
    page = int(page_str)
    sort_key, sort_name = LEADERBOARD_SORT_FIELDS[sort_index]

    if sort_key == "level":
        pigs_sorted = sorted(all_pigs, key=lambda p: (p.level, p.xp), reverse=True)
    else:
        pigs_sorted = sorted(all_pigs, key=lambda p: getattr(p, sort_key), reverse=True)

    max_page = max(0, (len(pigs_sorted) - 1) // ITEMS_PER_PAGE)
    if page < 0 or page > max_page:
        await callback.answer("Це межа списку!", show_alert=True)
        return

    text = format_leaderboard(pigs_sorted, sort_key, page, sort_name)
    keyboard = get_leaderboard_keyboard(sort_index, page, max_page)
    await callback.message.edit_text(sanitize_text(text), reply_markup=keyboard)
    await callback.answer()
