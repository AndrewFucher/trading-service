import os

import dotenv
from loguru import logger

dotenv.load_dotenv()

logger.info("Setting config parameters")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

LOGGIN_FORMAT = os.getenv(
    "LOGGIN_FORMAT",
    (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        " - <level>{message}</level>"
    ),
)
LOGGIN_LEVEL = os.getenv("LOGGIN_LEVEL")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", None)
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", None)
