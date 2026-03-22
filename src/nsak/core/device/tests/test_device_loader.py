from ipaddress import IPv4Interface

from nsak.core.device.device import (
    DeviceConfigration,
)
from nsak.core.device.device_loader import DeviceLoader
from nsak.core.network.configuration import (
    EthernetConfiguration,
    IPConfiguration,
    NetworkConfiguration,
)


def test_device_loader_configuration() -> None:
    """
    Tests if the device loader correctly loads the configuration.

    This test could be improved by mocking the device library, but is good enough for now.
    """
    # Arrange
    raw = {
        "network": {
            "ethernets": {
                "lan1@eth0": {
                    "addresses": {
                        "10.10.10.30/24": {"is_target": True, "is_management": False},
                        "10.10.20.30/24": {"is_target": False, "is_management": True},
                    }
                }
            }
        }
    }
    expected_configuration = DeviceConfigration(
        raw=raw,
        network=NetworkConfiguration(
            ethernets={
                "lan1@eth0": EthernetConfiguration(
                    name="lan1@eth0",
                    addresses={
                        "10.10.10.30/24": IPConfiguration(
                            ip=IPv4Interface("10.10.10.30/24"),
                            is_target=True,
                            is_management=False,
                        ),
                        "10.10.20.30/24": IPConfiguration(
                            ip=IPv4Interface("10.10.20.30/24"),
                            is_target=False,
                            is_management=True,
                        ),
                    },
                )
            }
        ),
    )

    # Act
    device = DeviceLoader.load("bananapi_r4")

    # Assert
    assert device.configuration == expected_configuration
