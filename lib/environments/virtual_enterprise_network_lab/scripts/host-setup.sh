sudo ip link add dmz-br type bridge && sudo ip link set dmz-br up
sudo ip link add lan-br type bridge && sudo ip link set lan-br up
sudo ip link add wan-br type bridge && sudo ip link set wan-br up

sudo ip addr add 10.0.1.254/24 dev wan-br

sudo iptables -t nat -A POSTROUTING -s 10.0.1.0/24 ! -d 10.0.1.0/24 -j MASQUERADE
