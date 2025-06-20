import os
import sys
import fcntl
from rpc import rpc
from typing import Optional
import logging
from lsp import initialize, textDocument
from analysis import state as State

logging.basicConfig(filename="log.txt", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

buffer = bytearray()


def read_message():
    while True:
        try:
            chunk = os.read(fd, 1024)
            buffer.extend(chunk)
        except BlockingIOError:
            break


def handle_message(state: State.State):
    method, contents = rpc.decode_message(bytes(buffer))
    logger.info(f'Recieved method: {method}')
    buffer.clear()

    match method:
        case "initialize":
            initializeRequest: initialize.InitializeRequest = initialize.InitializeRequest.from_json(contents)
            logging.info(f'Connected to {initializeRequest.params.clientInfo.name}')
            logging.info(f'Version {initializeRequest.params.clientInfo.version}')
                
            msg = initialize.newInitializeResponse(int(initializeRequest.id))
            reply = rpc.encode_message(msg)
            sys.stdout.buffer.write(reply)
            sys.stdout.buffer.flush()
            logger.info("Sent initialize response.")

        case "textDocument/didOpen":
            didOpenRequest: textDocument.DidOpenTextDocumentNotification = textDocument.DidOpenTextDocumentNotification.from_json(contents)
            State.openDocument(didOpenRequest.params.textDocument.uri, didOpenRequest.params.textDocument.text, state)
            logging.info(f'Opened: {didOpenRequest.params.textDocument.uri}')

        case "textDocument/didChange":
            didChangeRequest: textDocument.DidChangeTextDocumentNotification = textDocument.DidChangeTextDocumentNotification.from_json(contents)
            logger.info(f'Changed file: {didChangeRequest.params.textDocument.uri}')
            logger.info(f'Changes for file: {didChangeRequest.params.contentChanges}')
            for change in didChangeRequest.params.contentChanges:
                State.updateDocument(didChangeRequest.params.textDocument.uri, change.text, state)
            
        case _:
            logging.warn(f"Method '{method}' not handled.")


def shouldExit():
    return False


def main():
    logger.info("----- Start Logger -----")

    state = State.newState()

    while not shouldExit():
        read_message()
        if buffer:
            handle_message(state)

    logger.info("----- End Logger -----")


if __name__ == '__main__':
    main()
