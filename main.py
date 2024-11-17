import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from utils import del_data_play
import config
from handlers import router

bot = Bot(token=config.BOT_TOKEN)


async def start():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    del_data_play()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
