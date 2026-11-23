import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Literal

PortState = Literal["open", "closed", "filtered"]

MIN_PORT = 1
MAX_PORT = 65535


@dataclass(frozen=True)
class PortResult:
    port: int
    state: PortState


def check_port(host: str, port: int, timeout: float = 1.0) -> PortState:
    """Check a single TCP port with a full TCP handshake (connect scan).

    Returns:
        "open"     - the handshake succeeded (SYN-ACK)
        "closed"   - the host answered with RST
        "filtered" - no answer within `timeout` or another network error

    Raises:
        socket.gaierror: if `host` cannot be resolved to an IP address.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "open"
    except ConnectionRefusedError:
        return "closed"
    except TimeoutError:
        return "filtered"
    except socket.gaierror:
        # An unknown host breaks the whole scan, not a single port,
        # so the caller decides what to do instead of getting a port state.
        raise
    except OSError:
        # e.g. "No route to host": the port itself never answered,
        # so "filtered" is the most honest state we can report.
        return "filtered"


def parse_ports(spec: str) -> list[int]:
    """Turn a port list like "22,80,8000-8010" into a sorted list of ports.

    Duplicates are removed. Raises ValueError for anything that is not
    a port number from 1 to 65535 or a valid "start-end" range.
    """
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            raise ValueError(f"empty entry in port list: {spec!r}")
        if "-" in part:
            start_text, _, end_text = part.partition("-")
            start, end = _to_port(start_text), _to_port(end_text)
            if start > end:
                raise ValueError(f"range start is bigger than end: {part!r}")
            ports.update(range(start, end + 1))
        else:
            ports.add(_to_port(part))
    return sorted(ports)


def _to_port(text: str) -> int:
    text = text.strip()
    if not text.isdigit():
        raise ValueError(f"not a port number: {text!r}")
    port = int(text)
    if not MIN_PORT <= port <= MAX_PORT:
        raise ValueError(f"port out of range {MIN_PORT}-{MAX_PORT}: {port}")
    return port


def resolve_host(host: str) -> str:
    """Return the first IP address of `host` (IPv4 or IPv6).

    Resolving once before the scan means one DNS query instead of one per
    port, and an unknown host fails fast with socket.gaierror.
    """
    infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    return str(infos[0][4][0])


def scan(
    host: str,
    ports: list[int],
    timeout: float = 1.0,
    workers: int = 100,
) -> list[PortResult]:
    """Check many ports at the same time and return results sorted by port.

    Most of a scan is waiting for the network, so threads give a big speedup:
    with 100 workers, 1000 filtered ports take ~10 timeouts instead of 1000.
    """
    address = resolve_host(host)

    def check(port: int) -> PortResult:
        return PortResult(port, check_port(address, port, timeout))

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(check, ports))
    return sorted(results, key=lambda result: result.port)


def service_name(port: int) -> str:
    """Well-known service name for a TCP port (e.g. 22 -> "ssh"), or ""."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return ""
