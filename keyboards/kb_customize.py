import sqlite3

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from database.db_customize_tools import get_quanity_screens


async def kb_lux_customize():


    kb = InlineKeyboardMarkup()

    button = InlineKeyboardButton("Смена имени", callback_data="rename_menu")
    kb.add(button)

    button = InlineKeyboardButton("Смена фона", callback_data="screen_roller 1")
    kb.add(button)

    button = InlineKeyboardButton("Вернуться", callback_data="return")
    kb.add(button)

    return kb


async def kb_free_customize():
    pass


async def kb_screen_roller(screen_id: int, conn:sqlite3.Connection):
    scr_quan = await get_quanity_screens(conn)
    kb = InlineKeyboardMarkup()

    left_scroll = screen_id - 1
    right_scroll = screen_id + 1
    if left_scroll == 0:
        left_scroll = scr_quan
    if right_scroll > scr_quan:
        right_scroll = 1

    button1 = InlineKeyboardButton("<<", callback_data=f"screen_roller {left_scroll}")

    button2 = InlineKeyboardButton("Выбрать", callback_data=f"screen_choose {screen_id}")

    button3 = InlineKeyboardButton(">>", callback_data=f"screen_roller {right_scroll}")

    button4 = InlineKeyboardButton("Вернуться", callback_data="return_customize")

    kb.row(button1, button2, button3).add(button4)

    return kb
