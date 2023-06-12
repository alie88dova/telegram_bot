import datetime
import sqlite3
from create_bot import bot, conn, PAY_TOKEN, dp, PRICE
from aiogram import types, Dispatcher
from aiogram.types import ContentType

from database.db_customize_tools import get_menu_name, update_menu_name, get_screen, update_screen, get_menu_screen
from database.db_tools import register, position_now, check_sub, check_cor_activate, get_user_last_msg, get_sub_type, \
    check_type_sub, update_type_sub
from keyboards.kb_customize import kb_lux_customize, kb_screen_roller
from keyboards.kb_mainmenu import first_enterkb, first_enterkb2, menu_first_kb, menu_kb, novel_menu_kb, first_enterkb3
from keyboards.kb_events import kb_return
from env_const import contact_text
from random import randint
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def scan_message(msg: types.Message):
    print(msg.photo)


async def enter_banner(msg: types.Message):
    """/Start message handler"""
    try:
        await msg.delete()

        if await register(conn, msg.from_user.id) == "reg":
            return 0

        msg_id = await bot.send_message(
            msg.from_user.id,
            text="""Здравствуй, Дорогой читатель.\n<b>Данный бот - ядро Обыденности.</b>""",
            reply_markup=await first_enterkb(),
            parse_mode="html",
        )
        await position_now(conn, msg.from_user.id, msg_id.message_id)

    except sqlite3.OperationalError as e:
        print(e)
    except Exception as e:
        #Заменить на logging
        print(e)


async def enter_banner2(call: types.CallbackQuery):

    await call.message.delete()
    call_id = await bot.send_message(
        call.from_user.id,
        """<b>Взаимодействия внутри мира напрямую зависят от Вас.</b>""",
        reply_markup=await first_enterkb2(),
        parse_mode="html"
    )
    await position_now(conn, call.from_user.id, call_id.message_id)


async def enter_banner3(call: types.CallbackQuery):
    await call.message.delete()
    call_id = await bot.send_message(
        call.from_user.id,
        """<b>До встречи в следующем одноразовом сообщении.</b>""",
        reply_markup=await first_enterkb3(),
        parse_mode="html"
    )
    await position_now(conn, call.from_user.id, call_id.message_id)


async def menu_first(call: types.CallbackQuery):

    await call.message.delete()

    call_id = await bot.send_animation(
        call.from_user.id,
        animation="CgACAgIAAxkBAANKZBBoz2ytV2S7A33ZUXCwjfyYCQYAAogpAAIUKIhIYFKFDU1T_N0vBA",
        caption="Text для first menu",
        reply_markup= await menu_first_kb()
    )
    await position_now(conn, call.from_user.id, call_id.message_id)


async def event_giver(msg:types.Message):
    await delete_last_item(msg.from_user.id)
    await msg.delete()
    msg_id=await bot.send_message(
        msg.from_user.id,
        f"На данный момент у нас нет ресурсов для проведения офлайн событий.\n"
        f"Вы можете поддержать нас:\n"
        f"Оформив подписку на <a href='https://boosty.to/3.03wave'>бусти</a>\n"
        f"Оформив подписку на <a href='https://t.me/FabulatorBot'> Бота</a>\n"
        f"Добровольным <a href='https://www.tinkoff.ru/cf/5TA2trKYm2b'>пожертвованием на благо проекта.</a>",
        reply_markup=await kb_return(),
        parse_mode="html"
        )
    await position_now(conn, msg.from_user.id, msg_id.message_id)


