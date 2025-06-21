from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional
# this is correct
from lsp import message

@dataclass_json
@dataclass
class ClientInfo:
    name: str
    version: Optional[str] = None

@dataclass_json
@dataclass
class InitializeRequestParams:
    processId: int | None
    clientInfo: ClientInfo
    rootPath: Optional[str] | Optional[None] = None
    locale: Optional[str] = None

@dataclass_json
@dataclass
class InitializeRequest(message.Request):
    params: InitializeRequestParams

@dataclass_json
@dataclass
class ServerInfo:
    name: str
    version: Optional[str] = ''

@dataclass_json
@dataclass
class ServerCapabilities:
    textDocumentSync: int
    hoverProvider: bool

@dataclass_json
@dataclass
class InitializeResult:
    capabilities: ServerCapabilities
    serverInfo: ServerInfo


@dataclass_json
@dataclass
class InitializeResponse(message.Response):
    result: InitializeResult

def newInitializeResponse(id: int) -> InitializeResponse:
    return InitializeResponse(
        "2.0", 
        id, 
        InitializeResult(
            ServerCapabilities(
                textDocumentSync=1, 
                hoverProvider=True,
            ), 
            ServerInfo(
                "python-lsp-chris", 
                "7.2.2-aa"
            )
        )
    )

