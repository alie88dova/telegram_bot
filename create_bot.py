import types

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage #Переделать на рэдис можно позже
from database.db_tools import sql_connection, novel_count
import logging


#memory storage for use states group
storage = MemoryStorage()


bot = Bot(token="TOKEN")


PAY_TOKEN ="PAY_TOKEN"
PRICE = types.LabeledPrice(label='Покупка доступа к новвелам', amount=30000)


#Start dispatcher to use handlers and our storage
dp = Dispatcher(bot, storage=storage)

#Create conection to database
conn = sql_connection()




#System logging to file logs.log
#logging.basicConfig(filename="logs.log", filemode="a")

#event creation