async def buy_message(msg:types.Message):
    await msg.delete()
    await delete_last_item(msg.from_user.id)
    msg_id = await bot.send_message(
        msg.from_user.id,
        f"Единоразовая подписка на бота 300 р.\n"
        f"Оплатив ее один раз Вы получите доступ ко всему контенту, который будет обновляться\n"
        f'Ознакомиться с правилами и условиями покупки единоразовой подписки "здесь"\n\n'
        f'Для получения подписки необходимо перевести деньги на <a href="https://www.tinkoff.ru/cf/5TA2trKYm2b">счет</a>, отравить чек или скриншот перевода <a href="https://t.me/fm_303">нам</a> и получить уникальный одноразовый код активации.'
        ,reply_markup=await kb_return(),
        parse_mode="html"
    )
    await position_now(conn, msg.from_user.id, msg_id.message_id)


async def test_buy(msg:types.Message):
    await delete_last_item(msg.from_user.id)
    if await check_type_sub(conn, msg.from_user.id) != "unsub":
        return 0
    await msg.delete()
    msg_id = await bot.send_invoice(msg.from_user.id,
                           title="Оплата подписки на бота",
                           description='ОПИСАНИЕ !!!',
                           provider_token=PAY_TOKEN,
                           currency='rub',
                           photo_url=None,
                           photo_height=512,  # !=0/None, иначе изображение не покажется
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICE],
                           start_parameter='podpiska-na-bota-test',
                           payload=f'{msg.from_user.id}'
                           )

    await position_now(conn, msg.from_user.id, msg_id.message_id)


#TODO Отключить test_buy тк у нас нет рабочей кассы
#@dp.pre_checkout_query_handler(lambda query: True)
#async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    #await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def help_message(msg:types.Message):
    await delete_last_item(msg.from_user.id)
    await msg.delete()
    msg_id = await bot.send_message(
        msg.from_user.id,
        f"Данная команда будет обновляться по мере развития проекта. \n"
        f"Сейчас тут пусто)))",
        reply_markup=await kb_return(),
        parse_mode="html"
    )
    await position_now(conn, msg.from_user.id, msg_id.message_id)


#TODO Отключить эту штуку тк у нас нет касссы
#@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
#async def process_successful_payment(message: types.Message):
    #print('successful_payment:')

    #pmnt = message.successful_payment.to_python()
    #print(pmnt)
    #await update_type_sub(conn, message.from_user.id)
    #msg_id = await bot.send_message(
        #message.from_user.id,
        #f"Уважаемый читатель, спасибо что оплатили подписку на нашего бота",
        #reply_markup=await kb_return()
    #)

    #await position_now(conn, message.from_user.id, msg_id.message_id)


async def delete_last_item(tg_id:int):
    try:
        user = await get_user_last_msg(tg_id, conn)
        await bot.delete_message(tg_id, user)
    except Exception as e:
        print(e)


#TODO доработать wrapper 1.Добавить фон
async def menu_wrapper(call: types.CallbackQuery):
    #Функция формирует основное меню пользователя
    user_sub = await check_sub(call.from_user.id, conn)
    #Часть 1 из таблицы menu_text, функцией для выбора данной секции текста для пользователя
    mt1 = await create_main_text()

    #Часть 2 Обращение к пользователю
    mt2 = await create_contacting_text(call.from_user.id)

    #Часть 3 текущая версия подписки
    mt3 = f"Текущий статус подписки пользователя - {user_sub} \n"
    mt31 = f"Сменить статус подписки - /buy"
    if user_sub != "unsub":
        mt31 = ""
    #Часть 4 События в мире
    mt4 = f"Состояние мира - Мир сокрыт пеленой\n"

    mt5 = f"Ближайшее событие мир - /event\n" \
          f"Кастомизация интерфейса - /customize\n" \
          f"Помощь - /help"

    #Часть 5 Статистика и ПРОГРЕСс
    #TODO Возможен рефактор в версию с этой частью на отдельной функции

    mt6 = await get_menu_screen(call.from_user.id, conn)

    if mt6 != 0:
        return await bot.send_photo(
            call.from_user.id,
            photo=mt6,
            caption=f"{mt1}\n"
            f"{mt2}\n"
            f"{mt3}\n"
            f"{mt31}\n"
            f"{mt4}\n"
            f"{mt5}\n",
            reply_markup=await menu_kb()
        )
    return await bot.send_message(
        call.from_user.id,
        f"{mt1}\n"
        f"{mt2}\n"
        f"{mt3}\n"
        f"{mt4}\n"
        f"{mt5}\n",
        reply_markup=await menu_kb()
    )


