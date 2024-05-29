from abc import ABC, abstractmethod
from typing import Tuple, Sequence, Dict, TypeVar, Type

T = TypeVar("T", bound="RestorableModel")


class RestorableModel(ABC):
    """
    Abstract base class for restorable models.
    """

    @abstractmethod
    def dump(self) -> Tuple[Sequence, Dict]:
        """
        Serializes the model.

        :return: A tuple of positional arguments and a dictionary of named arguments.
        """

    @classmethod
    def load(cls: Type[T], __args_kwargs: Tuple[Sequence, Dict], /) -> T:
        """
        Deserializes the data and creates a new instance of the model.

        :param __args_kwargs: A tuple of positional arguments and a dictionary of named arguments.
        :return: A new instance of the model.
        """
        return cls(*__args_kwargs[0], **__args_kwargs[1])  # type: ignore


__all__ = ("RestorableModel",)
