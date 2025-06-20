from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any, List, Optional, Dict


@dataclass_json
@dataclass
class Message:
    jsonrpc: str

@dataclass_json
@dataclass
class Request(Message):
    id: int | str
    method: str
    params: Optional[List] | Optional[Dict]

@dataclass_json
@dataclass
class Response(Message):
    id: int | str | None
    # result: Optional[Any]
    # error: Optional[Any]

@dataclass_json
@dataclass
class Notification(Message):
    method: str
    # params: Optional[List] | Optional[Dict]

