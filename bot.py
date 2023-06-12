from aiogram.utils import executor
from create_bot import dp
from handlers import main_menu, zero_novel, admin_panel
import asyncio
from handlers.events import scheluled
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def on_startup(_):
    print('Бот онлайн')

main_menu.register_handlers_client(dp)
admin_panel.register_handlers_admin(dp)
zero_novel.registre_handlers_client(dp)

#other.registre_handlers_other(dp)
#loop = asyncio.get_event_loop()
#loop.create_task(scheluled(3600*24))

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) #
