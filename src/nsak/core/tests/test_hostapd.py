from pathlib import Path

from nsak.core.access_point.config import AccessPointConfig
from nsak.core.access_point.hostapd_manager import HostapdManager


def test_write_hostapd_config(tmp_path: Path) -> None:
    """
    Test that the ap_mod config file is written correctly.

    :param tmp_path: temporary directory
    :return: None
    """
    config = AccessPointConfig(
        ssid="TEST_AP",
        interface="wlan0",
        channel=6,
        country_code="CH",
    )

    manager = HostapdManager(config_dir_path=tmp_path)

    path = manager._write_hostapd_config(config)
    content = path.read_text()

    assert path.exists()

    expected_lines = [
        "TEST_AP",
        "channel=6",
        "country_code=CH",
    ]

    for expected in expected_lines:
        assert expected in content


def test_start_and_stop_hostapd(tmp_path: Path) -> None:
    """
    Test that the ap_mod starts and stops correctly.

    :param tmp_path: temporary directory
    :return:
    """


pass
