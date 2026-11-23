import re

import pytest

from portscan.__main__ import main


def test_shows_only_open_ports_by_default(capsys, open_port, closed_port):
    code = main(["127.0.0.1", "-p", f"{open_port},{closed_port}", "-t", "0.5"])
    out = capsys.readouterr().out
    assert code == 0
    assert re.search(rf"^{open_port}/tcp\s+open\b", out, re.MULTILINE)
    assert f"{closed_port}/tcp" not in out
    assert "1 open, 1 closed, 0 filtered" in out


def test_all_flag_shows_closed_ports(capsys, open_port, closed_port):
    main(["127.0.0.1", "-p", f"{open_port},{closed_port}", "-t", "0.5", "--all"])
    out = capsys.readouterr().out
    assert f"{closed_port}/tcp" in out
    assert "closed" in out


def test_unknown_host_returns_error_code(capsys, unknown_host):
    code = main(["nonexistent.invalid", "-p", "80"])
    assert code == 1
    assert "cannot resolve host" in capsys.readouterr().err


@pytest.mark.parametrize(
    "args",
    [
        ["127.0.0.1", "-p", "99999"],
        ["127.0.0.1", "-t", "0"],
        ["127.0.0.1", "-w", "0"],
    ],
)
def test_invalid_arguments_exit_with_usage_error(capsys, args):
    with pytest.raises(SystemExit) as exit_info:
        main(args)
    assert exit_info.value.code == 2
    assert "error:" in capsys.readouterr().err
