from abc import ABC
from typing import Optional, Mapping, Tuple, Sequence, Dict

from pydantic import AnyHttpUrl, validate_call

from .. import BaseReader, BaseAsyncReader


class BaseHTTPReader(BaseReader, ABC):
    """
    Abstract base class for HTTP readers.
    """

    @validate_call
    def __init__(
        self,
        __url: AnyHttpUrl,
        /,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ):
        self._url = __url
        self._headers = headers or {}

    @property
    def url(self) -> str:
        return str(self._url)

    def dump(self) -> Tuple[Sequence, Dict]:
        return (self._url,), dict(headers=self._headers)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._url!r}, headers={self._headers})"


class BaseAsyncHTTPReader(BaseAsyncReader, ABC):
    """
    Abstract base class for asynchronous HTTP readers.
    """

    @validate_call
    def __init__(
        self,
        __url: AnyHttpUrl,
        /,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ):
        """
        :param __url: The URL of the HTTP resource.
        :param headers: Optional. HTTP headers.
        """
        self._url = __url
        self._headers = headers or {}

    def dump(self) -> Tuple[Sequence, Dict]:
        return (self._url,), dict(headers=self._headers)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._url!r}, headers={self._headers})"


__all__ = (
    "HTTPReader",
    "BaseHTTPReader",
    "BaseAsyncHTTPReader",
)
