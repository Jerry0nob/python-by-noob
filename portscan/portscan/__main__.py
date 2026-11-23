import argparse
import socket
import sys
import time

from portscan.core import parse_ports, resolve_host, scan, service_name


def port_list(text: str) -> list[int]:
    """argparse type: turns ValueError into a clean usage error."""
    try:
        return parse_ports(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m portscan",
        description="TCP connect port scanner. Scan only hosts you own "
        "or have permission to test.",
    )
    parser.add_argument("host", help="host name or IP address, e.g. 127.0.0.1")
    parser.add_argument(
        "-p",
        "--ports",
        type=port_list,
        default=parse_ports("1-1024"),
        help='ports to scan, e.g. "22,80,8000-8010" (default: 1-1024)',
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=1.0,
        help="seconds to wait for each port (default: 1.0)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="how many ports to check at the same time (default: 100)",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="show closed and filtered ports too, not only open ones",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    if args.workers < 1:
        parser.error("--workers must be at least 1")

    try:
        address = resolve_host(args.host)
    except socket.gaierror as error:
        print(f"error: cannot resolve host {args.host!r} ({error})", file=sys.stderr)
        return 1

    print(f"Scanning {args.host} ({address}), {len(args.ports)} ports...")
    started = time.perf_counter()
    results = scan(address, args.ports, timeout=args.timeout, workers=args.workers)
    elapsed = time.perf_counter() - started

    shown = results if args.all else [r for r in results if r.state == "open"]
    if shown:
        print(f"\n{'PORT':<11}{'STATE':<10}SERVICE")
        for result in shown:
            port = f"{result.port}/tcp"
            print(f"{port:<11}{result.state:<10}{service_name(result.port)}")

    counts = {state: 0 for state in ("open", "closed", "filtered")}
    for result in results:
        counts[result.state] += 1
    print(
        f"\nDone in {elapsed:.2f}s: {counts['open']} open, "
        f"{counts['closed']} closed, {counts['filtered']} filtered."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
