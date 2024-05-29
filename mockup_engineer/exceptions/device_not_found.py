from pydantic import validate_call, constr


class DeviceNotFound(Exception):
    """
    Exception raised when a device is not found.
    """

    @validate_call
    def __init__(self, __message: constr(min_length=1) = "Device not found", /):
        super().__init__(__message)


__all__ = ("DeviceNotFound",)
