ip link add dmz-br type bridge && sudo ip link set dmz-br up
ip link add lan-br type bridge && sudo ip link set lan-br up
ip link add wan-br type bridge && sudo ip link set wan-br up