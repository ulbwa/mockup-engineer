from . import RestorableStrEnum


class DeviceType(RestorableStrEnum):
    """
    Enumeration representing types of devices.

    :cvar SMARTPHONE: Device type representing smartphones.
    :cvar TABLET: Device type representing tablets.
    :cvar WEARABLE: Device type representing wearable devices.
    :cvar DESKTOP: Device type representing desktop computers.
    """

    SMARTPHONE = "smartphone"
    TABLET = "tablet"
    WEARABLE = "wearable"
    DESKTOP = "desktop"


__all__ = ("DeviceType",)
