from typing import Dict, List
from lsp import textDocument
from dataclasses_json import dataclass_json
from dataclasses import dataclass

@dataclass_json
@dataclass
class State:
    # map of filenames to contents
    documents: Dict[str, str]
    

def openDocument(uri: str, text: str, state: State):
    state.documents[uri] = text

def updateDocument(uri: str, text: str, state: State):
    state.documents[uri] = text
        

def newState() -> State:
    return State(dict())


