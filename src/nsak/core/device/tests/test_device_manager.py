from nsak.core.device import DeviceManager


def test_device_manager() -> None:
    """
    Tests if the device manager lists any device at all.

    This test could be improved by mocking the device library, but is good enough for now.
    """
    # Arrange

    # Act
    device_list = DeviceManager.list()

    # Assert
    assert len(device_list) > 0

    # Act
    device = DeviceManager.get(device_list[0].id)

    # Assert
    assert device is not None
