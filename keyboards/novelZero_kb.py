from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

async def createRoller(blockId: int, tetx_to_next) ->  InlineKeyboardMarkup:

    button_next = InlineKeyboardButton(
        f'{tetx_to_next}',
        callback_data=f'ZeroNovelClick'
    )
    button_back = InlineKeyboardButton(
        '---',
        callback_data='world'
    )

    kb_choose_novel = InlineKeyboardMarkup().row(button_next, button_back)

    return kb_choose_novel


async def createChooseRoller(dialog_content) -> InlineKeyboardMarkup:
    kb_choose_novel = InlineKeyboardMarkup()
    for d in dialog_content:
        kb_choose_novel.add(InlineKeyboardButton(f'{d[0]}', callback_data= d[1]))

    return kb_choose_novel