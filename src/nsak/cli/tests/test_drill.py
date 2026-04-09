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
    with patch("nsak.core.DrillManager.list") as mock_list:
        mock_list.return_value = fake_drills
        runner = CliRunner()

        # Act
        result = runner.invoke(list_drills)

    # Assert
    for drill in fake_drills:
        assert str(drill.id) in result.output
        assert str(drill.name) in result.output
        assert str(drill.path.relative_to()) in result.output
