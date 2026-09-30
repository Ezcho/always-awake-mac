#!/usr/bin/env python3
"""Isolated stdio lifecycle checks; never invokes pika power-control tools."""
import argparse
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys


def read_line(fd):
    data = bytearray()
    while b'\n' not in data:
        assert select.select([fd], [], [], 5)[0], 'MCP response timed out'
        chunk = os.read(fd, 1)
        assert chunk, 'MCP closed before response'
        data.extend(chunk)
    return json.loads(data)


def request(process, number=0):
    process.stdin.write(json.dumps({'jsonrpc':'2.0','id':number,'method':'initialize',
        'params':{'protocolVersion':'2025-11-25','capabilities':{},
        'clientInfo':{'name':'lifecycle-test','version':'1'}}}).encode()+b'\n')
    process.stdin.flush()
    reply = read_line(process.stdout.fileno())
    assert 'result' in reply, reply


def orphan(binary, expect_exit, abrupt=False):
    source_read, source_write = os.pipe()
    reply_read, reply_write = os.pipe()
    launcher = subprocess.Popen([sys.executable, '-c', '''
import os, subprocess, sys
p = subprocess.Popen([sys.argv[1]], stdin=int(sys.argv[2]), stdout=int(sys.argv[3]), stderr=subprocess.DEVNULL)
print(p.pid, flush=True)
sys.stdin.buffer.read(1)
os._exit(0)
''', binary, str(source_read), str(reply_write)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        pass_fds=(source_read, reply_write), start_new_session=True)
    os.close(source_read)
    os.close(reply_write)
    try:
        child = int(launcher.stdout.readline())
        message = {'jsonrpc':'2.0','id':1,'method':'initialize','params':{
            'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'orphan-test','version':'1'}}}
        os.write(source_write, json.dumps(message).encode()+b'\n')
        assert 'result' in read_line(reply_read)
        if abrupt:
            os.write(source_write, b'{\"jsonrpc\":')  # Block inside a partially received frame.
            launcher.kill()
        else:
            launcher.stdin.write(b'x'); launcher.stdin.flush()
        launcher.wait(timeout=5)
        # Keep the inherited stdin writer alive: parent exit must end the server even without EOF.
        ready = select.select([reply_read], [], [], 3)[0]
        ended = bool(ready) and os.read(reply_read, 1) == b''
        assert ended == expect_exit, f'parent exit cleanup: expected {expect_exit}, got {ended}'
        print(('PASS killed-parent/partial-input cleanup' if abrupt else 'PASS parent-exit cleanup') if ended else 'REPRODUCED orphan survives parent exit while inherited stdin stays open')
    finally:
        os.close(source_write)
        os.close(reply_read)
        # This is an isolated process group created solely by this test.
        try: os.killpg(launcher.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        if launcher.poll() is None: launcher.wait(timeout=5)
        launcher.stdin.close(); launcher.stdout.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary', type=Path)
    parser.add_argument('--expect-orphan', action='store_true')
    args = parser.parse_args()
    binary = str(args.binary.resolve())
    clients = []
    try:
        for _ in range(4):
            p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            clients.append(p); request(p)
        assert all(p.poll() is None for p in clients), 'Independent live clients must coexist'
        clients[0].stdin.close(); assert clients[0].wait(timeout=5)==0
        assert all(p.poll() is None for p in clients[1:])
        for p in clients[1:]:
            p.stdin.close(); assert p.wait(timeout=5)==0
        print('PASS four independent clients and per-connection EOF cleanup')
    finally:
        for p in clients:
            if p.poll() is None: p.terminate(); p.wait(timeout=5)
            for stream in (p.stdin,p.stdout,p.stderr): stream.close()
    orphan(binary, not args.expect_orphan)
    orphan(binary, not args.expect_orphan, abrupt=True)


if __name__ == '__main__': main()
