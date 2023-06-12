from create_bot import bot, conn
from database.db_tools import position_now, get_user_last_msg, check_priv
from keyboards.kb_events import kb_return
from aiogram import types, Dispatcher


async def delete_last_item(tg_id:int):
    try:
        user = await get_user_last_msg(tg_id, conn)
        await bot.delete_message(tg_id, user)
    except Exception as e:
        print(e)


async def main_admin_panel_wrapper(msg: types.Message):
    await msg.delete()
    if await check_priv(conn,msg.from_user.id) != "admin":
        return 0
    await delete_last_item(msg.from_user.id)
    msg_id = await bot.send_message(msg.from_user.id,"Админ меню", reply_markup= await kb_return())
    await position_now(conn, msg.from_user.id, msg_id.message_id)


async def all_about_customers(call: types.CallbackQuery):
    """
    Фармирует статистику по всем пользователям что зарегистрировались в боте
    :param call:
    """

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(main_admin_panel_wrapper, commands=["admin"])