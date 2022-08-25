from abc import ABC, abstractmethod
from typing import Set

from ..model.processor_models import KLineInterval, ProcessorConfig
from ..services.processor import LogicType, Processor, ProcessorId


class ProcessorsManager(ABC):
    @abstractmethod
    async def add_processor(self, processor: Processor) -> None:
        pass

    @abstractmethod
    async def create_processor(
        self,
        symbol: str,
        interval: KLineInterval,
        logics_to_run: Set[LogicType] = None,
        config: ProcessorConfig = ProcessorConfig(),
    ) -> None:
        pass

    @abstractmethod
    async def add_logic(self, logic_type: LogicType, processor_id: ProcessorId) -> None:
        pass

    @abstractmethod
    async def remove_logic(
        self, logic_type: LogicType, processor_id: ProcessorId
    ) -> None:
        pass
