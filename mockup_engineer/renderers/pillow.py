from io import BytesIO
from typing import Self, Union, Optional

import PIL.Image
from pydantic import validate_call, ConfigDict, SkipValidation

from . import BaseRenderer
from ..models.point2d import Point2D
from ..models.size2d import Size2D


class PilRenderer(BaseRenderer):
    __proxy: PIL.Image.Image

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(self, __size_or_pil_image: Union[Size2D, PIL.Image.Image], /):  # noqa
        if isinstance(__size_or_pil_image, Size2D):
            self.__proxy = PIL.Image.new(
                "RGBA", (__size_or_pil_image.width, __size_or_pil_image.height)
            )
        else:
            self.__proxy = __size_or_pil_image
            __size_or_pil_image = Size2D(*self.__proxy.size)
        super().__init__(__size_or_pil_image)

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def resize(self, __size: Size2D, /):
        self.__proxy = self.__proxy.resize((__size.width, __size.height))
        print(self.__proxy)

    @validate_call
    def rotate(self, __angle: float, /):
        self.__proxy = self.__proxy.rotate(__angle, expand=True)

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def put_image(
        self,
        __image: BaseRenderer,
        __start_point: Point2D = Point2D(1, 1),
        /,
        *,
        mask: Optional[BaseRenderer] = None,
    ):
        if isinstance(__image, PilRenderer):
            __temp_image = __image
        else:
            __temp_image = PilRenderer.from_bytes(__image.to_bytes())
        if mask is not None and not isinstance(mask, PilRenderer):
            mask = PilRenderer.from_bytes(mask.to_bytes())
        self.__proxy.paste(
            __temp_image.__proxy,
            (__start_point.x, __start_point.y),
            mask.__proxy if mask is not None else None,
        )

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def put_alpha(self, __image: BaseRenderer, /):
        if isinstance(__image, PilRenderer):
            __temp_image = __image
        else:
            __temp_image = PilRenderer.from_bytes(__image.to_bytes())

        self.__proxy.putalpha(__temp_image)

    @classmethod
    @validate_call
    def from_bytes(cls, __data: bytes, /) -> SkipValidation[Self]:
        return cls(PIL.Image.open(BytesIO(__data)))

    def to_bytes(self) -> bytes:
        b = BytesIO()
        self.__proxy.save(b, "PNG")
        b.seek(0)
        return b.read()

    @property
    def size(self) -> Size2D:
        return Size2D(*self.__proxy.size)


__all__ = ("PilRenderer",)
