sudo ip link add dmz-br type bridge && sudo ip link set dmz-br up && sudo sysctl net.ipv6.conf.dmz-br.disable_ipv6=1
sudo ip link add lan-br type bridge && sudo ip link set lan-br up && sudo sysctl net.ipv6.conf.lan-br.disable_ipv6=1
sudo ip link add wan-br type bridge && sudo ip link set wan-br up && sudo sysctl net.ipv6.conf.wan-br.disable_ipv6=1
