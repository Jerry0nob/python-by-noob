import socket

import pytest

from portscan.core import PortResult, check_port, parse_ports, scan, service_name


def test_check_port_open(open_port):
    assert check_port("127.0.0.1", open_port) == "open"


def test_check_port_closed(closed_port):
    assert check_port("127.0.0.1", closed_port) == "closed"


@pytest.mark.parametrize("error", [TimeoutError(), OSError("No route to host")])
def test_check_port_filtered(monkeypatch, error):
    def no_answer(*args, **kwargs):
        raise error

    monkeypatch.setattr(socket, "create_connection", no_answer)
    assert check_port("10.255.255.1", 80, timeout=0.1) == "filtered"


def test_check_port_unknown_host_raises(unknown_host):
    with pytest.raises(socket.gaierror):
        check_port("nonexistent.invalid", 80)


@pytest.mark.parametrize(
    ("spec", "expected"),
    [
        ("80", [80]),
        ("22,80,443", [22, 80, 443]),
        ("8000-8003", [8000, 8001, 8002, 8003]),
        ("443, 22-23 ,80", [22, 23, 80, 443]),
        ("80,80,79-81", [79, 80, 81]),
        ("1,65535", [1, 65535]),
    ],
)
def test_parse_ports(spec, expected):
    assert parse_ports(spec) == expected


@pytest.mark.parametrize(
    "spec",
    ["", "0", "65536", "http", "-80", "80-", "90-80", "22,,80", "1.5", "-1"],
)
def test_parse_ports_invalid(spec):
    with pytest.raises(ValueError):
        parse_ports(spec)


def test_scan_returns_results_sorted_by_port(open_port, closed_port):
    results = scan("127.0.0.1", [closed_port, open_port], timeout=0.5)
    assert results == sorted(
        [PortResult(open_port, "open"), PortResult(closed_port, "closed")],
        key=lambda result: result.port,
    )


def test_scan_unknown_host_raises(unknown_host):
    with pytest.raises(socket.gaierror):
        scan("nonexistent.invalid", [80])


def test_service_name_unknown_port_is_empty(monkeypatch):
    def not_found(*args):
        raise OSError("port/proto not found")

    monkeypatch.setattr(socket, "getservbyport", not_found)
    assert service_name(65000) == ""
