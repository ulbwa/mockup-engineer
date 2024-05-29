from abc import ABC
from types import TracebackType
from typing import (
    Protocol,
    Iterator,
    Self,
    Optional,
    Type,
    AsyncIterator,
    Generator,
    AsyncGenerator,
)

from mockup_engineer.models import RestorableModel


class Reader(Protocol):
    """
    Protocol for reading and writing bytes from various sources.
    """

    def __enter__(self) -> Self:
        """
        Enter the runtime context related to this object.

        :returns: The current instance of the class.
        """

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        """
        Exit the runtime context related to this object.

        :param exc_type: Optional. The exception type.
        :param exc_value: Optional. The exception value.
        :param traceback: Optional. The traceback.
        """

    def open(self):
        """
        Open the underlying IO object.
        """

    def close(self):
        """
        Close the underlying IO object.
        """

    def read(self) -> bytes:
        """
        Read the entire contents of the object.

        :returns: The read bytes.
        """

    def write(self, __data: bytes, /):
        """
        Write bytes to the object.

        :param __data: The bytes to write.
        """

    def iter_chunks(self, __chunk_size: int, /) -> Generator[bytes, None, None]:
        """
        Iterate over chunks of bytes from the object.

        :param __chunk_size: The size of each chunk.

        :returns: A generator that yields chunks of bytes.
        """

    def __iter__(self) -> Iterator[bytes]:
        """
        Iterate over chunks of bytes from the IO object using a default chunk size of 1024.

        :returns: An iterator that yields chunks of bytes.
        """


class AsyncReader(Protocol):
    """
    Protocol for asynchronous reading and writing bytes from various sources.
    """

    async def __aenter__(self) -> Self:
        """
        Enter the asynchronous runtime context related to this object.

        :returns: The current instance of the class.
        """

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        """
        Exit the asynchronous runtime context related to this object.

        :param exc_type: Optional. The exception type.
        :param exc_value: Optional. The exception value.
        :param traceback: Optional. The traceback.
        """

    async def open(self):
        """
        Open the underlying object asynchronously.
        """

    async def close(self):
        """
        Close the underlying object asynchronously.
        """

    async def read(self) -> bytes:
        """
        Read the entire contents of the object asynchronously.

        :returns: The read bytes.
        """

    async def write(self, __data: bytes, /):
        """
        Write bytes to the object asynchronously.

        :param __data: The bytes to write.
        """

    async def iter_chunks(self, __chunk_size: int, /) -> AsyncGenerator[bytes, None]:
        """
        Iterate over chunks of bytes from the object asynchronously.

        :param __chunk_size: The size of each chunk.

        :returns: An asynchronous generator that yields chunks of bytes.
        """

    def __aiter__(self) -> AsyncIterator[bytes]:
        """
        Iterate over chunks of bytes from the object asynchronously using a default chunk size of 1024.

        :returns: An asynchronous iterator that yields chunks of bytes.
        """


class BaseReader(Reader, RestorableModel, ABC):
    """
    Abstract base class for reading and writing bytes from various sources.
    """

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        self.close()

    def read(self) -> bytes:
        return b"".join(self)

    def write(self, __data: bytes, /):
        raise NotImplementedError()

    def __iter__(self) -> Iterator[bytes]:
        return self.iter_chunks(1024)


class BaseAsyncReader(AsyncReader, RestorableModel, ABC):
    """
    Abstract base class for asynchronously reading and writing bytes from various sources.
    """

    async def __aenter__(self) -> Self:
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        await self.close()

    async def read(self) -> bytes:
        buffer = b""
        async for chunk in self:
            buffer += chunk
        return buffer

    async def write(self, __data: bytes, /):
        raise NotImplementedError()

    def __aiter__(self) -> AsyncIterator[bytes]:
        return self.iter_chunks(1024)  # type: ignore


__all__ = (
    "Reader",
    "AsyncReader",
    "BaseReader",
    "BaseAsyncReader",
)
