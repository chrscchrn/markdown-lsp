import unittest
import rpc
from dataclasses import dataclass

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
        incomingMessage = "Content-Length: 30\r\n\r\n{\"method\": \"hi\", \"params\": {}}".encode('utf-8')
        method, content = rpc.decode_message(incomingMessage)
        contentLength = len(content)
        self.assertEqual(30, contentLength)
        self.assertEqual(method, "hi")


if __name__ == '__main__':
    unittest.main()
