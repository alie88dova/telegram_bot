from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def kb_return() -> ReplyKeyboardMarkup:

    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Вернуться", callback_data="return")
    kb.add(button)

    return kb

async def kb_remove():
    return ReplyKeyboardRemove()