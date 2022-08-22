from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Set


class BinanceClientWebsocketStreamManager(ABC):
    @abstractmethod
    async def _run_listener(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def subscribe(self, params: Set[str]) -> List[bool]:
        raise NotImplementedError()

    @abstractmethod
    async def unsubscribe(self, params: Set[str]) -> List[bool]:
        raise NotImplementedError()
