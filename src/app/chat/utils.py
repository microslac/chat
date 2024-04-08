import base64
from datetime import datetime
from contextlib import suppress
from functools import reduce
from typing import Tuple, Union


def encode_cursor(text: str, default="") -> str:
    if text:
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")
    return default


def decode_cursor(
    cursor: str,
    scheme: str,
    default: str = "",
    delimiter: str = ":",
    raise_exception: bool = True,
    parser: Union[callable, Tuple[callable]] = None,
) -> str:
    with suppress(Exception):
        decoded = base64.b64decode(cursor).decode("utf-8").split(delimiter)
        if len(decoded) == 2 and decoded[0] == scheme:
            if parser is not None:
                parsers = list(parser)
                return reduce(lambda acc, fn: fn(acc), parsers, decoded[1])
            return decoded[1]

    if raise_exception:
        raise Exception("invalid_cursor")
    return default


def to_timestamp(dt, default=0, round_ts=False) -> int | float:
    if isinstance(dt, datetime):
        if round_ts:
            return round(dt.timestamp() * 1e3)
        return dt.timestamp()
    return default
