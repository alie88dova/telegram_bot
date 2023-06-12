from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


async def first_enterkb() -> InlineKeyboardMarkup:

    kb = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton(f"Идем дальше", callback_data="first_enter_1")
    return kb.row(button_next)


async def first_enterkb2() -> InlineKeyboardMarkup:

    kb = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton(f"Идем дальше", callback_data="first_enter_2")
    return kb.row(button_next)


async def first_enterkb3() -> InlineKeyboardMarkup:

    kb = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton(f"Идем дальше", callback_data="menu_first")
    return kb.row(button_next)


async def menu_kb():
    button_news = InlineKeyboardButton('Новости',
                                       url='https://t.me/duonzo_news')
    button_contacts = InlineKeyboardButton('Контакты',
                                           callback_data='contacts')
    button_world = InlineKeyboardButton("Мир",
                                        callback_data="world")
    kb_start = InlineKeyboardMarkup().row(button_world, button_news, button_contacts)
    return kb_start


async def menu_first_kb():
    button_news = InlineKeyboardButton('Новости',
                                       url='https://t.me/duonzo_news')
    button_contacts = InlineKeyboardButton('Контакты',
                                           callback_data='contacts')
    button_world1 = InlineKeyboardButton("Мир",
                                         callback_data="world")
    kb_start_first = InlineKeyboardMarkup().row(button_world1, button_news, button_contacts)

    return kb_start_first

#TODO переделается на что нормальное после релиза
async def novel_menu_kb():
    button_select = InlineKeyboardButton(
        'Вход',
        callback_data='ZeroNovelStart'
    )
    button_back = InlineKeyboardButton(
        '---',
        callback_data='menu'
    )

    kb_choose_novel = InlineKeyboardMarkup().row(button_select, button_back)

    return kb_choose_novel