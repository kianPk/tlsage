#!/usr/bin/env python3
"""tlsage — show TLS certificate expiry for a host:port."""

from __future__ import annotations

import argparse
import socket
import ssl
import sys
from datetime import datetime, timezone


def fetch_not_after(host: str, port: int, timeout: float) -> datetime:
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
    # 'notAfter': 'Oct 20 12:00:00 2026 GMT'
    return datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(
        tzinfo=timezone.utc
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="tlsage",
        description="Check how many days remain before a TLS certificate expires.",
    )
    p.add_argument("host", help="hostname (e.g. github.com)")
    p.add_argument("-p", "--port", type=int, default=443)
    p.add_argument("-w", "--warn", type=int, default=30, help="warn if days left ≤ N")
    p.add_argument("-t", "--timeout", type=float, default=8.0)
    p.add_argument("--version", action="version", version="tlsage 1.0.0")
    args = p.parse_args(argv)

    try:
        expires = fetch_not_after(args.host, args.port, args.timeout)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    days = (expires - now).total_seconds() / 86400
    print(f"{args.host}:{args.port}")
    print(f"  expires  {expires.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  days     {days:.1f}")

    if days < 0:
        print("  status   EXPIRED")
        return 1
    if days <= args.warn:
        print(f"  status   WARN (≤ {args.warn} days)")
        return 1
    print("  status   OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
