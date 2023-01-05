from typing import Set, Dict, Any, Optional, Callable
from ipaddress import IPv4Address, IPv4Network


#
# Reusable validators
#
def formatted_string(v: str, values: Dict[str, Any]) -> str:
    """
    Process v as a python formatted string
    :param v: Value to be validated
    :param values: {<field name>: <field value> ...} dict of previously validated model fields
    :return: Expanded formatted string
    """
    try:
        return v.format(**values) if v is not None else v
    except KeyError as ex:
        raise ValueError(f"Variable not found: {ex}") from None


_used_addresses: Set[IPv4Address] = set()


def unique_system_ip(system_ip: IPv4Address) -> IPv4Address:
    if system_ip in _used_addresses:
        raise ValueError(f'system-ip "{system_ip}" is already in use')

    _used_addresses.add(system_ip)
    return system_ip


def constrained_cidr(
    *,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    length: Optional[int] = None
) -> Callable[[IPv4Network], IPv4Network]:
    def validator(ipv4_network: IPv4Network):
        if length is not None and ipv4_network.prefixlen != length:
            raise ValueError(f'IPv4 prefix length needs to be /{length}')
        if max_length is not None and ipv4_network.prefixlen > max_length:
            raise ValueError(f'IPv4 prefix length needs to be <= /{max_length}')
        if min_length is not None and ipv4_network.prefixlen < min_length:
            raise ValueError(f'IPv4 prefix length needs to be >= /{min_length}')

        return ipv4_network

    return validator
