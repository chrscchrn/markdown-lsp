from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any, List, Optional
from lsp import message

@dataclass_json
@dataclass
class TextDocumentItem:
    uri: str
    languageId: str
    version: int
    text: str

# Notification
@dataclass_json
@dataclass
class DidOpenTextDocumentParams:
    textDocument: TextDocumentItem

@dataclass_json
@dataclass
class DidOpenTextDocumentNotification(message.Notification):
    params: DidOpenTextDocumentParams

@dataclass_json
@dataclass
class TextDocumentIdentifier:
    uri: str

@dataclass_json
@dataclass
class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: int

@dataclass_json
@dataclass
class TextDocumentContentChangeEvent:
    text: str

@dataclass_json
@dataclass
class DidChangeTextDocumentParams:
    textDocument: VersionedTextDocumentIdentifier
    contentChanges: List[TextDocumentContentChangeEvent]

@dataclass_json
@dataclass
class DidChangeTextDocumentNotification(message.Notification):
    params: DidChangeTextDocumentParams

@dataclass_json
@dataclass
class Position:
    line: int
    character: int

@dataclass_json
@dataclass
class TextDocumentPositionParams:
    textDocument: TextDocumentIdentifier
    position: Position

@dataclass_json
@dataclass
class WorkDoneProgressParams:
    workDoneToken: Optional[int] | Optional[str] = None

@dataclass_json
@dataclass
class HoverParams(WorkDoneProgressParams, TextDocumentPositionParams):
    _: Optional[Any] = None

@dataclass_json
@dataclass
class HoverRequest(message.Request):
    params: HoverParams

@dataclass_json
@dataclass
class Range:
    start: Position
    end: Position

@dataclass_json
@dataclass
class MarkedStringObject:
    language: str
    value: str

@dataclass_json
@dataclass
class MarkupContent:
    kind: str

@dataclass_json
@dataclass
class Hover:
    contents: str | List[str] | MarkedStringObject | List[MarkedStringObject] | MarkupContent
    range: Optional[Range] = None

@dataclass_json
@dataclass
class HoverResponse(message.Response):
    result: Hover