async def create_main_text():

    """Cоздает текст для части 1"""
    x = randint(0,19)
    return contact_text[x]


async def create_contacting_text(tg_id):

    """Создает сообщение с обращением к пользователю выбирая текст
     в осноном делая выбор относительно заданного пользователем параметра

     Для этого используется таблица users_contacting_attemtion
     """
    return f"Здравствуй, {await get_menu_name(tg_id, conn)}.\n"


async def menu(call: types.CallbackQuery):

    await call.message.delete()
    try:
        call_id = await menu_wrapper(call)
        await position_now(conn, call.from_user.id, call_id.message_id)
    except Exception as e:
        print(e)


async def contacts(call: types.CallbackQuery):

    await call.message.delete()
    msg_id = await bot.send_message(
        call.from_user.id,
        text=f"Мы хотим максимально упростить процесс взаимодействия, ниже представлены все варианты связи с Нами. Спасибо за обратную связь и поддержку!\n\n\n"
             f"<em>Контактная информация</em>\n"#italic
             f"Наш основной <a href='https://t.me/duonzo'>канал</a>\n"#url
             f"Наш новостной <a href='https://t.me/duonzo_news'>канал</a>\n"#url
             f"Написать нам в <a href='https://t.me/fm_303'>телеграмм</a>\n"#url
             f"Написать нам на <a href='http://3.03wave@gmail.com/'>почту</a>\n"#url
             f"Наш бусти <a href='https://boosty.to/3.03wave'>аккаунт</a>\n",#url
        reply_markup= await kb_return(),
        parse_mode="html"
    )
    await position_now(conn, call.from_user.id, msg_id.message_id)


async def add_purchase(msg: types.Message):
    await delete_last_item(msg.from_user.id)
    await msg.delete()
    if await check_cor_activate(msg.from_user.id, msg.text.upper(), conn):
        call_id = await bot.send_message(msg.from_user.id, "Поздравляем! Ваша подписка активирована. Спасибо за поддержку!", reply_markup=await kb_return())
        await position_now(conn, msg.from_user.id, call_id.message_id)


#Штукт для работы выбра меню
#TODO сейчас эта штука просто выдает нульноввелу
async def wrap_novel_block(call :types.CallbackQuery):

    """Собирает и отправляет сообщение про """
    kb = await novel_menu_kb()
    img_id = None
    call_id = await bot.send_photo(
        call.from_user.id,
        photo = "AgACAgIAAxkBAAIC7mREIijgLFOU5Il946ZeG-2hsSl7AAKFyTEby60gSu4RVrvx8RjqAQADAgADcwADLwQ",
        caption = "Здравствуй, Дорогой читатель!\n"
                  "Данная часть проекта является тизером новелл.\n"
                  "Бот и новелла будут обновляться до момента релиза.\n"
                  "Будьте внимательны, ведь вы не сможете изменить свой выбор или перепройти главу.", #NovelName
        reply_markup=kb
    )
    await position_now(conn, call.from_user.id, call_id.message_id)


async def choose_novel(call: types.CallbackQuery):

    await call.message.delete()
    await wrap_novel_block(call)


async def customize(msg: types.Message):
    await delete_last_item(msg.from_user.id)
    await msg.delete()
    type_sub = await get_sub_type(conn, msg.from_user.id)
    type_sub = type_sub[0][0]
    if type_sub == "Предзаказ":
        await customize_lux(msg)
    elif type_sub == "unsub":
        await customize_free(msg)



class ReName(StatesGroup):
    START = State()
    NEW_NAME = State()


