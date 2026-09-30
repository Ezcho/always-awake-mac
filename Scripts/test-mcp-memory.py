#!/usr/bin/env python3
"""Bounded macOS MCP memory regression test; never calls app control tools.

Usage: python3 Scripts/test-mcp-memory.py path/to/pika-mcp [--output report.json]
Only initializes a fresh subprocess and repeatedly requests tools/list. The
default workload detects the Foundation autorelease growth seen in 1.0.7.
"""

import argparse
import ctypes
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import tempfile
import time


class RUsageInfoV0(ctypes.Structure):
    # Darwin <sys/resource.h>, RUSAGE_INFO_V0, including ri_phys_footprint.
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [
        (name, ctypes.c_uint64)
        for name in (
            "user_time", "system_time", "pkg_idle_wkups", "interrupt_wkups",
            "pageins", "wired_size", "resident_size", "phys_footprint",
            "proc_start_abstime", "proc_exit_abstime",
        )
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--requests", type=int, default=20_000)
    parser.add_argument("--warmup", type=int, default=2_000)
    parser.add_argument("--max-growth-mib", type=float, default=12)
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("proc_pid_rusage requires macOS")
    if not 0 < args.warmup < args.requests or args.max_growth_mib <= 0:
        parser.error("require 0 < warmup < requests and a positive growth limit")

    libproc = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    libproc.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    libproc.proc_pid_rusage.restype = ctypes.c_int
    rows = []
    with tempfile.TemporaryFile() as diagnostics:
        process = subprocess.Popen(
            [str(args.binary.resolve())], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=diagnostics, bufsize=0,
        )
        pending = bytearray()

        def request(number, method, params):
            data = json.dumps({
                "jsonrpc": "2.0", "id": number,
                "method": method, "params": params,
            }).encode() + b"\n"
            process.stdin.write(data)
            deadline = time.monotonic() + 10
            while b"\n" not in pending:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not select.select([process.stdout], [], [], remaining)[0]:
                    raise AssertionError(f"MCP response timed out at request {number}")
                chunk = os.read(process.stdout.fileno(), 65536)
                if not chunk:
                    raise AssertionError(f"MCP exited before response {number}")
                pending.extend(chunk)
                if len(pending) > 1024 * 1024:
                    raise AssertionError("Unexpected oversized MCP response")
            line, _, rest = pending.partition(b"\n")
            pending[:] = rest
            reply = json.loads(line)
            assert reply.get("id") == number and "error" not in reply, reply
            if method == "tools/list":
                names = {tool["name"] for tool in reply["result"]["tools"]}
                assert names == {"pika_status", "pika_set_session", "pika_set_monitor"}, names

        def sample(number):
            usage = RUsageInfoV0()
            if libproc.proc_pid_rusage(process.pid, 0, ctypes.byref(usage)):
                raise OSError(ctypes.get_errno(), "proc_pid_rusage failed")
            row = {
                "requests": number, "rss": usage.resident_size,
                "footprint": usage.phys_footprint,
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
            # Bound the test even when run against a known broken binary.
            assert row["footprint"] < 200 * 1024 * 1024, "Memory cap exceeded"

        try:
            request(0, "initialize", {
                "protocolVersion": "2025-11-25", "capabilities": {},
                "clientInfo": {"name": "pika-memory-test", "version": "1"},
            })
            for number in range(1, args.requests + 1):
                request(number, "tools/list", {})
                if number % args.warmup == 0 or number == args.requests:
                    sample(number)
            process.stdin.close()
            assert process.wait(timeout=5) == 0, "MCP failed on clean EOF"
            assert not pending and process.stdout.read() == b"", "Unexpected output at EOF"
            print("clean EOF exit", flush=True)
            growth = max(row["footprint"] for row in rows) - rows[0]["footprint"]
            print(f"Peak footprint growth after warmup: {growth / 1024**2:.2f} MiB")
            assert growth <= args.max_growth_mib * 1024**2, (
                f"Footprint grew {growth / 1024**2:.2f} MiB; "
                f"limit is {args.max_growth_mib:.2f} MiB"
            )
        finally:
            if not process.stdin.closed:
                process.stdin.close()
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            process.stdout.close()
            diagnostics.seek(0)
            diagnostic_text = diagnostics.read().decode(errors="replace")
            if diagnostic_text:
                print(diagnostic_text, file=sys.stderr)
            if args.output:
                args.output.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
