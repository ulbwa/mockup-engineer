from contextlib import suppress
from typing import List, Iterator

from pydantic import validate_call, ConfigDict, UUID4

from .exceptions.device_not_found import DeviceNotFound
from .exceptions.duplicate_identifier import DuplicateIdentifier
from .exceptions.template_not_found import TemplateNotFound
from .models.device import Device
from .models.template import Template
from .repositories import BaseRepository, BaseAsyncRepository
from .singleton_meta import SingletonMeta


class TemplateStorage(metaclass=SingletonMeta):
    """
    Storage for devices and associated templates.
    """

    __devices: List[Device]

    def __init__(self):  # noqa
        self.__devices = []

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def append(self, __device: Device, /):
        """
        Append a device to the storage.

        :param __device: Device to be appended.

        :raises DuplicateIdentifier: If device or template with the same ID already exists.
        """
        if __device.id in map(lambda x: x.id, self.__devices):
            raise DuplicateIdentifier(
                "Can't append device to storage because "
                f"device with id {__device.id!r} already exists"
            )

        for device_template in __device:
            for assigned_device in self.__devices:
                if any(
                    map(
                        lambda assigned_template: assigned_template.id
                        == device_template.id,
                        assigned_device,
                    )
                ):
                    raise DuplicateIdentifier(
                        "Can't append device to storage because "
                        f"template with id {device_template.id!r} already exists"
                    )

        self.__devices.append(__device)

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def remove(self, __device: Device, /):
        """
        Remove a device from the storage.

        :param __device: Device to be removed.
        :raises ValueError: If device is not found in the storage.
        """
        if __device not in self.__devices:
            raise ValueError(f"{__device!r} not in storage")

        self.__devices.remove(__device)

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def import_from_repository(self, __repository: BaseRepository, /):
        """
        Import devices from a repository into the storage.

        :param __repository: Repository to import devices from.
        """
        for device in __repository:
            self.append(device)

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    async def import_from_async_repository(self, __repository: BaseAsyncRepository, /):
        """
        Import devices from an asynchronous repository into the storage.

        :param __repository: Asynchronous repository to import devices from.
        """
        async for device in __repository:
            self.append(device)

    @validate_call
    def get_device_by_id(self, __id: UUID4, /) -> Device:
        """
        Get a device by its ID.

        :param __id: ID of the device to retrieve.
        :return: Device with the specified ID.
        :raises DeviceNotFound: If device with the specified ID is not found.
        """
        for device in self:
            if device.id == __id:
                return device
        else:
            raise DeviceNotFound(f"Device with id {__id!r} is not found")

    @validate_call
    def get_template_by_id(self, __id: UUID4, /) -> Template:
        """
        Get a template by its ID.

        :param __id: ID of the template to retrieve.
        :return: Template with the specified ID.
        :raises TemplateNotFound: If template with the specified ID is not found.
        """
        for device in self:
            with suppress(TemplateNotFound):
                return device.get_template_by_id(__id)
        else:
            raise TemplateNotFound(f"Template with id {__id!r} is not found")

    def __iter__(self) -> Iterator[Device]:
        return iter(self.__devices)


__all__ = ("TemplateStorage",)
