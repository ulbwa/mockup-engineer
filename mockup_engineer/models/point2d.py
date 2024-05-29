from typing import Tuple, Sequence, Dict

from pydantic import validate_call, conint

from . import RestorableModel

_X_VALIDATOR = conint(ge=0)
_Y_VALIDATOR = conint(ge=0)


class Point2D(RestorableModel):
    """
    Class representing a 2-dimensional point.
    """

    __x: int
    __y: int

    @validate_call
    def __init__(
        self,
        __x: _X_VALIDATOR,
        __y: _Y_VALIDATOR,
        /,
    ):
        """
        :param __x: The x-coordinate of the point.
        :param __y: The y-coordinate of the point.
        """
        self.__x = __x  # get, set
        self.__y = __y  # get, set

    @property
    def x(self) -> _X_VALIDATOR:
        """
        X-coordinate of the point.
        """
        return self.__x

    @x.setter
    @validate_call
    def x(self, __x: _X_VALIDATOR, /):
        """
        Set the x-coordinate of the point.

        :param __x: The x-coordinate of the point.
        """
        self.__x = __x

    @property
    def y(self) -> _Y_VALIDATOR:
        """
        Y-coordinate of the point.
        """
        return self.__y

    @y.setter
    @validate_call
    def y(self, __y: _Y_VALIDATOR, /):
        """
        Set the y-coordinate of the point.

        :param __y: The y-coordinate of the point.
        """
        self.__y = __y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__x!r}, {self.__y!r})"

    def dump(self) -> Tuple[Sequence, Dict]:
        return (self.__x, self.__y), dict()


__all__ = ("Point2D",)
