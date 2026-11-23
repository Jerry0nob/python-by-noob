import socket

import pytest


@pytest.fixture
def open_port():
    """A port on 127.0.0.1 that accepts TCP connections during the test."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))  # 0 = let the OS pick a free port
        server.listen()
        yield server.getsockname()[1]


@pytest.fixture
def closed_port():
    """A port on 127.0.0.1 that nobody listens on, so it answers with RST."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return port


@pytest.fixture
def unknown_host(monkeypatch):
    """Make every DNS lookup fail, without asking a real DNS server."""

    def fail(*args, **kwargs):
        raise socket.gaierror(socket.EAI_NONAME, "Name or service not known")

    monkeypatch.setattr(socket, "getaddrinfo", fail)
    monkeypatch.setattr(socket, "create_connection", fail)
