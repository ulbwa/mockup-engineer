from datetime import date
from typing import (
    Optional,
    List,
    TYPE_CHECKING,
    Iterator,
    Sequence,
    Tuple,
    Dict,
    Self,
    Iterable,
)
from uuid import UUID

from pydantic import validate_call, ConfigDict, UUID4, constr, SkipValidation

from . import RestorableModel
from .size2d import Size2D
from ..enums.device_type import DeviceType
from ..exceptions.template_not_found import TemplateNotFound

if TYPE_CHECKING:
    from .template import Template


_MANUFACTURER_VALIDATOR = constr(min_length=1)
_NAME_VALIDATOR = constr(min_length=1)


class Device(RestorableModel, Iterable["Template"]):
    """
    Class representing a device.
    """

    __id: UUID
    __manufacturer: str
    __name: str
    __type: DeviceType
    __resolution: Size2D
    __released_at: Optional[date]
    __can_rotate: bool

    __templates: List["Template"]

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(
        self,
        *,
        id: UUID4,  # noqa
        manufacturer: _MANUFACTURER_VALIDATOR,
        name: _NAME_VALIDATOR,
        type: DeviceType,  # noqa
        resolution: Size2D,
        released_at: Optional[date] = None,
        can_rotate: bool = False,
    ):
        """
        :param id: The unique identifier of the device.
        :param manufacturer: The manufacturer of the device.
        :param name: The name of the device.
        :param type: The type of the device.
        :param resolution: The resolution of the device.
        :param released_at: Optional. The release date of the device.
        :param can_rotate: Optional. Indicates if the device can rotate.
        """
        self.__id = id  # get, set
        self.__manufacturer = manufacturer  # get, set
        self.__name = name  # get, set
        self.__type = type  # get, set
        self.__resolution = resolution  # get, set
        self.__released_at = released_at  # get, set
        self.__can_rotate = can_rotate
        self.__templates = list()

    @property
    def id(self) -> UUID:
        """
        Unique identifier of the device.
        """
        return self.__id

    @id.setter
    @validate_call
    def id(self, __id: UUID4, /) -> None:
        """
        Set the unique identifier of the device.

        :param __id: The unique identifier of the device.
        """
        self.__id = __id

    @property
    def manufacturer(self) -> str:
        """
        Manufacturer of the device.
        """
        return self.__manufacturer

    @manufacturer.setter
    @validate_call
    def manufacturer(self, __manufacturer: _MANUFACTURER_VALIDATOR, /):
        """
        Set the manufacturer of the device.

        :param __manufacturer: The manufacturer of the device.
        """
        self.__manufacturer = __manufacturer

    @property
    def name(self) -> str:
        """
        Name of the device.
        """
        return self.__name

    @name.setter
    @validate_call
    def name(self, __name: _NAME_VALIDATOR, /):
        """
        Set the name of the device.

        :param __name: The name of the device.
        """
        self.__name = __name

    @property
    def type(self) -> DeviceType:
        """Type of the device."""
        return self.__type

    @type.setter
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def type(self, __type: DeviceType, /):
        """
        Set the type of the device.

        :param __type: The type of the device.
        """
        self.__type = __type

    @property
    def resolution(self) -> Size2D:
        """
        Resolution of the device.
        """
        return self.__resolution

    @resolution.setter
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def resolution(self, __resolution: Size2D, /):
        """
        Set the resolution of the device.

        :param __resolution: The resolution of the device.
        """
        self.__resolution = __resolution

    @property
    def released_at(self) -> Optional[date]:
        """
        Release date of the device.
        """
        return self.__released_at

    @released_at.setter
    @validate_call
    def released_at(self, __released_at: Optional[date], /):
        """
        Set the release date of the device.

        :param __released_at: Optional. The release date of the device.
        """
        self.__released_at = __released_at

    @property
    def can_rotate(self) -> bool:
        """
        Whether the device can rotate. Indicates if the device can rotate.
        """
        return self.__can_rotate

    @can_rotate.setter
    @validate_call
    def can_rotate(self, __can_rotate: bool, /):
        """
        Set whether the device can rotate.

        :param __can_rotate: Whether the device can rotate.
        """
        self.__can_rotate = __can_rotate

    def __iter__(self) -> Iterator["Template"]:
        return iter(self.__templates)

    @property
    def templates(self) -> Sequence["Template"]:
        """
        List of templates associated with the device.
        """
        return tuple(self)

    def get_template_by_id(self, __id: UUID4, /) -> "Template":
        """
        Get a template associated with the device by its ID.

        :param __id: The ID of the template.

        :return: The template associated with the device.
        :raises TemplateNotFound: If the template with the specified ID is not found.
        """
        for template in self:
            if template.id == __id:
                return template
        raise TemplateNotFound(f"Template with id {__id!r} is not found")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"manufacturer={self.manufacturer!r}, "
            f"name={self.name!r}, "
            f"type={self.type!r}, "
            f"resolution={self.resolution!r}, "
            f"released_at={self.released_at!r}, "
            f"can_rotate={self.can_rotate!r})"
        )

    def dump(self) -> Tuple[Sequence, Dict]:
        return tuple(), dict(
            id=str(self.__id),
            manufacturer=self.__manufacturer,
            name=self.__name,
            type=self.__type.dump(),  # type: ignore
            resolution=self.__resolution.dump(),
            released_at=self.__released_at.isoformat() if self.__released_at else None,
            can_rotate=self.__can_rotate,
        )

    @classmethod
    @validate_call
    def load(cls, __args_kwargs: Tuple[Sequence, Dict], /) -> SkipValidation[Self]:
        args, kwargs = __args_kwargs
        if (released_at := kwargs.pop("released_at")) is not None:
            released_at = date.fromisoformat(released_at)
        return cls(
            *args,
            id=UUID(kwargs.pop("id")),
            type=DeviceType.load(kwargs.pop("type")),  # type: ignore
            resolution=Size2D.load(kwargs.pop("resolution")),
            released_at=released_at,
            **kwargs,
        )


from .template import Template  # noqa

Device.get_template_by_id = validate_call(Device.get_template_by_id)

__all__ = ("Device",)
