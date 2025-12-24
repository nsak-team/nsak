## DNSMASQ - light

[man page dnsmasq](https://linux.die.net/man/8/dnsmasq)

Dnsmasq is a DNS query forwarder: it it not capable of recursively answering arbitrary queries starting from the
root servers but forwards such queries to a fully recursive upstream DNS server which is typically provided by an ISP

### Default ip range
```
    "range_start": "10.0.0.10",
    "range_end": "10.0.4.14",  # 1024 addresses
    "lease_time": "12h",
```
