
import socket
from typing import Literal

PortState = Literal["open", "closed", "filtered"]


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


if __name__ == "__main__":
    examples = [
        ("127.0.0.1", 8000),
        ("127.0.0.1", 8001),
        ("::1", 8000),
        ("10.255.255.1", 80),
        ("nonexistent.invalid", 80),
    ]
    for host, port in examples:
        try:
            state = check_port(host, port)
        except socket.gaierror as error:
            state = f"cannot resolve host ({error})"
        print(f"{host:<20} {port:>5}  {state}")
