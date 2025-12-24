## DNSMASQ - light

[man page dnsmasq](https://linux.die.net/man/8/dnsmasq)

Dnsmasq is a DNS query forwarder: it is not capable of recursively answering arbitrary queries starting from the
root servers but forwards such queries to a fully recursive upstream DNS server which is typically provided by an ISP

### Default ip range
```
  "range_start": "10.0.0.10",
    "range_end": "10.0.0.200",
    "lease_time": "12h",
    "gateway": "10.0.0.1",
    "dns": "10.0.0.1",
    "upstream_dns": "1.1.1.1",
```
