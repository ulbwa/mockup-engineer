from typing import Optional, Tuple, Sequence, Dict, Self, Type, Union
from uuid import UUID

from pydantic import validate_call, UUID4, ConfigDict, SkipValidation

from . import BaseRestorableModel
from .color import Color
from .device import Device
from .point2d import Point2D
from .size2d import Size2D
from ..exceptions.duplicate_identifier import DuplicateIdentifier
from ..readers import BaseReader, BaseAsyncReader  # noqa


class Template(BaseRestorableModel):
    """
    Class representing a template.
    """

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(
        self,
        *,
        id: UUID4,  # noqa
        color: Color,
        screenshot_start_point: Point2D,
        screenshot_size: Size2D,
        frame: Union[BaseReader, BaseAsyncReader],
        mask: Optional[Union[BaseReader, BaseAsyncReader]] = None,
        device: Optional[Device] = None,
    ):
        """
        :param id: The unique identifier of the template.
        :param color: The Color object associated with the template.
        :param screenshot_start_point: The Point2D object representing the starting point of a screenshot.
        :param screenshot_size: The Size2D object representing the size of the screenshot.
        :param frame: The BaseReader or BaseAsyncReader object representing template frame.
        :param mask: Optional. The BaseReader or BaseAsyncReader object representing template's screenshot mask.
        :param device: Optional. Device object associated with the template.
        """
        self.__id = id  # get, set
        self.__color = color  # get, set
        self.__screenshot_start_point = screenshot_start_point  # get, set
        self.__screenshot_size = screenshot_size  # get, set
        self.__frame = frame  # get
        self.__mask = mask  # get

        # init device
        self.__device = None
        self.device = device

    @property
    def id(self) -> UUID:
        """
        The unique identifier of the template.
        """
        return self.__id

    @id.setter
    @validate_call
    def id(self, __id: UUID4, /):
        """
        Set the unique identifier of the template.

        :param __id: The unique identifier of the template.
        """
        self.__id = __id

    @property
    def device(self) -> Optional[Device]:
        """
        Device object associated with the template.
        """
        return self.__device

    @device.setter
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def device(self, __device: Optional[Device], /):
        """
        Set the Device object associated with the template.

        :param __device: Device object associated with the template.
        """
        if __device == self.__device:
            return
        if self.id in map(lambda device_template: device_template.id, __device):
            raise DuplicateIdentifier(
                "Can't assign template to device because "
                f"template with id {self.id!r} already exists"
            )
        if self.__device:
            self.__device._Device__templates.remove(self)  # noqa
        if __device:
            __device._Device__templates.append(self)  # noqa
        self.__device = __device

    @property
    def color(self) -> Color:
        """
        The Color object associated with the template.
        """
        return self.__color

    @color.setter
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def color(self, __color: Color, /):
        """
        Set the Color object associated with the template.

        :param __color: The Color object associated with the template.
        """
        self.__color = __color

    @property
    def screenshot_start_point(self) -> Point2D:
        """
        The Point2D object representing the starting point of a screenshot.
        """
        return self.__screenshot_start_point

    @screenshot_start_point.setter
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def screenshot_start_point(self, __screenshot_start_point: Point2D, /):
        """
        Set the Point2D object representing the starting point of a screenshot.

        :param __screenshot_start_point: The Point2D object representing the starting point of a screenshot.
        """
        self.__screenshot_start_point = __screenshot_start_point

    @property
    def screenshot_size(self) -> Size2D:
        """
        The Size2D object representing the size of the screenshot.
        """
        return self.__screenshot_size

    @screenshot_size.setter  # noqa
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def screenshot_size(self, __screenshot_size: Size2D, /):
        """
        Set the Size2D object representing the size of the screenshot.

        :param __screenshot_size: The Size2D object representing the size of the screenshot.
        """
        self.__screenshot_size = __screenshot_size

    @property
    def frame(self) -> Union[BaseReader, BaseAsyncReader]:
        """
        The BaseReader or BaseAsyncReader object representing template frame.
        """
        return self.__frame

    @property
    def mask(self) -> Optional[Union[BaseReader, BaseAsyncReader]]:
        """
        The BaseReader or BaseAsyncReader object representing template's screenshot mask.
        """
        return self.__mask

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"color={self.color!r}, "
            f"screenshot_start_point={self.screenshot_start_point!r}, "
            f"screenshot_size={self.screenshot_size!r}, "
            f"frame={self.frame!r}, "
            f"mask={self.mask!r})"
        )

    @validate_call
    def dump(
        self,
        *,
        exclude_device: bool = False,
        exclude_frame: bool = False,
        exclude_mask: bool = False,
    ) -> Tuple[Sequence, Dict]:
        return tuple(), dict(
            id=str(self.__id),
            color=self.__color.dump(),
            screenshot_start_point=self.__screenshot_start_point.dump(),
            screenshot_size=self.__screenshot_size.dump(),
            **(dict() if exclude_frame else dict(frame=self.__frame.dump())),
            **(
                dict()
                if exclude_mask
                else dict(mask=self.__mask.dump() if self.__mask is not None else None)
            ),
            **(
                dict()
                if exclude_device
                else dict(
                    device=self.__device.dump() if self.__device is not None else None
                )
            ),
        )

    @classmethod
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def load(
        cls,
        __args_kwargs: Tuple[Sequence, Dict],
        /,
        *,
        reader_cls: Optional[Type[Union[BaseReader, BaseAsyncReader]]] = None,
        excluded_device: Optional[Device] = None,
        excluded_frame: Optional[BaseReader] = None,
        excluded_mask: Optional[BaseReader] = None,
    ) -> SkipValidation[Self]:
        assert (excluded_frame and excluded_mask) or reader_cls
        args, kwargs = __args_kwargs
        return cls(
            *args,
            id=UUID(kwargs.pop("id")),
            color=Color.load(kwargs.pop("color")),
            screenshot_start_point=Point2D.load(kwargs.pop("screenshot_start_point")),
            screenshot_size=Size2D.load(kwargs.pop("screenshot_size")),
            frame=reader_cls.load(kwargs.pop("frame"))
            if excluded_frame is None
            else excluded_frame,
            mask=(
                reader_cls.load(mask_reader)
                if (mask_reader := kwargs.pop("mask") is not None)
                else None
            )
            if excluded_mask is None
            else excluded_mask,
            device=Device.load(kwargs.pop("device"))
            if excluded_device is None
            else excluded_device,
            **kwargs,
        )


__all__ = ("Template",)
