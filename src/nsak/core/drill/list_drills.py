from nsak.core.drill import Drill, DrillLoader


def list_drills() -> list[Drill]:
    """
    Lists all drills.
    """
    drill_loader = DrillLoader()
    return drill_loader.load_all()
