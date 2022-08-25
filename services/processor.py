from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Set

from ..model.processor_models import KLineData, KLineInterval, ProcessorConfig


class LogicType(Enum):
    HIGH_VOLUME_RAISE: Final[str] = "HIGH_VOLUME_RAISE"


@dataclass(unsafe_hash=True, frozen=True)
class ProcessorId:
    symbol: str
    interval: KLineInterval


class Processor(ABC):
    @abstractmethod
    async def run_logic(self, logic_type: LogicType) -> bool:
        pass

    @abstractmethod
    async def stop_logic(self, logic_type: LogicType) -> bool:
        pass

    @abstractmethod
    async def update_config(self, config: ProcessorConfig) -> None:
        pass

    @abstractmethod
    async def get_config(self) -> ProcessorConfig:
        pass

    @abstractmethod
    async def update_data(self, data: KLineData) -> None:
        pass

    @abstractmethod
    async def get_id(self) -> ProcessorId:
        pass

    @abstractmethod
    async def ger_running_logics(self) -> Set[LogicType]:
        pass
