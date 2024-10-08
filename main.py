from __future__ import annotations

import asyncio
import sys
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher

from handlers import user_handlers, other_handlers
from config_data.config import load_config, Config


formatter = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(filename)s:'
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)


async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))

    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    logger.info('Бот был успешно запущен')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
