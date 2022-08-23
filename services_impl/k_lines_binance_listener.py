from __future__ import annotations

import asyncio
from typing import Callable, Coroutine, Dict, List, Set, Type

from ..model.binance_client_models import EventType, KLineData, KLineDataModel
from ..services.binance_client import BinanceClientWebsocketStreamManager
from ..services.k_lines_listener import KLinesListener
from ..services_impl.binance_client_impl import BinanceClientWebsocketStreamManagerImpl
from ..utils.binance_utils import BinanceStreamNameUtil


class KLinesBinanceListener(KLinesListener):
    _binance_client: BinanceClientWebsocketStreamManager
    _listener_callback: Callable[[KLineData], Coroutine[None]]

    def __init__(
        self,
        listener_callback: Callable[[KLineData], Coroutine[None]] = None,
        binance_client: BinanceClientWebsocketStreamManager = None,
    ) -> None:
        self._binance_client = binance_client
        self._listener_callback = listener_callback

    @classmethod
    async def create(
        cls: Type[KLinesBinanceListener],
        listener_callback: Callable[[KLineData], Coroutine[None]],
    ) -> KLinesBinanceListener:

        this = cls(listener_callback)

        binance_client_listener_callbacks: Dict[EventType, KLineDataModel] = {
            EventType.KLINE: this._publish_new_k_line
        }
        binance_client: BinanceClientWebsocketStreamManager = (
            await BinanceClientWebsocketStreamManagerImpl.create(
                binance_client_listener_callbacks
            )
        )
        this._binance_client = binance_client

        return this

    async def _publish_new_k_line(self, data: KLineDataModel) -> None:
        asyncio.create_task(self._listener_callback(data))

    async def start_listening(self, symbols: Set[str] | List[str] = None) -> None:
        await self._binance_client.start()

    async def stop_listening(self, symbols: Set[str] | List[str] = None) -> None:
        await self._binance_client.stop()

    async def add_symbols_to_listen(self, symbols: Set[str] | List[str]) -> None:
        params = [BinanceStreamNameUtil.get_k_line_stream(symbol) for symbol in symbols]
        await self._binance_client.subscribe(params)

    async def remove_symbols_to_listen(self, symbols: Set[str] | List[str]) -> None:
        params = [BinanceStreamNameUtil.get_k_line_stream(symbol) for symbol in symbols]
        await self._binance_client.unsubscribe(params)
