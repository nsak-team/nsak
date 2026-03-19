from unittest.mock import Mock, patch

from click.testing import CliRunner

from nsak.cli.device import list_devices, load_device, loaded_device, unload_device
from nsak.core import Device

DeviceMock = Mock(spec=Device)

fake_devices = [
    DeviceMock(
        id="test_device_1",
        name="Test Device 1",
        path="/home/user/nsak/lib/devices/test_device_1",
    ),
    DeviceMock(
        id="test_device_2",
        name="Test Device 2",
        path="/home/user/nsak/lib/devices/test_device_2",
    ),
    DeviceMock(
        id="test_device_3",
        name="Test Device 3",
        path="/home/user/nsak/lib/devices/test_device_3",
    ),
]


def test_list_devices() -> None:
    """
    Tests the cli command `nsak device list`, which should list all devices.
    """
    with patch("nsak.core.DeviceManager.list") as mock_list:
        # Arrange
        mock_list.return_value = fake_devices
        runner = CliRunner()

        # Act
        result = runner.invoke(list_devices)

    # Assert
    for device in fake_devices:
        assert str(device.id) in result.output
        assert str(device.name) in result.output
        assert str(device.path) in result.output


def test_device_loading() -> None:
    """
    Tests the cli command `nsak device load <device-name>`, `nsak device loaded` and `nsak device unload`.
    """
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(loaded_device)

    # Assert
    assert "No device loaded." in result.output

    # Act
    result = runner.invoke(unload_device)

    # Assert
    assert "Device unloaded." in result.output

    # Act
    result = runner.invoke(load_device, "bananapi_r4")

    # Assert
    assert "Successfully loaded device config: bananapi_r4" in result.output

    # Act
    result = runner.invoke(loaded_device)

    # Assert
    assert "Loaded device: BananaPI R4 (id = bananapi_r4" in result.output

    # Act
    result = runner.invoke(unload_device)

    # Assert
    assert "Device unloaded." in result.output

    # Act
    result = runner.invoke(loaded_device)

    # Assert
    assert "No device loaded." in result.output
