# Exceptions thrown by the driver


class DriverException(Exception):
    pass


class DriverConnectionException(DriverException):
    pass


class DriverCommandException(DriverException):
    pass


class DriverUnknownException(DriverException):
    pass


class DriverClientException(DriverException):
    pass


class DriverServerException(DriverException):
    pass


class DriverConversionException(DriverException):
    pass
