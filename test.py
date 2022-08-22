import asyncio

from binance import AsyncClient, BinanceSocketManager
from binance.streams import ReconnectingWebsocket

# b = AsyncClient()

# bm = BinanceSocketManager(b)


# ss: ReconnectingWebsocket = bm.trade_socket("btcusdt")

# print(sock)

client = AsyncClient()
bm = BinanceSocketManager(client)

sock: ReconnectingWebsocket = bm.multiplex_socket(
    [
        # "XRPUSDT@kline_1m".lower(),
        # "ETHBUSD@kline_1m".lower(),
        # "BTCUSDT@kline_1m".lower(),
        # "ETHUSDT@kline_1m".lower(),
        # "BNBUSDT@kline_1m".lower(),
        "EOSUSDT@kline_1m".lower(),
    ]
)


async def q():

    # start any sockets here, i.e a trade socket
    ts = bm.kline_socket("EOSUSDT")
    # then start receiving messages
    async with sock as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await b.close_connection()


asyncio.run(q())
