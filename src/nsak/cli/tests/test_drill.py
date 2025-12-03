from unittest.mock import Mock, patch

from click.testing import CliRunner

from nsak.cli.drill import list_drills
from nsak.core import Drill

DrillMock = Mock(spec=Drill)

fake_drills = [
    DrillMock(name="test_drill_1"),
    DrillMock(name="test_drill_2"),
    DrillMock(name="test_drill_3"),
]


def test_list_drills() -> None:
    """
    Tests the cli command `nsak drill list`, which should list all drills.
    """
    # Arrange
    expected_output = f"{'\n'.join([str(drill.name) for drill in fake_drills])}\n"

    with patch("nsak.core.DrillManager.list") as mock_list:
        mock_list.return_value = fake_drills
        runner = CliRunner()

        # Act
        result = runner.invoke(list_drills)

    # Assert
    assert result.output == expected_output
