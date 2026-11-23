# portscan

A multithreaded TCP connect port scanner written with only the Python standard
library (`socket`, `concurrent.futures`, `argparse`).

> Scan only hosts you own or have permission to test.

```bash
cd portscan
python -m portscan 127.0.0.1 -p 7999-8001 --all
```

```
Scanning 127.0.0.1 (127.0.0.1), 3 ports...

PORT       STATE     SERVICE
7999/tcp   closed    irdmi2
8000/tcp   open      irdmi
8001/tcp   closed    vcom-tunnel

Done in 0.00s: 1 open, 2 closed, 0 filtered.
```

## Options

| Option | Default | What it does |
|---|---|---|
| `host` | - | host name or IP address (IPv4 or IPv6) |
| `-p`, `--ports` | `1-1024` | ports to scan, e.g. `22,80,8000-8010` |
| `-t`, `--timeout` | `1.0` | seconds to wait for each port |
| `-w`, `--workers` | `100` | how many ports to check at the same time |
| `-a`, `--all` | off | show closed and filtered ports too, not only open ones |

Exit codes: `0` scan finished, `1` host cannot be resolved, `2` invalid arguments.

## How it works

A **connect scan** tries a full TCP handshake on each port, the same way any
program opens a connection, so it needs no root rights:

| The host answers with | State | Meaning |
|---|---|---|
| SYN-ACK | `open` | a program is listening on the port |
| RST | `closed` | the host is up, but nothing listens there |
| nothing (timeout) or a network error | `filtered` | most likely a firewall drops the packets |

- The host name is resolved **once** before the scan (`resolve_host`), so a
  typo fails fast and there is one DNS query instead of one per port.
  `localhost` can resolve to IPv6 `::1`, so a server listening only on
  `127.0.0.1` will look closed there - scan `127.0.0.1` directly in that case.
- Ports are checked in a `ThreadPoolExecutor`. A scan is mostly waiting for the
  network, so threads give a big speedup: with 100 workers and a 1 s timeout,
  1000 filtered ports take about 10 s instead of 1000 s.
- `parse_ports` turns `"22,80,8000-8010"` into a sorted list without
  duplicates and rejects anything outside 1-65535.

## Tests

```bash
cd portscan
pytest
```

The tests start their own listening socket on `127.0.0.1`, so "open" and
"closed" are checked against a real TCP stack. Timeouts and DNS errors are
simulated with `monkeypatch`, so the tests never touch the internet.

They run automatically on GitHub Actions on every push
(`.github/workflows/portscan.yml`).
