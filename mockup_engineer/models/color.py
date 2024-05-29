from typing import Optional, Tuple, Sequence, Dict

from pydantic import validate_call, constr

from . import RestorableModel

EMOJI_MAPPER = {
    "⬛️": ["black", "graphite", "grey", "gray", "dark", "midnight"],
    "⬜️": ["white", "silver", "light", "platinum"],
    "🟫": ["brown"],
    "🟪": ["purple", "pink"],
    "🟦": ["blue"],
    "🟩": ["green", "coral"],
    "🟨": ["yellow", "gold"],
    "🟧": ["orange"],
    "🟥": ["red"],
}


class Color(RestorableModel):
    """
    Class representing a color.
    """

    __name: str
    __emoji: Optional[str]

    @validate_call
    def __init__(
        self,
        __name: constr(min_length=1),
        /,
        *,
        emoji: Optional[constr(min_length=1)] = None,
    ):
        """
        :param __name: The name of the color.
        :param emoji: Optional. The emoji representation of the color.
                      If not provided, it will be automatically determined
                      based on the color name.
        """
        self.__name = __name  # get, set
        self.__emoji = emoji  # get, set

    @property
    def name(self) -> str:
        """
        Name of the color.
        """

        return self.__name

    @name.setter
    @validate_call
    def name(self, __name: constr(min_length=1), /):
        """
        Set the name of the color.

        :param __name: The name of the color.
        """
        self.__name = __name

    @property
    def emoji(self) -> str:
        """
        Emoji representation of the color.

        If the emoji is not set explicitly, it will be automatically
        determined based on the color name.
        """
        if self.__emoji is not None:
            return self.__emoji

        for emoji, colors in EMOJI_MAPPER.items():
            if any(map(lambda color: color in self.__name.lower(), colors)):
                return emoji

        return "🔸"

    @emoji.setter
    @validate_call
    def emoji(self, __emoji: Optional[constr(min_length=1)], /):
        """
        Set the emoji representation of the color.

        :param __emoji: Optional. The emoji representation of the color.
                        If not provided, it will be automatically determined
                        based on the color name.
        """
        self.__emoji = __emoji

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, emoji={self.__emoji!r})"

    def dump(self) -> Tuple[Sequence, Dict]:
        return (self.__name,), dict(emoji=self.__emoji)


__all__ = ("Color",)
