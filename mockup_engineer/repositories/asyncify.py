from asyncio import get_running_loop, AbstractEventLoop
from typing import AsyncGenerator, AsyncIterator

from pydantic import validate_call, ConfigDict

from . import BaseAsyncRepository, BaseRepository, _CONFIG_VALIDATOR
from ..models.device import Device


class AsyncifyRepository(BaseAsyncRepository):
    """
    Asynchronous repository that wraps a synchronous repository.
    """

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(
        self,
        __sync_repository: BaseRepository,
        /,
        *,
        loop: AbstractEventLoop = None,
    ):
        """
        :param __sync_repository: The synchronous reader to wrap.
        :param loop: Optional. The event loop to use.
        """
        self.__sync_repository = __sync_repository
        self.__loop = loop or get_running_loop()

    async def _read_config(self) -> _CONFIG_VALIDATOR:
        return await self.__loop.run_in_executor(
            None, self.__sync_repository._read_config
        )

    async def _load_config(
        self, __config: _CONFIG_VALIDATOR, /
    ) -> AsyncGenerator[Device, None]:
        for device in await self.__loop.run_in_executor(
            None, self.__sync_repository._load_config, __config
        ):
            yield device

    def __aiter__(self) -> AsyncIterator[Device]:
        async def iterator():
            config = await self._read_config()
            async for device in self._load_config(config):
                yield device

        return iterator()

    async def _dump_config(self, *__devices: Device) -> _CONFIG_VALIDATOR:
        return await self.__loop.run_in_executor(
            None, self.__sync_repository._dump_config, *__devices
        )

    async def _write_config(self, __config: _CONFIG_VALIDATOR, /):
        return await self.__loop.run_in_executor(
            None, self.__sync_repository._write_config, __config
        )


__all__ = ("AsyncifyRepository",)
