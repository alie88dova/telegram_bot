import datetime
import sqlite3

from create_bot import bot, conn
from database.db_tools import position_now
from database.tool_novel_0 import getFullBlockFromBlockId, ComeUserToNovelZero, get_user_state, \
    get_user_in_novel_position, update_user_id_block, get_content_to_dialog, update_choose_user
from aiogram import types, Dispatcher

from keyboards.kb_events import kb_return
from keyboards.novelZero_kb import createRoller, createChooseRoller


#Выяснилось что он не нужен
async def enter_novel(msg: types.CallbackQuery):
    try:
        await ComeUserToNovelZero(msg.from_user.id, conn)
    except:
        print(f"Уже зареган {msg.from_user.id}" )
    await next_blocks(msg)

async def next_blocks(msg: types.CallbackQuery) -> None:
    await msg.message.delete()
    try:
        block = await getFullBlockFromBlockId(
            await get_user_in_novel_position(msg.from_user.id,conn),
            await get_user_state(msg.from_user.id,conn),
            conn)
        if block['modify']==1:
            await dialog_block(msg, block)
            return
        if block['modify'] == 2:
            pass
        kb = await createRoller(block["id"], block["button_text"])
        await send_block(block,kb ,msg)
    except Exception as e:
        await end_novel(msg)


#TODO end this shit


async def end_novel(msg:types.CallbackQuery):
    chat_id = await bot.send_photo(msg.from_user.id,
                   photo="AgACAgIAAxkBAAIC7mREIijgLFOU5Il946ZeG-2hsSl7AAKFyTEby60gSu4RVrvx8RjqAQADAgADcwADLwQ",
                   caption="Информацию о ближайшем апдейте можно найти в основном меню бота.\n"
                           "Ваш прогресс был сохранен.\n"
                           "Оформить предзаказ и получить полный доступ ко всему материалу бота - /buy\n",
                   reply_markup=await kb_return()
    )
    await position_now(conn, msg.from_user.id, chat_id.message_id)


async def dialog_block(msg: types.CallbackQuery, block):

    d_cont = await get_content_to_dialog(
        block["blockId"],
        block["stateUserChose"],
        conn
    )
    kb = await createChooseRoller(d_cont)
    print(kb)
    #msg_id = await bot.send_message(msg.from_user.id,"test",reply_markup=kb)
    await send_block(block,kb,msg)


async def send_block(block,kb, msg):

    """Функция для типизированной отправки блоков"""
    if block["blockImageType"] == "TXT":
        call_id = await bot.send_message(
            msg.from_user.id,
            f"{block['blockText']}",
            reply_markup=kb
        )
    elif block["blockImageType"] == "GIF":
        call_id = await bot.send_animation(
            msg.from_user.id,
            animation=f"{block['blockImageIdificatore']}",
            caption=f"{block['blockText']}",
            reply_markup=kb
        )
    elif block["blockImageType"] == "PIC":
        call_id = await bot.send_photo(
            msg.from_user.id,
            photo=f"{block['blockImageIdificatore']}",
            caption=f"{block['blockText']}",
            reply_markup=kb
        )
    elif block["blockImageType"] == "VIDEO":
        call_id = await bot.send_video(
            msg.from_user.id,
            video=f"{block['blockImageIdificatore']}",
            caption=f"{block['blockText']}",
            reply_markup=kb
        )
    elif block["blockImageType"] == "AUDIO":
        call_id = await bot.send_audio(
            msg.from_user.id,
            audio=f"{block['blockImageIdificatore']}",
            caption=f"{block['blockText']}",
            reply_markup=kb
        )


    await position_now(conn, msg.from_user.id, call_id.message_id)


async def user_click(msg: types.CallbackQuery):
    block = await getFullBlockFromBlockId(await get_user_in_novel_position(msg.from_user.id, conn),
                                          await get_user_state(msg.from_user.id, conn), conn)
    await update_user_id_block(msg.from_user.id, block["blockId"] + 1, conn)
    await next_blocks(msg)


async def Choose_0(msg: types.CallbackQuery):
    block = await getFullBlockFromBlockId(
        await get_user_in_novel_position(msg.from_user.id, conn),
        await get_user_state(msg.from_user.id, conn),
        conn)
    await update_user_id_block(msg.from_user.id, block["blockId"] + 1, conn)
    await update_choose_user(msg.from_user.id,1,conn)
    await next_blocks(msg)


async def Choose_1(msg: types.CallbackQuery):
    block = await getFullBlockFromBlockId(
        await get_user_in_novel_position(msg.from_user.id, conn),
        await get_user_state(msg.from_user.id, conn),
        conn)
    await update_user_id_block(msg.from_user.id, block["blockId"] + 1, conn)
    await update_choose_user(msg.from_user.id,2,conn)
    await next_blocks(msg)


async def Choose_2(msg: types.CallbackQuery):
    block = await getFullBlockFromBlockId(
        await get_user_in_novel_position(msg.from_user.id, conn),
        await get_user_state(msg.from_user.id, conn),
        conn)
    await update_user_id_block(msg.from_user.id, block["blockId"] + 1, conn)
    await update_choose_user(msg.from_user.id,3,conn)
    await next_blocks(msg)


async def Choose_3(msg: types.CallbackQuery):
    block = await getFullBlockFromBlockId(
        await get_user_in_novel_position(msg.from_user.id, conn),
        await get_user_state(msg.from_user.id, conn),
        conn)
    await update_user_id_block(msg.from_user.id, block["blockId"] + 1, conn)
    await update_choose_user(msg.from_user.id,4,conn)
    await next_blocks(msg)


async def Choose_4(msg: types.CallbackQuery):
    block = await getFullBlockFromBlockId(
        await get_user_in_novel_position(msg.from_user.id, conn),
        await get_user_state(msg.from_user.id, conn),
        conn)
    await update_user_id_block(msg.from_user.id, block["blockId"] + 1, conn)
    await update_choose_user(msg.from_user.id,5,conn)
    await next_blocks(msg)

def registre_handlers_client(dp: Dispatcher):
    #
    dp.register_callback_query_handler(enter_novel, text='ZeroNovelStart')

    dp.register_callback_query_handler(user_click, text='ZeroNovelClick')

    dp.register_callback_query_handler(Choose_0, text="ZeroNovelChoose0")
    dp.register_callback_query_handler(Choose_1, text="ZeroNovelChoose1")
    dp.register_callback_query_handler(Choose_2, text="ZeroNovelChoose2")
    dp.register_callback_query_handler(Choose_3, text="ZeroNovelChoose3")