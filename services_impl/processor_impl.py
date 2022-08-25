import asyncio
from collections import defaultdict
from typing import Callable, Coroutine, DefaultDict, Dict, List, Set

from loguru import logger

from ..model.processor_models import KLineData, KLineInterval, ProcessorConfig
from ..services.processor import LogicType, Processor, ProcessorId


class ProcessorImpl(Processor):
    _id: ProcessorId
    _config: ProcessorConfig
    _logics: DefaultDict[LogicType, Callable[[], Coroutine[None]]] = defaultdict(
        lambda: None
    )
    _running_logics: Dict[LogicType, Callable[[], Coroutine[None]]] = dict()

    _max_elements_in_data: int = None

    _data: List[KLineData] = [None]

    def __init__(
        self,
        symbol: str,
        interval: KLineInterval,
        logics_to_run: Set[LogicType] = None,
        config: ProcessorConfig = ProcessorConfig(),
    ) -> None:
        self._id = ProcessorId(symbol, interval)
        self._logics.update({LogicType.HIGH_VOLUME_RAISE: self._high_volume_raise})
        self._config = config
        self._max_elements_in_data = max(
            self._config.high_rise_config.process_intervals
        )

        for logic_type_to_run in set(logics_to_run):
            if self._logics[logic_type_to_run]:
                self._running_logics.add(self._logics[logic_type_to_run])

    async def run_logic(self, logic_type: LogicType) -> bool:
        if not self._logics[logic_type]:
            return False

        if self._running_logics[logic_type]:
            return True

        self._running_logics.add(self._logics[logic_type])

        return True

    async def stop_logic(self, logic_type: LogicType) -> bool:
        if logic_type not in self._running_logics:
            return True

        del self._running_logics[logic_type]

        return True

    async def _high_volume_raise(self) -> None:
        logger.debug("Runnin High Volume Raise logic")

    async def update_data(self, data: KLineData) -> None:
        self._data[-1] = data
        if data.is_kline_closed:
            self._data.append(None)

        if len(self._data) + 1 > self._max_elements_in_data:
            del self._data[0]

        for logic_type, logic in self._running_logics.items():
            asyncio.create_task(logic())

    async def get_id(self) -> ProcessorId:
        return self._id

    async def ger_running_logics(self) -> Set[LogicType]:
        return set(self._running_logics.keys())

    @property.setter
    async def update_config(self, config: ProcessorConfig) -> None:
        self._config = config
        self._max_elements_in_data = max(
            self._config.high_rise_config.process_intervals
        )

    @property.getter
    async def get_config(self) -> ProcessorConfig:
        return self._config
