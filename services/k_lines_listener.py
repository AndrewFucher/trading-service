from abc import ABC, abstractmethod
from typing import Set


class KLinesListener(ABC):
    @abstractmethod
    async def start_listening(self, symbols: Set[str] = None) -> None:
        pass

    @abstractmethod
    async def stop_listening(self, symbols: Set[str] = None) -> None:
        pass

    async def add_symbol_to_listen(self, symbol: str) -> None:
        await self.add_symbols_to_listen([symbol])

    async def remove_symbol_to_listen(self, symbol: str) -> None:
        await self.remove_symbols_to_listen([symbol])

    @abstractmethod
    async def add_symbols_to_listen(self, symbols: Set[str]) -> None:
        pass

    @abstractmethod
    async def remove_symbols_to_listen(self, symbols: Set[str]) -> None:
        pass
