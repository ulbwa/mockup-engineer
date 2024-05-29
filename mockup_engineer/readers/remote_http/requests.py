from typing import Optional, Iterator

from pydantic import validate_call, conint

from . import BaseHTTPReader

try:
    import requests
except ImportError:
    requests = None


class RequestsReader(BaseHTTPReader):
    __response: Optional["requests.Response"] = None

    def __send_request(self) -> "requests.Response":
        if requests is None:
            raise ImportError("'requests' is required to use RequestsReader")

        return requests.get(str(self._url), headers=self._headers)

    def open(self):
        if not self.__response:
            self.__response = self.__send_request()

    @validate_call
    def iter_chunks(self, __chunk_size: conint(gt=0), /) -> Iterator[bytes]:
        if self.__response is None:
            raise IOError("Request is not sent")
        return self.__response.iter_content(__chunk_size)


__all__ = ("RequestsReader",)
