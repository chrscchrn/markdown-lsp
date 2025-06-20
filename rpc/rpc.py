import json 
from typing import Any, Dict, Optional, Type
from lsp import message
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BaseMessage:
    jsonrpc: Any
    method: str
    params: Optional[str] = ''
    id: Optional[Any] = ''

def class_to_dict(input: object):
    if not hasattr(input, "__dict__"):
        return input
    result = {}
    for k, v in input.__dict__.items():
        if k.startswith('__'):
            continue
        if hasattr(v, "__dict__"):
            result[k] = class_to_dict(v)
        else:
            result[k] = v
    return result

def encode_message(msg: Type[message.Message]) -> bytes:
    content = json.dumps(class_to_dict(msg))
    return f'Content-Length: {len(content.encode("utf-8"))}\r\n\r\n{content}'.encode('utf-8')

def decode_message(msg: bytes) -> tuple[str, bytes]:
    header, content = msg.split(b'\r\n\r\n')
    _ = int(header[len("Content-Length: "):])
    baseMessage = BaseMessage(**json.loads(content.decode('utf-8')))

    return baseMessage.method, content

# def cut(data: bytes, delimiter: bytes) -> tuple[bytes, bytes, bool]:
#     '''
#     Takes in bytes and a delimiter and returns the two split sections (or empty bytes) and the success as a boolean
#     '''
#     if delimiter not in data:
#         return b'', b'', False
#     [a, b] = data.split(delimiter, 1)
#     return a, b, True
#
# def parseLspHeader(data: bytes) -> tuple[int, int, bool]:
#     '''
#     Returns the total length of the message.
#     '''
#
#     header, content, found = cut(data, b'\r\n\r\n')
#     if not found:
#         return 0, 0, False
#
#     contentLengthBytes = header[len("Content-Length: "):]
#     contentLength = int(contentLengthBytes.decode())
#
#     return len(header), contentLength, True
#
# def split(data: bytes) -> tuple[int, bytes, bool]:
#     '''
#     Split function for deciding whether there was engough data read to parse the LSP message successfully
#     '''
#
#     header, content, found = cut(data, b'\r\n\r\n')
#     if not found:
#         return 0, b'', False
#
#     contentLengthBytes = header[len("Content-Length: "):]
#     contentLength = int(contentLengthBytes.decode())
#
#     if len(content) < contentLength:
#         return 0, b'', False
#
#     totalLength = len(header) + 4 + contentLength
#     return totalLength, data[:totalLength], True
