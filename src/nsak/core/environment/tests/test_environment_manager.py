from nsak.core.environment import EnvironmentManager


def test_environment_manager() -> None:
    """
    Tests if the environment manager lists any environment at all.

    This test could be improved by mocking the environment library, but is good enough for now.
    """
    # Arrange

    # Act
    environment_list = EnvironmentManager.list()

    # Assert
    assert len(environment_list) > 0

    # Act
    environment = EnvironmentManager.get(environment_list[0].id)

    # Assert
    assert environment is not None
