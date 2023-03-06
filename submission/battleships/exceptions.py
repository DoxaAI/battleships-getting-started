class BattleshipsException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)


class ShipRegistrationException(BattleshipsException):
    """Ship cannot be registered."""

    pass


class InvalidShipException(BattleshipsException):
    """Ship cannot be created."""

    pass


class InvalidShipsCountException(BattleshipsException):
    """Number of ships of different kinds incorrect."""

    pass


class ImpossibleShipGenerationException(BattleshipsException):
    """Impossible specification of ships to generate."""

    pass
