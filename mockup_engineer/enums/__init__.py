from enum import Enum, StrEnum
from typing import Tuple, Sequence, Dict

from ..models import RestorableModel


class RestorableEnum(Enum):
    """
    Base class for restorable enums.
    """

    def dump(self) -> Tuple[Sequence, Dict]:
        """
        Serializes the current instance of the enumeration.

        :return: A tuple of positional arguments and a dictionary of named arguments.
        """
        return (self.value,), dict()

    @classmethod
    def load(cls, __args_kwargs: Tuple[Sequence, Dict], /) -> "RestorableEnum":
        """
        Deserializes the data and creates a new instance of the enumeration.

        :param __args_kwargs: A tuple of positional arguments and a dictionary of named arguments.
        :return: A new instance of the enumeration.
        """
        return cls(*__args_kwargs[0], **__args_kwargs[1])  # type: ignore


RestorableEnum: RestorableModel


class RestorableStrEnum(RestorableEnum, StrEnum):
    """
    Base class for string enums that can be saved and restored.
    """


__all__ = (
    "RestorableEnum",
    "RestorableStrEnum",
)
