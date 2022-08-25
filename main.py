import sys
from typing import Any

from aiogram import Bot, Dispatcher
from loguru import logger

from config import config

telegram_bot: Bot = None
telegram_dp: Dispatcher = None


def set_up_logger(sink: Any) -> None:
    logger_configuration = {
        "handlers": [{"sink": sink, "format": config.LOGGIN_FORMAT}]
    }
    logger.configure(**logger_configuration)


if __name__ == "__main__":
    set_up_logger(sys.stderr)
    logger.info("Setting up services")

    telegram_bot = Bot(config.TELEGRAM_BOT_TOKEN)
    telegram_dp = Dispatcher(telegram_bot)
