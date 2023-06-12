import datetime
import sqlite3
from create_bot import bot, conn
from aiogram import types, Dispatcher
from database.db_tools import give_novels, novel_count, give_chapter,give_block, position_now
from keyboards.kb_novel import create_roller_novel_kb, create_roller_chapter_kb, create_roller_blocks_kb, kb_blocks_end


async def start_select_section_first(call: types.CallbackQuery):

    await call.message.delete()
    x = 1
    kb = await create_roller_novel_kb(x)

    novel = await give_novels(conn, x)
    text = f"Внимание. Справочное сообщение. Главы не имеют ручного сохранения, сохранение происходит автоматически.Вы не сможете переиграть выбор или вернуться обратно к пройденной части. Модели секций подготовят вас к содержанию главы\n"
    await send_content(
        call,
        text + novel["desc"],
        novel["content_type"],
        novel["content_id"],
        kb
    )


async def start_select_section(call: types.CallbackQuery):

    await call.message.delete()

    x = 3
    kb = await create_roller_novel_kb(x)
    novel = await give_novels(conn, x)
    await send_content(
        call,
        novel["desc"],
        novel["content_type"],
        novel["content_id"],
        kb
    )

#TODO Надо переделать if not ибо я думаю он ебанет
async def roller_novel(call: types.CallbackQuery):

    await call.message.delete()
    index = int(call.data.split()[1])


    try:
        novel_c = await novel_count(conn)
        novel = await give_novels(conn, index)
        print(f"novel_c={novel_c}\n"
              f"ibdex = {index}\n"
              f"novel={novel}")
        if not novel:
            if index == 0:

                index = novel_c

                kb = await create_roller_novel_kb(index)
            elif index > novel_c:
                index = 1
                kb = await create_roller_novel_kb(index)
            novel = await give_novels(conn, index)
            print(f"novel_c={novel_c}\n"
                  f"ibdex = {index}\n"
                  f"novel={novel}")
            await send_content(
                call,
                novel["desc"],
                novel["content_type"],
                novel["content_id"],
                kb
            )
            return
        kb = await create_roller_novel_kb(index)
        await send_content(
            call,
            novel["desc"],
            novel["content_type"],
            novel["content_id"],
            kb
        )
    except Exception as e:
        print(e, " ERRRO")


async def start_select_chapter(call: types.CallbackQuery):

    await call.message.delete()
    i_novel = int(call.data.split()[1])
    i_chapter = 1

    chapter = await give_chapter(conn, i_novel, i_chapter)

    kb = await create_roller_chapter_kb(i_novel, i_chapter, chapter["id"])
    await send_content(
        call,
        chapter["desc"],
        chapter["content_type"],
        chapter["content_id"],
        kb
    )

#TODO Надо переделать if ибо я думаю он ебанет
async def roller_chapter(call: types.CallbackQuery):

    await call.message.delete()
    i_novel = int(call.data.split()[1])
    i_chapter = int(call.data.split()[2])

    try:
        chapter = await give_chapter(conn, i_novel, i_chapter)


        print(f"chapter_c={chapter['chapter_count']}\n"
              f"i_nveol = {i_novel}\n"
              f"i_chapter={i_chapter}\n"
              f"chapter={chapter}")
        if i_chapter == 0:
            i_chapter = chapter['chapter_count']
            chapter = await give_chapter(conn, i_novel, i_chapter)
            kb = await create_roller_chapter_kb(i_novel, i_chapter, chapter['id'])

        elif i_chapter > chapter['chapter_count']:
            i_chapter = 1
            chapter = await give_chapter(conn, i_novel, i_chapter)
            kb = await create_roller_chapter_kb(i_novel, i_chapter, chapter['id'])
        else:
            kb = await create_roller_chapter_kb(i_novel, i_chapter, chapter['id'])
        print(f"chapter_c={chapter['chapter_count']}\n"
              f"i_nveol = {i_novel}\n"
              f"i_chapter={i_chapter}\n"
              f"chapter={chapter}")
        await send_content(
            call,
            chapter["desc"],
            chapter["content_type"],
            chapter["content_id"],
            kb
        )


    except Exception as e:
        print(e, " ERROR")


async def start_select_block(call: types.CallbackQuery):

    await call.message.delete()
    i_novel = int(call.data.split()[1])
    i_chapter = int(call.data.split()[2])
    id_chapter = int(call.data.split()[3])
    i_block = 1

    block = await give_block(conn, i_novel, id_chapter, i_block)

    kb = await create_roller_blocks_kb(i_novel, i_chapter, id_chapter, i_block)
    await send_content(
        call,
        block["desc"],
        block["content_type"],
        block["content_id"],
        kb
    )


async def roller_block(call: types.CallbackQuery):

    await call.message.delete()
    i_novel = int(call.data.split()[1])
    i_chapter = int(call.data.split()[2])
    id_chapter = int(call.data.split()[3])
    i_block = int(call.data.split()[4])

    block = await give_block(conn, i_novel, id_chapter, i_block)

    if i_block > block["blocks_count"]:
        kb = await kb_blocks_end(i_novel, i_chapter)
        text = "Блок завершен"
        type_c = "TXT"
        c_id = None
    else:
        kb = await create_roller_blocks_kb(i_novel,i_chapter, id_chapter, i_block)
        text = block["desc"]
        type_c = block["content_type"]
        c_id = block["content_id"]

    await send_content(
        call,
        text,
        type_c,
        c_id,
        kb
    )

async def send_content(call:types.CallbackQuery, content: str, type_content: str, content_id: str, kb):
    """Функция формирующая сообшение Забавный факт она полезнее чем чел который ее написал"""
    if type_content == "TXT":
        call_id = await bot.send_message(
            call.from_user.id,
            f"{content}",
            reply_markup=kb
        )
    elif type_content == "GIF":
        call_id = await bot.send_animation(
            call.from_user.id,
            animation=f"{content_id}",
            caption=f"{content}",
            reply_markup=kb
        )
    elif type_content == "PIC":
        call_id = await bot.send_photo(
            call.from_user.id,
            photo=f"{content_id}",
            caption=f"{content}",
            reply_markup=kb
        )
    elif type_content == "VIDEO":
        call_id = await bot.send_video(
            call.from_user.id,
            video=f"{content_id}",
            caption=f"{content}",
            reply_markup=kb
        )
    elif type_content == "AUDIO":
        call_id = await bot.send_audio(
            call.from_user.id,
            audio=f"{content_id}",
            caption=f"{content}",
            reply_markup=kb
        )
    await position_now(conn, call.from_user.id, call_id.message_id)

def registre_handlers_client(dp: Dispatcher):
    #Функции с входом в выбор novel
    dp.register_callback_query_handler(start_select_section_first, text="world_first")
    dp.register_callback_query_handler(start_select_section, text="world")

    #Управления ввыводом описания новеллы
    dp.register_callback_query_handler(roller_novel, lambda x: x.data and x.data.startswith('novel '))
    #Возврат из сhapter в novel

    #Вход в выбор выбор chapter
    dp.register_callback_query_handler(start_select_chapter,lambda x: x.data and x.data.startswith('schapter '))

    #Управление в chapter
    dp.register_callback_query_handler(roller_chapter,lambda x: x.data and x.data.startswith('chapter ') )

    #Старт block
    dp.register_callback_query_handler(start_select_block, lambda x: x.data and x.data.startswith('sblock '))

    #Управление в block
    dp.register_callback_query_handler(roller_block, lambda x: x.data and x.data.startswith('block '))




