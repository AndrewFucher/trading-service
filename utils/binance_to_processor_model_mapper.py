import asyncio

from ..model.binance_client_models import EventType, KLineData
from ..model.binance_client_models import KLineDataModel as BinanceKLineData
from ..model.binance_client_models import KLineInterval
from ..model.processor_models import KLineData as ProcessorKLineData
from ..model.processor_models import KLineInterval as ProcessorKLineInterval


def binance_to_processor_kline_data(data: BinanceKLineData) -> ProcessorKLineData:
    return ProcessorKLineData(
        data.data.start_time,
        data.data.symbol,
        ProcessorKLineInterval(data.data.interval.value),
        data.data.open_price,
        data.data.close_price,
        data.data.high_price,
        data.data.low_price,
        data.data.base_asset_volume,
        data.data.is_kline_closed,
    )


# Small check that everything works fine
# if __name__ == "__main__":
#     a = BinanceKLineData(
#         e=EventType.KLINE,
#         E=123,
#         s="asd",
#         k=KLineData(
#             t=100,
#             T=1111,
#             s="123",
#             i=KLineInterval("1m"),
#             f=100,
#             L=100,
#             o=123.3,
#             c=1234.5,
#             h=123,
#             l=123,
#             v=123,
#             n=100,
#             x=True,
#             q=1233,
#             V=1233,
#             Q=1233,
#         ),
#     )
#     asyncio.run(binance_to_processor_kline_data(a))
#     print("asd")
