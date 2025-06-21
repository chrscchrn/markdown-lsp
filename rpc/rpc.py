import collections
import json 
from typing import Any, Deque, List, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BaseMessage:
    jsonrpc: Any
    method: str
    params: Optional[str] = ''
    id: Optional[Any] = ''

def unpack_messages(buffer: bytearray) -> List[tuple[str, bytes]]:
    '''
    Handles multiple LSP messages from the buffer parameter then appends the messages as bytes into the bi-di queue parameter. Returns a boolean representing the success.
    '''
    messages = []
    while True:
        header_end = buffer.find(b'\r\n\r\n')
        if header_end == -1:
            break
        print(f'header end: {header_end}\n')

        header = buffer[:header_end].decode("ascii")
        print(f'header: {header}\n')

        content_length = None
        for line in header.split("\r\n"):
            if line.lower().startswith('content-length:'):
                content_length = int(line.split(":")[1].strip())
                break

        if content_length is None:
            raise ValueError("Missing Content-Length header.")
        print(f'content len: {content_length}\n')
        
        total_length = header_end + 4 + content_length
        print(f'total len: {total_length}\n')

        if len(buffer) < total_length:
            raise ValueError("Incomplete body message.")

        body = buffer[header_end + 4:total_length]
        print(f'body: {body}\n')
        messages.append(body)
        # removed processed message from buffer
        del buffer[:total_length+1]
    return [(BaseMessage(**json.loads(m.decode('utf-8'))).method, m) for m in messages]

def class_to_dict(input: object):
    '''
    Recusively transforms class object and children to dictionaries using the __dict__ attribute
    '''
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

def encode_message(msg: object) -> bytes:
    '''
    Takes in a LSP message as class objects and returns the JSON as a string encoded to utf-8 
    '''
    content = json.dumps(class_to_dict(msg))
    return f'Content-Length: {len(content.encode("utf-8"))}\r\n\r\n{content}'.encode('utf-8')

def decode_message(msg: bytes) -> tuple[str, bytes]:
    '''
    Takes in bytes containing a LSP message returning the LSP method and message content (JSON)
    '''
    header, content = msg.split(b'\r\n\r\n')
    _ = int(header[len("Content-Length: "):])
    baseMessage = BaseMessage(**json.loads(content.decode('utf-8')))

    return baseMessage.method, content

