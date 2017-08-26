#!/bin/bash
'''':;exec /usr/bin/env python3 -i "${BASH_SOURCE[0]}" #' '''

def xor(blocks):
    blocks = list(blocks)
    assert all(type(block) is bytes and len(block) == 16 for block in blocks)
    def _xor(blockA, blockB):
        assert type(blockA) is bytes and len(blockA) == 16
        assert type(blockB) is bytes and len(blockB) == 16
        return bytes(a ^ b for a, b in zip(blockA, blockB))
    import functools
    return functools.reduce(_xor, blocks, bytes([0] * 16))

def connect(host, port):
    assert type(host) is str
    assert type(port) is int and 0 <= port < 65536
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((host, port))
    s.recv(8192)
    def request_response(req):
        import base64
        s.send(base64.b64encode(req) + b'\r')
        res = s.recv(8192)
        assert res[-2:] == b'\r\n'
        return base64.b64decode(res[:-2])
    return request_response
