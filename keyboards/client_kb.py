from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


async def create_roller_novel_kb(index: int, count_click_left=0, count_click_right=0) -> InlineKeyboardMarkup:

    """Создает клавиатуру для работы системы перлистывания chapter"""

    kb_section = InlineKeyboardMarkup()
    button_left = InlineKeyboardButton(f'<<', callback_data=f'novel {index - 1} {count_click_left+1} {0}')
    button_middle = InlineKeyboardButton(f'---', callback_data=f'menu')
    button_right = InlineKeyboardButton(f'>>', callback_data=f'novel {index + 1} {0} {count_click_right+1}')
    button_select = InlineKeyboardButton(f'Выбрать', callback_data=f'schapter {index}')
    kb_section.row(button_left, button_middle, button_right).add(button_select)

    return kb_section


async def create_roller_chapter_kb(index: int, chapter_index, count_click_left=0, count_click_right=0) -> InlineKeyboardMarkup:

    """Создает клавиатуру для работы системы перлистывания chapter"""

    kb_section = InlineKeyboardMarkup()
    button_left = InlineKeyboardButton(f'<<', callback_data=f'chapter {chapter_index} {index - 1} {count_click_left+1} {0}')
    button_middle = InlineKeyboardButton(f'---', callback_data=f'middle')
    button_right = InlineKeyboardButton(f'>>', callback_data=f'chapter {chapter_index} {index + 1} {0} {count_click_right+1}')
    button_select = InlineKeyboardButton(f'Выбрать', callback_data=f'sblock {index}')
    kb_section.row(button_left, button_middle, button_right).add(button_select)

    return kb_section


async def menu_back():

    button_middle = InlineKeyboardButton(f'В меню', callback_data=f'menu')
    kb_section = InlineKeyboardMarkup()
    kb_section.row(button_middle)

    return kb_section

async def kb_first_enter() -> InlineKeyboardMarkup:

    kb = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton(f"Идем дальше", callback_data="first_enter_1")
    return kb.row(button_next)


async def kb_first_enter_2() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton(f"Идем дальше", callback_data="menu_first")
    return kb.row(button_next)
