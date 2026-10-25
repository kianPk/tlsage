#!/usr/bin/env python3
"""tlsage — show TLS certificate expiry for a host:port."""

from __future__ import annotations

import argparse
import json
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


def status_for(days: float, warn_days: int) -> tuple[str, int]:
    if days < 0:
        return "EXPIRED", 1
    if days <= warn_days:
        return f"WARN (≤ {warn_days} days)", 1
    return "OK", 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="tlsage",
        description="Check how many days remain before a TLS certificate expires.",
    )
    p.add_argument("host", help="hostname (e.g. github.com)")
    p.add_argument("-p", "--port", type=int, default=443)
    p.add_argument(
        "-w",
        "--warn",
        "--warn-days",
        dest="warn_days",
        type=int,
        default=30,
        metavar="N",
        help="exit 1 if certificate expires within N days (default: 30)",
    )
    p.add_argument("-t", "--timeout", type=float, default=8.0)
    p.add_argument("--json", action="store_true", help="print machine-readable JSON")
    p.add_argument("--version", action="version", version="tlsage 1.1.0")
    args = p.parse_args(argv)

    try:
        expires = fetch_not_after(args.host, args.port, args.timeout)
    except Exception as e:
        if args.json:
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    days = (expires - now).total_seconds() / 86400
    status, code = status_for(days, args.warn_days)

    if args.json:
        print(
            json.dumps(
                {
                    "ok": code == 0,
                    "host": args.host,
                    "port": args.port,
                    "expires": expires.isoformat(),
                    "days_remaining": round(days, 2),
                    "warn_days": args.warn_days,
                    "status": status.split()[0] if status.startswith("WARN") else status,
                    "exit_code": code,
                },
                indent=2,
            )
        )
        return code

    print(f"{args.host}:{args.port}")
    print(f"  expires  {expires.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  days     {days:.1f}")
    print(f"  status   {status}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
