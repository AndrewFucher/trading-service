from typing import Set

from aiogram import Bot, Dispatcher, filters, types


class TelegramClient:
    _bot: Bot
    _dp: Dispatcher
    _user_id = _user_id

    def __init__(self, bot: Bot, user_id: int) -> None:
        self._bot = bot
        self._dp = Dispatcher(bot)
        self._user_id = user_id
        self._dp.filters_factory.bind(filters.IDFilter(self._user_id))
        self._dp.register_message_handler()

    # async def
