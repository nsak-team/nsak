#!/usr/bin/env bash

NSAK_LAB_BRIDGE=br-nsak-lab
NSAK_LAB_SUBNET=10.10.10.1/24

sudo ip link add "$NSAK_LAB_BRIDGE" type bridge
sudo ip addr add "$NSAK_LAB_SUBNET" dev "$NSAK_LAB_BRIDGE"
sudo ip link set "$NSAK_LAB_BRIDGE" up

#sudo ip link add veth-host type veth peer name veth-br
#sudo ip link set veth-br master br-lab
#sudo ip link set veth-br up
#sudo ip link set veth-host up
#sudo ip addr add 10.10.10.254/24 dev veth-host
