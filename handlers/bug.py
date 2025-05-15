from aiogram import types
from aiogram.filters import CommandObject
from aiogram.types import Message

# заміни на ID адмінського чату
ADMIN_CHAT_ID = -1002500459432

async def bug_report_handler(message: Message, command: CommandObject):
    user = message.from_user
    text = command.args

    if not text:
        await message.answer("❗ Будь ласка, надішли опис проблеми. Наприклад:\n/bug бот не відповідає після команди /fight")
        return

    author = f"{user.full_name} (@{user.username}) [ID: {user.id}]"
    report = f"🐞 *Надійшло повідомлення про баг:*\n\n📨 {text}\n\n👤 Від: {author}"

    await message.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=report,
        parse_mode="HTML"
    )

    await message.answer("✅ Дякую! Твоє повідомлення про баг надіслано розробникам.")
