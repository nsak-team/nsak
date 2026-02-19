## Testing in lab

The idea was, testing the dnsmasq config in the provided lab. Are the necessary config files
are getting created and is the client1 able to receive an Ip in the range of `"range_start": "10.0.0.10"` -
`"range_end": "10.0.4.14" `.
Therefore the setup of the nsak project on the ns in the lab network was necessary.
The project is set up and accessable with https and a private access token.

Result of the test. The temp/dnsmasq/config file is created. But the lease file is missing which
is totally normal as no client has tried to establish a connection.

I tried to temper the inline connection of the client1 to check if the lease file is getting created.
In the lab set up, the clients are with the L3-Router inline so the dhcp does not work which should not
be an issue in enterprise or wifi scenario.
