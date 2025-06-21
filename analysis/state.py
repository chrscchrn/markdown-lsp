from typing import Any, Dict, List
from lsp import textDocument
from dataclasses_json import dataclass_json
from dataclasses import dataclass

from lsp import textDocument

@dataclass_json
@dataclass
class State:
    # map of filenames to contents
    documents: Dict[str, str]
    
def newState() -> State:
    return State(dict())

def openDocument(uri: str, text: str, state: State):
    state.documents[uri] = text

def updateDocument(uri: str, text: str, state: State):
    state.documents[uri] = text
        
def hover(state: State, id: Any, uri: str, position: textDocument.Position) -> textDocument.HoverResponse:
    document = state.documents[uri]
    return textDocument.HoverResponse(
        '2.0', 
        id, 
        textDocument.Hover(
            f'{document.split('/')[-1]}:{len(document)}:{position}'
        )
    )


