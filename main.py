import structlog
import logging
import os
from aiogram import Bot, Dispatcher
from config import load_config
import asyncio
from bot.handlers import register_handlers

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(message)s")
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

def main():
    config = load_config()
    bot = Bot(token=config.token)
    dp = Dispatcher()
    asyncio.run(_run(dp, bot))

def _register(dp):
    asyncio.run(register_handlers(dp))

def _run(dp, bot):
    _register(dp)
    logger.info("bot_start")
    dp.run_polling(bot)

if __name__ == "__main__":
    main()
