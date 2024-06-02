from abc import abstractmethod, ABC
from pathlib import Path
from typing import Protocol, Self, Union, Optional

from pydantic import ConfigDict, validate_call, SkipValidation

from .. import FileReader
from ..models.point2d import Point2D
from ..models.size2d import Size2D
from ..models.template import Template
from ..readers import Reader, BaseReader


class Renderer(Protocol):
    """
    A protocol for working with images.
    """

    def __init__(self, __size: Size2D, /):
        """
        Creates new transparent image

        :param __size: The size of the renderers as a `Size2D` object.
        """

    def resize(self, __size: Size2D, /):
        """
        Resizes the image to the specified size.

        :param __size: The new size of the renderers.
        """

    def rotate(self, __angle: float, /):
        """
        Rotates the image by the specified angle.

        :param __angle: The angle in degrees to rotate the renderers.
        """

    def put_image(
        self,
        __image: "Renderer",
        __start_point: Point2D = Point2D(1, 1),
        /,
        *,
        mask: Optional["Renderer"] = None,
    ):
        """
        Puts the specified image onto the current image.

        :param __image: The image to be put onto the current image.
        :param __start_point: The starting point for the image to be put.
        :param mask: An optional mask image to be used for the operation.
        """

    def put_alpha(self, __image: "Renderer", /):
        """
        Puts the alpha channel from the specified monochrome image.

        :param __image: The image to put the alpha channel from.
        """

    @classmethod
    def from_bytes(cls, __data: bytes, /) -> Self:
        """
        Creates a new image from the specified byte data.

        :param __data: The byte data representing the image.

        :return: A new `Renderer` object.
        """

    def to_bytes(self) -> bytes:
        """
        Converts the image to byte data in PNG format.

        :return: The byte data representing the image in PNG format.
        """

    @classmethod
    def from_reader(cls, __reader: Reader, /) -> Self:
        """
        Creates a new image from the specified reader.

        :param __reader: The reader to read the image from.

        :return: A new `Renderer` object.
        """

    @property
    @abstractmethod
    def size(self) -> Size2D:
        """
        The size of the image as a `Size2D` object.
        """

    def copy(self) -> Self:
        """
        Creates a deep copy of the image.

        :return: A new `Renderer` object that is a copy of the current image.
        """

    @classmethod
    def render(
        cls, __template: Template, __screenshot: Union["Renderer", Reader, Path], /
    ):
        """
        Renders the specified template from a screenshot.

        :param __template: The template to be rendered.
        :param __screenshot: The screenshot to render the template from, either as an `Renderer` object or a `Reader`.

        :return: A new `Renderer` object containing the rendered template.
        """


class BaseRenderer(Renderer, ABC):
    def copy(self) -> Self:
        return self.__class__.from_bytes(self.to_bytes())

    @classmethod
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def from_reader(cls, __reader: BaseReader, /) -> SkipValidation[Self]:  # noqa
        return cls.from_bytes(__reader.read())

    @classmethod
    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def render(  # noqa
        cls,
        __template: Template,
        __screenshot: Union[SkipValidation["Renderer"], BaseReader, Path],
        /,
        disable_rotate: bool = False,
        constrain_proportions: bool = False,
    ):
        assert __template.device is not None

        if isinstance(__screenshot, BaseReader):
            screenshot = cls.from_reader(__screenshot)
        elif isinstance(__screenshot, Path):
            with FileReader(__screenshot) as screenshot_reader:
                screenshot = cls.from_reader(screenshot_reader)
        else:
            screenshot = __screenshot.copy()

        with __template.frame as template_frame:
            frame = cls.from_reader(template_frame)

        placeholder = cls(frame.size)

        screenshot_orientation = screenshot.size.width <= screenshot.size.height
        frame_orientation = frame.size.width <= frame.size.height

        if (
            not disable_rotate
            and screenshot_orientation != frame_orientation
            and __template.device.can_rotate
        ):
            screenshot.rotate(-90)
        if constrain_proportions:
            screenshot_placeholder = cls(__template.screenshot_size)
            screenshot_scale = min(
                __template.screenshot_size.width / screenshot.size.width,
                __template.screenshot_size.height / screenshot.size.height,
            )
            screenshot.resize(
                Size2D(
                    int(screenshot.size.width * screenshot_scale) or 1,
                    int(screenshot.size.height * screenshot_scale) or 1,
                )
            )
            screenshot_placeholder.put_image(
                screenshot,
                Point2D(
                    (screenshot_placeholder.size.width - screenshot.size.width) // 2,
                    (screenshot_placeholder.size.height - screenshot.size.height) // 2,
                ),
            )
            screenshot = screenshot_placeholder

        else:
            screenshot.resize(__template.screenshot_size)

        placeholder.put_image(screenshot, __template.screenshot_start_point)
        placeholder.put_image(frame, mask=frame)

        if __template.mask:
            mask = Renderer.from_reader(__template.mask)
            placeholder.put_alpha(mask)

        if (
            not disable_rotate
            and screenshot_orientation != frame_orientation
            and __template.device.can_rotate
        ):
            placeholder.rotate(90)

        return placeholder


__all__ = ("Renderer", "BaseRenderer")
