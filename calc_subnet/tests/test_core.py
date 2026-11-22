import pytest

from calc_subnet.core import subnet_info


def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        subnet_info("10.0.0.0/33")
    with pytest.raises(ValueError):
        subnet_info("999.1.1.1/24")  # Invalid IP address


def test_info_for_slash_24():
    info = subnet_info("192.168.1.0/24")
    assert info.network == "192.168.1.0"
    assert info.broadcast == "192.168.1.255"
    assert info.usable_hosts == 254


def test_info_for_slash_30_point_to_point():
    info = subnet_info("10.0.0.0/30")
    assert info.network == "10.0.0.0"
    assert info.broadcast == "10.0.0.3"
    assert info.usable_hosts == 2


def test_info_for_slash_31():
    info = subnet_info("10.0.0.0/31")
    assert info.network == "10.0.0.0"
    assert info.broadcast == "10.0.0.1"
    assert info.usable_hosts == 2


def test_info_for_slash_32():
    info = subnet_info("10.0.0.0/32")
    assert info.network == "10.0.0.0"
    assert info.broadcast == "10.0.0.0"
    assert info.usable_hosts == 1
