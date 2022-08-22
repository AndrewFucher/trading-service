from abc import ABC, abstractmethod
from typing import List, Set


class KLinesListener(ABC):
    @abstractmethod
    async def _publish_new_k_line(self) -> None:
        pass

    @abstractmethod
    async def start_listening(self, symbols: List[str] | Set[str] = None) -> None:
        pass

    @abstractmethod
    async def add_symbol_to_listen(self, symbol: str) -> None:
        await self.add_symbols_to_listen([symbol])

    @abstractmethod
    async def remove_symbol_to_listen(self, symbol: str) -> None:
        await self.remove_symbols_to_listen([symbol])

    @abstractmethod
    async def add_symbols_to_listen(self, symbols: List[str]) -> None:
        pass

    @abstractmethod
    async def remove_symbols_to_listen(self, symbols: List[str]) -> None:
        pass

    @abstractmethod
    async def workflow(self) -> None:
        pass
