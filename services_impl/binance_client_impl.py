from __future__ import annotations

import asyncio
import json
from collections import deque
from typing import Callable, Coroutine, Deque, Dict, List, Set, Type

import websockets
from loguru import logger
from websockets.client import WebSocketClientProtocol

from ..model.binance_client_models import (
    EventType,
    KLineDataModel,
    Method,
    RequestModel,
    ResponseModel,
    Utils,
)
from ..services.binance_client import BinanceClientWebsocketStreamManager

CallbackFunctionType = Callable[[KLineDataModel], Coroutine[None]]


class BinanceClientWebsocketStreamManagerImpl(BinanceClientWebsocketStreamManager):
    _max_streams: int
    _max_messages_per_second: int
    _protocol: WebSocketClientProtocol
    _is_listening: bool = False  # Is listining stream
    _callbacks: Dict[
        EventType, CallbackFunctionType
    ]  # Async callbacks to run once message was gotten
    _messages_with_id: dict[int, ResponseModel]
    _listening_task: asyncio.Task
    _messages_sending_task: asyncio.Task
    _subscriptions: List[str]
    _messages_to_send: Deque[RequestModel] = deque()

    def __init__(
        self,
        protocol: WebSocketClientProtocol,
        callbacks: Dict[EventType, CallbackFunctionType] = None,
        max_streams=1024,
        max_messages_per_second=5,
    ) -> None:
        self._callbacks = callbacks | {}
        self._protocol = protocol
        self._max_messages_per_second = max_messages_per_second
        self._max_streams = max_streams

    @classmethod
    async def create(
        cls: Type[BinanceClientWebsocketStreamManagerImpl],
        callbacks: dict[EventType, CallbackFunctionType],
        connection_url: str = "wss://stream.binance.com:9443/ws",
        max_streams: int = 1024,
        max_messages_per_second: int = 5,
    ) -> BinanceClientWebsocketStreamManager:
        protocol = await websockets.connect(connection_url)
        return cls(
            protocol,
            callbacks,
            max_streams=max_streams,
            max_messages_per_second=max_messages_per_second,
        )

    async def _run_listener(self) -> None:
        while self._is_listening:
            raw_message: str = json.loads(await self._protocol.recv())
            if "id" in raw_message:
                self._messages_with_id[raw_message["id"]] = ResponseModel.parse_obj(
                    raw_message
                )
            elif "code" in raw_message:
                logger.error(f"Got error {raw_message}")
            elif "e" in raw_message:
                try:
                    event_type = EventType(raw_message["e"])
                    callback = self._callbacks[event_type]
                    model = (
                        await Utils.get_data_model_by_event_type(event_type)
                    ).parse_obj(raw_message)
                    await asyncio.create_task(callback(model))
                except KeyError:
                    logger.warning(f"No callback for EventType {raw_message['e']}")
            else:
                logger.warning(f"Unexpected message {raw_message}")

    async def start(self) -> None:
        self._is_listening = True
        self._listening_task = await asyncio.create_task(self._run_listener())
        self._messages_sending_task = await asyncio.create_task(
            self._send_messages_from_queue()
        )

    async def stop(self) -> None:
        self._is_listening = False
        self._listening_task.cancel()
        self._messages_sending_task.cancel()
        self._subscriptions.clear()
        self._messages_to_send.clear()
        if not self._protocol.closed():
            await self._protocol.close()

    async def subscribe(self, params: Set[str]) -> List[bool]:
        if not params:
            raise ValueError("params must be not None")

        params = set(params) - self._subscriptions

        if len(params) + self._subscriptions > self._max_streams:
            raise ValueError(
                f"Cannot create more than {self._max_streams}. Currently connected {len(self._subscriptions)} streams"
            )

        tasks: List[asyncio.Task] = list()
        step = 5
        for i in range(0, len(params) - 1 - step, step):
            step_params = params[i : i + step]
            tasks.append(
                asyncio.create_task(
                    self._send_message_with_id(
                        RequestModel(method=Method.SUBSCRIBE, params=step_params)
                    )
                )
            )
        if len(params) % step != 0:
            tasks.append(
                asyncio.create_task(
                    self._send_message_with_id(
                        RequestModel(
                            method=Method.SUBSCRIBE,
                            params=params[len(params) // step * step :],
                        )
                    )
                )
            )

        await asyncio.gather(tasks)
        del tasks

        await self._send_message_with_id(
            RequestModel(method=Method.SUBSCRIBE, params=params)
        )

        self._subscriptions = (
            await (
                self._send_message_with_id(
                    RequestModel(method=Method.LIST_SUBSCRIPTIONS)
                )
            )
        ).result

        return [sub in self._subscriptions for sub in params]

    async def unsubscribe(self, params: Set[str]) -> List[bool]:
        if not params:
            raise ValueError("params must be not None")

        params = set(params) & self._subscriptions

        await self._send_message_with_id(
            RequestModel(method=Method.UNSUBSCRIBE, params=params)
        )

        self._subscriptions = (
            await (
                self._send_message_with_id(
                    RequestModel(method=Method.LIST_SUBSCRIPTIONS)
                )
            )
        ).result

        return [sub not in self._subscriptions for sub in params]

    async def _send_message_with_id(self, message: RequestModel) -> ResponseModel:
        id = message.id

        self._messages_with_id[id] = None

        await self._wait_until_message_exists(id)

        return self._messages_with_id.pop(id)

    async def _wait_until_message_exists(self, message_id: int) -> None:
        while not self._messages_with_id[message_id]:
            await asyncio.sleep(1)

    async def _send_messages_from_queue(self) -> None:
        while True:
            if len(self._messages_to_send) > 0:
                await self._protocol.send(
                    self._messages_to_send.pop().json(exclude_none=True)
                )
            await asyncio.sleep(5)