async def rename_menu(call : types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await ReName.START.set()
    call_id = await bot.send_message(
        call.from_user.id,
        "Как к вам обращаться? (Пришлите сообщением новое имя",
        reply_markup=await kb_return()
    )
    await position_now(conn, call.from_user.id, call_id.message_id)


async def endReName(msg: types.Message, state: FSMContext):
    await delete_last_item(msg.from_user.id)
    await msg.delete()
    await update_menu_name(msg.from_user.id, msg.text, conn)
    await state.finish()

    call_id = await bot.send_message(msg.from_user.id, "Ваше имя изменено",reply_markup=await kb_return())
    await position_now(conn, msg.from_user.id, call_id.message_id)


async def return_to_customize(call: types.CallbackQuery):
    await call.message.delete()

    type_sub = await get_sub_type(conn, call.from_user.id)
    type_sub = type_sub[0][0]
    if type_sub == "Предзаказ":
        await customize_lux(call)
    elif type_sub == "unsub":
        await customize_free(call)


async def screens_roller(call: types.CallbackQuery):
    await call.message.delete()

    screen_id = int(call.data.split()[1])
    screen_file_id = await get_screen(screen_id, conn) # Получаем file_id фона
    kb = await kb_screen_roller(screen_id, conn)

    await bot.send_photo(
        call.from_user.id,
        photo=screen_file_id,
        caption=f"{screen_id}",
        reply_markup=kb
    )


async def screens_change(call: types.CallbackQuery):
    await call.message.delete()
    #Здесь надо будет сделать штуку которая разделяет data из call
    #И обновляет screen добавляя туда его id
    await update_screen(call.from_user.id,
                        call.data.split()[1],
                        conn
                        )
    call_id = await bot.send_message(call.from_user.id, "Ваш фон изменен", reply_markup=await kb_return())
    await position_now(conn, call.from_user.id, call_id.message_id)

async def customize_free(call):
    call_id = await bot.send_message(call.from_user.id, "Меню кастомизации бесплатное", reply_markup=await kb_return())
    await position_now(conn, call.from_user.id, call_id.message_id)


async def customize_lux(call):
    call_id = await bot.send_message(call.from_user.id, "Меню кастомизации премиум", reply_markup=await kb_lux_customize())
    await position_now(conn, call.from_user.id, call_id.message_id)





def register_handlers_client(dp: Dispatcher):

    dp.register_message_handler(enter_banner, commands=["start"])
    dp.register_message_handler(event_giver, commands=["event"])
    dp.register_message_handler(buy_message, commands=["buy"])
    dp.register_message_handler(help_message, commands=["help"])
    dp.register_callback_query_handler(enter_banner2, text="first_enter_1")
    dp.register_callback_query_handler(enter_banner3, text="first_enter_2")
    dp.register_callback_query_handler(menu, text="menu_first")
    dp.register_callback_query_handler(menu, text="menu")
    dp.register_callback_query_handler(menu, text="return")
    dp.register_callback_query_handler(contacts, text="contacts")
    #
    dp.register_callback_query_handler(choose_novel, text="world")
    #Кастомизация
    dp.register_message_handler(customize, commands=["customize"])
    dp.register_callback_query_handler(rename_menu, text="rename_menu")
    dp.register_message_handler(endReName, state=ReName.START)
    dp.register_callback_query_handler(screens_change, lambda x: x.data and x.data.startswith('screen_choose '))
    dp.register_callback_query_handler(screens_roller, lambda x: x.data and x.data.startswith('screen_roller '))
    dp.register_callback_query_handler(return_to_customize, text="return_customize")
    #Функции связанныые с оплатой
    #dp.register_message_handler(add_purchase, lambda message: len(message.text) == 8)
    #Штука для инициализации картинок, но мб потом сделаю нормально)
    dp.register_message_handler(scan_message, content_types=['any'])