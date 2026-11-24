# calc_subnet

A small IPv4 subnet calculator (work in progress).

Give it a network in CIDR notation, for example `192.168.1.0/24`, and it tells
you the network address, the broadcast address and how many hosts fit in it.

```python
>>> from calc_subnet.core import subnet_info
>>> subnet_info("192.168.1.0/24")
SubnetInfo(network='192.168.1.0', broadcast='192.168.1.255', usable_hosts=254)
```

## Tests

```bash
cd calc_subnet
pytest
```
