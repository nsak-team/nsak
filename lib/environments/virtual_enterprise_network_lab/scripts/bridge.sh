sudo ip link add dmz-br type bridge && sudo ip link set dmz-br up
sudo ip link add lan-br type bridge && sudo ip link set lan-br up
sudo ip link add wan-br type bridge && sudo ip link set wan-br up