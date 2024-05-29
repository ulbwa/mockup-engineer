from asyncio import AbstractEventLoop, get_running_loop
from typing import Tuple, Sequence, Dict, AsyncGenerator

from pydantic import ConfigDict, validate_call, conint

from . import BaseAsyncReader, BaseReader


class AsyncifyReader(BaseAsyncReader):
    """
    Asynchronous reader that wraps a synchronous reader.
    """

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(
        self,
        __sync_reader: BaseReader,
        /,
        *,
        loop: AbstractEventLoop = None,
    ):
        """
        :param __sync_reader: The synchronous reader to wrap.
        :param loop: Optional. The event loop to use.
        """
        self.__sync_reader = __sync_reader
        self.__loop = loop or get_running_loop()

    async def open(self):
        await self.__loop.run_in_executor(None, self.__sync_reader.open)

    async def close(self):
        await self.__loop.run_in_executor(None, self.__sync_reader.close)

    async def read(self) -> bytes:
        return await self.__loop.run_in_executor(None, self.__sync_reader.read)

    async def write(self, __data: bytes, /):
        await self.__loop.run_in_executor(None, self.__sync_reader.write, __data)

    @validate_call
    async def iter_chunks(
        self, __chunk_size: conint(gt=0), /
    ) -> AsyncGenerator[bytes, None]:
        for chunk in await self.__loop.run_in_executor(
            None, self.__sync_reader.iter_chunks, __chunk_size
        ):
            yield chunk

    def dump(self) -> Tuple[Sequence, Dict]:
        return self.__sync_reader.dump()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__sync_reader!r})"


__all__ = ("AsyncifyReader",)
