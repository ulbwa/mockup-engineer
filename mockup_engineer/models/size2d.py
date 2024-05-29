from typing import Tuple, Sequence, Dict

from pydantic import validate_call, conint

from . import RestorableModel

_WIDTH_VALIDATOR = conint(ge=1)
_HEIGHT_VALIDATOR = conint(ge=1)


class Size2D(RestorableModel):
    """
    Class representing a 2-dimensional size.
    """

    __width: int
    __height: int

    @validate_call
    def __init__(
        self,
        __width: _WIDTH_VALIDATOR,
        __height: _HEIGHT_VALIDATOR,
        /,
    ):
        """
        :param __width: The width of the size.
        :param __height: The height of the size.
        """
        self.__width = __width  # get, set
        self.__height = __height  # get, set

    @property
    def width(self) -> _WIDTH_VALIDATOR:
        """
        Width of the size.
        """
        return self.__width

    @width.setter
    @validate_call
    def width(self, __width: _WIDTH_VALIDATOR, /):
        """
        Set the width of the size.

        :param __width: The width of the size.
        """
        self.__width = __width

    @property
    def height(self) -> _HEIGHT_VALIDATOR:
        """
        Height of the size.
        """
        return self.__height

    @height.setter
    @validate_call
    def height(self, __height: _HEIGHT_VALIDATOR, /):
        """
        Set the height of the size.

        :param __height: The height of the size.
        """
        self.__height = __height

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__width!r}, {self.__height!r})"

    def dump(self) -> Tuple[Sequence, Dict]:
        return (self.__width, self.__height), dict()


__all__ = ("Size2D",)
