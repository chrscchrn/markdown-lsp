import collections
from typing import List, Tuple
import unittest
from dataclasses import dataclass

# from rpc.rpc import unpack_messages, decode_message, encode_message
import rpc

@dataclass
class EncodingExample:
    Testing: bool

class TestRPCMethods(unittest.TestCase):

    def test_encode(self):
        expected = "Content-Length: 17\r\n\r\n{\"Testing\": true}".encode('utf-8')
        encoding_example = EncodingExample(True).__dict__
        actual = rpc.encode_message(encoding_example)
        self.assertEqual(actual, expected)

    def test_decode(self):
        incomingMessage = "Content-Length: 55\r\n\r\n{\"jsonrpc\": \"2.0\",\"id\": 1,\"method\": \"hi\", \"params\": {}}".encode('utf-8')
        method, content = rpc.decode_message(incomingMessage)
        contentLength = len(content)
        self.assertEqual(55, contentLength)
        self.assertEqual(method, "hi")

    def test_unpack_messages(self):
        messages = collections.deque()
        buffer = bytearray()
        with open("rpc/test_data/initialize.txt", "r") as m:
            b = m.read().encode("utf-8")
            header_arr = [ord(char) for char in 'Content-Length: 4117\r\n\r\n']
            buffer.extend(header_arr)
            buffer.extend(b)
            buffer.extend(header_arr)
            buffer.extend(b)
        res = rpc.unpack_messages(buffer)
        self.assertEqual(list, type(res))
        self.assertEqual(tuple, type(res[0]))
        self.assertEqual(tuple, type(res[1]))
        self.assertEqual('initialize', res[0][0])
        self.assertEqual('initialize', res[1][0])
        self.assertEqual(2, len(res))

if __name__ == '__main__':
    unittest.main()
