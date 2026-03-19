from nsak.core.drill import DrillManager


def test_drill_manager() -> None:
    """
    Tests if the drill manager lists any drill at all.

    This test could be improved by mocking the drill library, but is good enough for now.
    """
    # Arrange

    # Act
    drill_list = DrillManager.list()

    # Assert
    assert len(drill_list) > 0

    # Act
    drill = DrillManager.get(drill_list[0].id)

    # Assert
    assert drill is not None
