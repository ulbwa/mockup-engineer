from abc import ABC
from typing import (
    Dict,
    Sequence,
    Tuple,
    Any,
    Iterator,
    Protocol,
    AsyncIterator,
    AsyncGenerator,
    Generator,
)

from mockup_engineer.models.device import Device

_CONFIG_OBJECT_VALIDATOR = Tuple[Sequence[Any], Dict[str, Any]]
_CONFIG_VALIDATOR = Sequence[_CONFIG_OBJECT_VALIDATOR]


class Repository(Protocol):
    """
    Protocol for a repository handling configuration and device operations.
    """

    def _read_config(self) -> _CONFIG_VALIDATOR:
        """
        Reads the configuration from the source.

        :return: The configuration validator object.
        """

    def _load_config(
        self, __config: _CONFIG_VALIDATOR, /
    ) -> Generator[Device, None, None]:
        """
        Loads the configuration and returns a generator of devices.

        :return: A generator yielding Device objects.
        """

    def _dump_config(self, *__devices: Device) -> _CONFIG_VALIDATOR:
        """
        Dumps the provided devices into a configuration.

        :param __devices: Devices to be dumped into the configuration.

        :return: Configuration containing provided devices.
        """

    def _write_config(self, __config: _CONFIG_VALIDATOR, /):
        """
        Writes the configuration to the source.
        """

    def __iter__(self) -> Iterator[Device]:
        """
        Returns an iterator over devices.

        :return: An iterator yielding Device objects.
        """

    def load(self) -> Sequence[Device]:
        """
        Loads and returns a sequence of devices.

        :return: A sequence of Device objects.
        """

    def save(self, *__devices: Device):
        """
        Saves the provided devices.

        :param __devices: Devices to be saved.
        """


class AsyncRepository(Protocol):
    """
    Protocol for an asynchronous repository handling configuration and device operations.
    """

    async def _read_config(self) -> _CONFIG_VALIDATOR:
        """
        Asynchronously reads the configuration from the source.

        :return: The configuration validator object.
        """

    async def _load_config(
        self, __config: _CONFIG_VALIDATOR, /
    ) -> AsyncGenerator[Device, None]:
        """
        Asynchronously loads the configuration and returns a generator of devices.

        :return: A generator yielding Device objects.
        """

    async def _dump_config(self, *__devices: Device) -> _CONFIG_VALIDATOR:
        """
        Asynchronously dumps the provided devices into a configuration.

        :param __devices: Devices to be dumped into the configuration.

        :return: Configuration containing provided devices.
        """

    async def _write_config(self, __config: _CONFIG_VALIDATOR, /):
        """
        Asynchronously writes the configuration to the source.
        """

    def __aiter__(self) -> AsyncIterator[Device]:
        """
        Returns an asynchronous iterator over devices.

        :return: An asynchronous iterator yielding Device objects.
        """

    async def load(self) -> Sequence[Device]:
        """
        Asynchronously loads and returns a sequence of devices.

        :return: A sequence of Device objects.
        """

    async def save(self, *__devices: Device):
        """
        Asynchronously saves the provided devices.

        :param __devices: Devices to be saved.
        """


class BaseRepository(Repository, ABC):
    """
    Abstract base class for a repository handling configuration and device operations.
    """

    def _dump_config(self, *__devices: Device) -> _CONFIG_VALIDATOR:
        raise NotImplementedError()

    def _write_config(self, __config: _CONFIG_VALIDATOR, /):
        raise NotImplementedError()

    def __iter__(self) -> Iterator[Device]:
        return self._load_config(self._read_config())

    def load(self) -> Sequence[Device]:
        return tuple(self)

    def save(self, *__devices: Device):
        self._write_config(self._dump_config(*__devices))


class BaseAsyncRepository(AsyncRepository, ABC):
    """
    Abstract base class for an asynchronous repository handling
    configuration and device operations.
    """

    async def _dump_config(self, *__devices: Device) -> _CONFIG_VALIDATOR:
        raise NotImplementedError()

    async def _write_config(self, __config: _CONFIG_VALIDATOR, /):
        raise NotImplementedError()

    async def load(self) -> Sequence[Device]:
        devices = list()
        async for device in self:
            devices.append(device)
        return tuple(devices)

    async def save(self, *__devices: Device):
        await self._write_config(await self._dump_config(*__devices))


__all__ = ("Repository", "AsyncRepository", "BaseRepository", "BaseAsyncRepository")
