from unittest.mock import Mock, patch

from click.testing import CliRunner

from nsak.cli.device import list_devices
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
