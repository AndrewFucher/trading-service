from __future__ import annotations

from typing import Final


class BinanceStreamNameUtil:
    K_LINE_INTERVALS: Final[tuple[str]] = (
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    )

    @classmethod
    def get_k_line_stream(cls, symbol: str, interval: str) -> str:
        if interval not in cls.K_LINE_INTERVALS:
            raise ValueError(
                f"Invalid interval {interval} that does not equal to any of {cls.K_LINE_INTERVALS}"
            )

        return f"{symbol}@kline_{interval}"
