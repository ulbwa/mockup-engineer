from abc import ABC
from typing import Iterator, BinaryIO, Optional

from pydantic import validate_call, conint

from .. import BaseReader


class BaseIOReader(BaseReader, ABC):
    """
    Abstract base class for IO readers.

    :ivar _io: The underlying IO object.
    """

    _io: Optional[BinaryIO]

    @validate_call
    def iter_chunks(self, __chunk_size: conint(gt=0), /) -> Iterator[bytes]:
        if not self._io:
            raise IOError("IO is not open")
        self._io.seek(0)
        while True:
            if chunk := self._io.read(__chunk_size):
                yield chunk
            else:
                break

    def write(self, __data: bytes, /):
        if not self._io:
            raise IOError("IO is not open")
        self._io.seek(0)
        self._io.write(__data)
        self._io.truncate()


__all__ = ("BaseIOReader",)
