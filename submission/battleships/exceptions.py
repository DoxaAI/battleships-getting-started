class ShipRegistrationException(Exception):
    """Ship cannot be registered."""

    def __init__(self, msg) -> None:
        super().__init__(msg)


class InvalidShipException(Exception):
    """Ship cannot be created."""

    def __init__(self, msg) -> None:
        super().__init__(msg)


class InvalidShipsCountException(Exception):
    """Number of ships of different kinds incorrect."""

    def __init__(self, msg) -> None:
        super().__init__(msg)

class ImpossibleShipGenerationException(Exception):
    """Impossible specification of ships to generate."""

    def __init__(self, msg) -> None:
        super().__init__(msg)

