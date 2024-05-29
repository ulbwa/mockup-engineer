from base64 import b64decode, b64encode
from io import BytesIO
from typing import Tuple, Sequence, Dict, Optional, Self

from pydantic import ConfigDict, validate_call, SkipValidation

from . import BaseIOReader


class BytesIOReader(BaseIOReader):
    """
    Reader for BytesIO objects.
    """

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(self, __buffer: Optional[BytesIO] = None, /):
        """
        :param __buffer: The BytesIO object to read from.
        """
        self._io = __buffer or BytesIO()

    def dump(self) -> Tuple[Sequence, Dict]:
        self._io.seek(0)
        return (b64encode(self._io.read()).decode(),), dict()

    @classmethod
    @validate_call
    def load(cls, __args_kwargs: Tuple[Sequence, Dict], /) -> SkipValidation[Self]:
        args, kwargs = __args_kwargs
        buffer = b""
        if args[0]:
            buffer = b64decode(str(args[0]))
        return cls(BytesIO(buffer), *args[1:], **kwargs)  # type: ignore

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._io!r})"


__all__ = ("BytesIOReader",)
