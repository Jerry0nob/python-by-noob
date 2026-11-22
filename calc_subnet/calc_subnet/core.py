import ipaddress
from dataclasses import dataclass


@dataclass(frozen=True)
class SubnetInfo:
    network: str
    broadcast: str
    usable_hosts: int


def subnet_info(cidr: str) -> SubnetInfo:
    network = ipaddress.ip_network(cidr, strict=False)
    if network.prefixlen == 31:
        # RFC 3021: /31 networks are point-to-point
        # links and have 2 usable addresses
        usable_hosts = 2
    elif network.prefixlen == 32:
        usable_hosts = 1
    else:
        usable_hosts = network.num_addresses - 2
    return SubnetInfo(
        network=str(network.network_address),
        broadcast=str(network.broadcast_address),
        usable_hosts=usable_hosts,
    )
