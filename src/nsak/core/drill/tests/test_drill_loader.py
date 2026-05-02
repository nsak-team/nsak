import dataclasses

from nsak.core import DrillLoader
from nsak.core.drill.drill import DrillArgument, DrillInterface


def test_drill_loader_interface() -> None:
    """
    Tests if the drill loader correctly loads the interface.

    This test could be improved by mocking the drill library, but is good enough for now.
    """
    # Arrange
    expected_interface = DrillInterface(
        arguments={
            "network_discovery_result_map": DrillArgument(
                type="NetworkDiscoveryResultMap",
                default=dataclasses.MISSING,
            ),
        },
        return_type="list[subprocess.Popen]",
    )

    # Act
    drill = DrillLoader.load("arp_spoof")

    # Assert
    assert drill.interface == expected_interface
