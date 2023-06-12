import asyncio
import sqlite3
from aiogram.utils.exceptions import ChatNotFound
from create_bot import bot, conn
from aiogram import types, Dispatcher
from database.db_tools import get_user, position_now
from keyboards.kb_events import kb_return


async def test_timer():
    users = await get_user(conn)
    for user in users:
        print(user[1])
        try:
            await bot.delete_message(user[1], user[3])
        except Exception as e:
            print(e)
        text = "Привет! Мы добрались до апдейта, а это значит следующие:\n" \
               "Вам необходимо удалить сообщения выше и нажать на кнопку вернуться.\n" \
               "Это первый из запланированных апдейтов.\n\n" \
               "Раз в сутки бот будет присылать сообщение, которое необходимо для его стабильной и корректной работы.\n" \
               "Для перехода в основной меню нажмите на кнопку вернуться."

        try:
            call_id = await bot.send_message(user[1], text, reply_markup=await kb_return(), disable_notification=True)
            await position_now(conn, user[1], call_id.message_id)
        except ChatNotFound:
            print("Данный юзер не подключался к боту")
        except Exception as e:
            print(e)

#Вызывается каждый день
async def scheluled(wait_for):
    while True:
        await test_timer()
        await asyncio.sleep(wait_for)

def registre_handlers_client(dp: Dispatcher):
    pass

