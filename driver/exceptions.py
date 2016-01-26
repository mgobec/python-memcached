# Exceptions thrown by the driver


class DriverException(Exception):
    """
    Base exception for all driver exceptions.
    """
    pass


class DriverConnectionException(DriverException):
    """
    Indicates that connection could not be established with the server.
    """
    pass


class DriverCommandException(DriverException):
    """
    Indicates that there was an error in the command sent to the server.
    """
    pass


class DriverUnknownException(DriverException):
    """
    Indicates that the driver received an unexpected response from the server.
    """
    pass


class DriverClientException(DriverException):
    """
    Indicates that the server replied with a client error message.
    """
    pass


class DriverServerException(DriverException):
    """
    Indicates that the server replied with a server error message.
    """
    pass


class DriverConversionException(DriverException):
    """
    Indicates that there was an error in the value conversion.
    """
    pass


class DriverConnectionLimitExceededException(DriverException):
    """
    Indicates that the driver reached a maximum number of connections available.
    """
    pass
