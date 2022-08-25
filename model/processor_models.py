from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Set


class KLineInterval(str, Enum):
    K_LINE_INTERVAL_1_MINUTE: Final[str] = "1m"
    K_LINE_INTERVAL_3_MINUTE: Final[str] = "3m"
    K_LINE_INTERVAL_5_MINUTE: Final[str] = "5m"
    K_LINE_INTERVAL_15_MINUTE: Final[str] = "15m"
    K_LINE_INTERVAL_30_MINUTE: Final[str] = "30m"
    K_LINE_INTERVAL_1_HOUR: Final[str] = "1h"
    K_LINE_INTERVAL_2_HOUR: Final[str] = "2h"
    K_LINE_INTERVAL_4_HOUR: Final[str] = "4h"
    K_LINE_INTERVAL_6_HOUR: Final[str] = "6h"
    K_LINE_INTERVAL_8_HOUR: Final[str] = "8h"
    K_LINE_INTERVAL_12_HOUR: Final[str] = "12h"
    K_LINE_INTERVAL_1_DAY: Final[str] = "1d"
    K_LINE_INTERVAL_3_DAY: Final[str] = "3d"
    K_LINE_INTERVAL_1_WEEK: Final[str] = "1w"
    K_LINE_INTERVAL_1_MONTH: Final[str] = "1M"


@dataclass
class KLineData:
    start_time: int
    symbol: str
    interval: KLineInterval
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    base_volume_asset: float
    is_kline_closed: bool


class HighRiseType(Enum):
    UP: Final[int] = 0
    DOWN: Final[int] = 1
    BOTH: Final[int] = 2


@dataclass
class ProcessorHighRiseConfig:
    process_intervals: Set[int] = {10, 20, 100}
    check_interval: str = "* * * * * */2"
    check_type: HighRiseType = HighRiseType.UP


@dataclass
class ProcessorConfig:
    high_rise_config: ProcessorHighRiseConfig = ProcessorHighRiseConfig()
