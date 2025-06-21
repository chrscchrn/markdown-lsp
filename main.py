import os
import sys
import fcntl
from lsp import message
from rpc import rpc
from typing import IO, BinaryIO, Deque, List, Optional, Type
import logging
from lsp import initialize, textDocument
from analysis import state as State
from collections import deque

logging.basicConfig(filename="log.log", level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

buffer = bytearray()
messages: Deque[tuple[str, bytes]] = deque()

def write_response(msg: message.Message, writer: BinaryIO, method: str):
    encoded_message = rpc.encode_message(msg)
    writer.write(encoded_message)
    writer.flush()
    logger.info(f'Wrote response for: ......... {method}')

def read_message():
    while True:
        try:
            chunk = os.read(fd, 1024)
            buffer.extend(chunk)
        except BlockingIOError:
            break


def handle_message(state: State.State, writer: BinaryIO):
    messages.extend(rpc.unpack_messages(buffer))
    buffer.clear()
    while messages:
        method, contents = messages.popleft()
        logger.info(f'Recieved method: ............ {method}')

        match method:
            case "initialize":
                initializeRequest: initialize.InitializeRequest = initialize.InitializeRequest.from_json(contents)
                logging.info(f'Connected to: ............... {initializeRequest.params.clientInfo.name}')
                logging.info(f'Version ..................... {initializeRequest.params.clientInfo.version}')

                msg = initialize.newInitializeResponse(int(initializeRequest.id))
                write_response(msg, writer, method)

            case "textDocument/didOpen":
                didOpenRequest: textDocument.DidOpenTextDocumentNotification = textDocument.DidOpenTextDocumentNotification.from_json(contents)
                State.openDocument(didOpenRequest.params.textDocument.uri, didOpenRequest.params.textDocument.text, state)
                logging.info(f'Opened: ..................... {didOpenRequest.params.textDocument.uri}')

            case "textDocument/didChange":
                didChangeRequest: textDocument.DidChangeTextDocumentNotification = textDocument.DidChangeTextDocumentNotification.from_json(contents)
                logger.info(f'Changed file: ............... {didChangeRequest.params.textDocument.uri}')
                logger.info(f'Changes for file: ........... {didChangeRequest.params.contentChanges}')
                for change in didChangeRequest.params.contentChanges:
                    State.updateDocument(didChangeRequest.params.textDocument.uri, change.text, state)

            case 'textDocument/hover':
                logger.info(contents)
                hoverRequest: textDocument.HoverRequest = textDocument.HoverRequest.from_json(contents)

                hoverResponse: textDocument.HoverResponse = State.hover(
                    state, hoverRequest.id, 
                    hoverRequest.params.textDocument.uri, 
                    hoverRequest.params.position)

                write_response(hoverResponse, writer, method)

            case 'initialized':
                pass
            case 'shutdown':
                pass
            case _:
                logging.warning(f"Method not handled: ...... {method}")


def shouldExit():
    return False


def main():
    logger.info("----- Start Logger -----")

    state = State.newState()
    writer = sys.stdout.buffer

    while not shouldExit():
        read_message()
        if buffer:
            handle_message(state, writer)

    logger.info("----- End Logger -----")


if __name__ == '__main__':
    main()
