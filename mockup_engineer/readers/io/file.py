from pathlib import Path
from typing import Tuple, Sequence, Dict

from pydantic import ConfigDict, validate_call

from . import BaseIOReader


class FileReader(BaseIOReader):
    """
    Reader for files.
    """

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(self, __path: Path, /):
        """
        :param __path: The path to the file to read from.
        """
        self.__path = __path
        self._io = None

    def open(self):
        if self._io:
            raise IOError("File is already open")
        self._io = self.__path.open("rb+")

    def close(self):
        if not self._io:
            raise IOError("File is not open")
        self._io.close()
        self._io = None

    @property
    def path(self) -> Path:
        return self.__path

    def dump(self) -> Tuple[Sequence, Dict]:
        return (self.__path,), dict()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__path!r})"


__all__ = ("FileReader",)
