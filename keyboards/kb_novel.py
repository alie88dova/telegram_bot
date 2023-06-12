from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


async def create_roller_novel_kb(novel_index: int) -> InlineKeyboardMarkup:

    """Создает клавиатуру для работы системы перлистывания chapter"""

    kb_section = InlineKeyboardMarkup()
    button_left = InlineKeyboardButton(f'<<', callback_data=f'novel {novel_index - 1}')
    button_middle = InlineKeyboardButton(f'---', callback_data=f'menu')
    button_right = InlineKeyboardButton(f'>>', callback_data=f'novel {novel_index + 1}')
    button_select = InlineKeyboardButton(f'Выбрать', callback_data=f'schapter {novel_index}')
    kb_section.row(button_left, button_middle, button_right).add(button_select)

    return kb_section


async def create_roller_chapter_kb(novel_index, chapter_index, id_chapter) -> InlineKeyboardMarkup:

    """Создает клавиатуру для работы системы перлистывания chapter"""

    kb_section = InlineKeyboardMarkup()
    button_left = InlineKeyboardButton(f'<<', callback_data=f'chapter {novel_index} {chapter_index - 1}')
    button_middle = InlineKeyboardButton(f'---', callback_data=f'novel {novel_index}')
    button_right = InlineKeyboardButton(f'>>', callback_data=f'chapter {novel_index} {chapter_index + 1}')
    button_select = InlineKeyboardButton(f'Выбрать', callback_data=f'sblock {novel_index} {chapter_index} {id_chapter}')
    kb_section.row(button_left, button_middle, button_right).add(button_select)

    return kb_section


async def create_roller_blocks_kb(novel_index , chapter_index, id_chapter,block_index) -> InlineKeyboardMarkup:

    """Создает клавиатуру для работы системы перлистывания chapter"""

    kb_section = InlineKeyboardMarkup()
    button_middle = InlineKeyboardButton(f'---', callback_data=f'chapter {novel_index} {chapter_index}')
    button_right = InlineKeyboardButton(f'>>', callback_data=f'block {novel_index} {chapter_index} {id_chapter} {block_index+1}')
    kb_section.row(button_middle, button_right)

    return kb_section


async def menu_back():

    button_middle = InlineKeyboardButton(f'В меню', callback_data=f'menu')
    kb_section = InlineKeyboardMarkup()
    kb_section.row(button_middle)

    return kb_section


async def kb_blocks_end(novel_index, chapter_index):

    kb_section = InlineKeyboardMarkup()
    button_middle = InlineKeyboardButton(f'Дальше', callback_data=f'chapter {novel_index} {chapter_index+1}')
    kb_section.row(button_middle)

    return kb_section
