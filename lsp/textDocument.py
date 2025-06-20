from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
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
