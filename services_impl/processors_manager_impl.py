import asyncio
from dataclasses import dataclass
from typing import Dict, Set, Tuple

from ..model.processor_models import KLineInterval, ProcessorConfig
from ..services.processor import LogicType, Processor, ProcessorId
from ..services.processors_manager import ProcessorsManager
from ..services_impl.processor_impl import ProcessorImpl


class ProcessorsManagerImpl(ProcessorsManager):
    _processors: Dict[ProcessorId, Processor]

    async def add_processor(self, processor: Processor) -> None:
        id = await processor.get_id()
        if id not in self._processors:
            self._processors[id] = processor

    async def create_processor(
        self,
        symbol: str,
        interval: KLineInterval,
        logics_to_run: Set[LogicType] = None,
        config: ProcessorConfig = ProcessorConfig(),
    ) -> None:
        processor = ProcessorImpl(symbol, interval, logics_to_run, config)

        await self.add_processor(processor)

    async def add_logic(self, logic_type: LogicType, processor_id: ProcessorId) -> None:
        if processor_id:
            await self._processors[processor_id].run_logic(logic_type)
            return

        for id, processor in self._processors.items():
            await asyncio.create_task(processor.run_logic(logic_type))

    async def remove_logic(
        self, logic_type: LogicType, processor_id: ProcessorId
    ) -> None:
        if processor_id:
            await self._processors[processor_id].stop_logic(logic_type)
            return

        for id, processor in self._processors.items():
            await asyncio.create_task(processor.stop_logic(logic_type))
