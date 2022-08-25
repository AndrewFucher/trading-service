import re
from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import Any, Dict, Final, List, Set

from pydantic import BaseModel, Field, ValidationError, validator


class Method(str, Enum):
    SUBSCRIBE: Final[str] = "SUBSCRIBE"
    UNSUBSCRIBE: Final[str] = "UNSUBSCRIBE"
    SET_PROPERTY: Final[str] = "SET_PROPERTY"
    LIST_SUBSCRIPTIONS: Final[str] = "LIST_SUBSCRIPTIONS"


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


class EventType(str, Enum):
    KLINE: Final[str] = "kline"


class ValidationUtils:
    PARAM_REGEX: Final[re.Pattern[str]] = re.compile(
        f"^.*@(kline_({'|'.join(e.value for e in KLineInterval)}))$"
    )

    METHOD_VALUES: Set[str] = set(e.value for e in Method)


class RequestModel(BaseModel):
    method: Method
    params: Set[str | bool] | None
    id: int = Field(default_factory=lambda: randint(0, 2**64 - 1))

    @validator("params", each_item=True)
    def validate_every_param(cls, param: str | bool) -> str | bool:
        if isinstance(param, str):
            if not ValidationUtils.PARAM_REGEX.match(param):
                raise ValidationError(f"Invalid param pattern for param '{param}'")

        return param

    @validator("params")
    def validate_params(
        cls, params: Set[str | bool] | None, values: dict[str, Any]
    ) -> Set[str | bool]:
        if values["method"] != Method.LIST_SUBSCRIPTIONS and not params:
            raise ValidationError(
                f"Field params for method {values['method']} must be not None"
            )

        if values["method"] == Method.SET_PROPERTY:
            if (
                len(params) != 2
                or not isinstance(params[0], str)
                or not isinstance(params[1], bool)
            ):
                raise ValidationError("Invalid params for method `SET_PROPERTY`")

        if values["method"] in (Method.SUBSCRIBE, Method.UNSUBSCRIBE):
            params = set(params)
            if len(params) > 5:  # Just somewhat random number. TODO: replace maybe
                raise ValidationError(
                    "Cannot Subscribe or Unsubscrive from more than 5 messages per request"
                )

        return params

    @validator("method")
    def validate_method(cls, method: Method | str) -> Method:
        if method not in ValidationUtils.METHOD_VALUES:
            raise ValidationError(f"Invalid method {method}")

        return method


class ResponseModel(BaseModel):
    result: Any
    id: int


class SubscribtionResultModel(BaseModel):
    result: str | None


class ListSubscriptionsResultModel(BaseModel):
    result: Set[str] | None


class BaseDataModel(BaseModel):
    event_type: EventType = Field(alias="e")
    event_time: int = Field(alias="E")
    symbol: str = Field(alias="s")


class KLineData(BaseModel):
    start_time: int = Field(alias="t")
    close_time: int = Field(alias="T")
    symbol: str = Field(alias="s")
    interval: KLineInterval = Field(alias="i")
    first_trade_id: int = Field(alias="f")
    last_trade_id: int = Field(alias="L")
    open_price: float = Field(alias="o")
    close_price: float = Field(alias="c")
    high_price: float = Field(alias="h")
    low_price: float = Field(alias="l")
    base_asset_volume: float = Field(alias="v")
    number_of_trades: int = Field(alias="n")
    is_kline_closed: bool = Field(alias="x")
    quote_asset_volume: float = Field(alias="q")
    taker_buy_base_asset_volume: float = Field(alias="V")
    taker_buy_quote_asset_volume: float = Field(alias="Q")
    # value_to_ignore: float = Field(alias="B")


class KLineDataModel(BaseDataModel):
    data: KLineData = Field(alias="k")


class Utils:
    EVENT_TYPE_TO_DATA_MODEL_DICT: Final[Dict[EventType, BaseDataModel]] = {
        EventType.KLINE: KLineDataModel
    }

    @staticmethod
    async def get_data_model_by_event_type(event_type: EventType) -> BaseDataModel:
        if event_type not in Utils.EVENT_TYPE_TO_DATA_MODEL_DICT:
            return BaseDataModel

        return Utils.EVENT_TYPE_TO_DATA_MODEL_DICT[event_type]
