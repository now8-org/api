"""Module to store common service functions."""


class TransportTypeError(ValueError):
    """Invalid transport type error."""

    def __init__(self, transport_type: str):
        """Set the error message and raise the exception.

        Arguments:
            transport_type: Invalid transport type passed.
        """
        message = f"Invalid transport type '{transport_type}'."
        super().__init__(message)


class StopIdError(ValueError):
    """Invalid stop ID error."""

    def __init__(self, stop_id: str):
        """Set the error message and raise the exception.

        Arguments:
            stop_id: Invalid stop identifier passed.
        """
        message = f"Invalid stop ID '{stop_id}'."
        super().__init__(message)


class CityNameError(ValueError):
    """Invalid city name error."""

    def __init__(self, city_name: str):
        """Set the error message and raise the exception.

        Arguments:
            city_name: Invalid city name passed.
        """
        message = f"Invalid city name '{city_name}'."
        super().__init__(message)
