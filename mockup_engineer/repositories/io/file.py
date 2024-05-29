import json
from pathlib import Path
from typing import Generator

from pydantic import validate_call, ConfigDict

from .. import BaseRepository, _CONFIG_VALIDATOR
from ...exceptions.duplicate_identifier import DuplicateIdentifier
from ...models.device import Device
from ...models.template import Template
from ...readers.io.file import FileReader


class FileRepository(BaseRepository):
    """
    A repository that handles file-based configuration and device operations.
    """

    @validate_call
    def __init__(self, __path: Path, /):
        """
        :param __path: The path to the repository directory
                       containing the configuration file.
        """
        self.__path = __path
        self.__reader = FileReader(__path.joinpath("config.json"))

    @validate_call
    def _load_config(
        self, __config: _CONFIG_VALIDATOR, /
    ) -> Generator[Device, None, None]:
        device_ids = list()
        template_ids = list()

        for device_data in __config:
            if device_data[1]["id"] in device_ids:
                raise DuplicateIdentifier(
                    "Can't assign device to repository because "
                    f"device with id {device_data[1]['id']!r} already exists"
                )
            else:
                device_ids.append(device_data[1]["id"])

            templates_data = device_data[1].pop("templates")
            device = Device.load(device_data)

            for template_data in templates_data:
                if template_data[1]["id"] in template_ids:
                    raise DuplicateIdentifier(
                        "Can't assign template to repository because "
                        f"template with id {template_data[1]['id']!r} already exists"
                    )
                else:
                    template_ids.append(template_data[1]["id"])

                frame_args, frame_kwargs = template_data[1].pop("frame")
                frame_args = list(frame_args)
                frame_args[0] = str(self.path.joinpath(frame_args[0]))  # type: ignore
                frame = FileReader.load((frame_args, frame_kwargs))

                if template_data[1].get("mask") is not None:
                    mask_args, mask_kwargs = template_data[1].pop("mask")
                    mask_args = list(mask_args)
                    mask_args[0] = str(self.path.joinpath(mask_args[0]))  # type: ignore
                    mask = FileReader.load((mask_args, mask_kwargs))
                else:
                    mask = None

                Template.load(
                    template_data,
                    reader_cls=FileReader,
                    excluded_device=device,
                    excluded_frame=frame,
                    excluded_mask=mask,
                )

            yield device

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def _dump_config(self, *__devices: Device) -> _CONFIG_VALIDATOR:
        config = list()
        device_ids = list()
        template_ids = list()

        for device in __devices:
            if device.id in device_ids:
                raise DuplicateIdentifier(
                    "Can't assign device to repository because "
                    f"device with id {device.id!r} already exists"
                )
            else:
                device_ids.append(device.id)

            device_data = device.dump()
            device_data[1]["templates"] = list()

            for template in device:
                if template.id in template_ids:
                    raise DuplicateIdentifier(
                        "Can't assign template to repository because "
                        f"template with id {template.id!r} already exists"
                    )
                else:
                    template_ids.append(template.id)

                assert isinstance(template.frame, FileReader)
                assert template.frame.path.is_relative_to(self.path)  # type: ignore
                if template.mask is not None:
                    assert isinstance(template.mask, FileReader)
                    assert template.mask.path.is_relative_to(self.path)  # type: ignore

                template_data = template.dump(
                    exclude_device=True,
                    exclude_frame=True,
                    exclude_mask=True,
                )

                frame_args, frame_kwargs = template.frame.dump()
                frame_args = list(frame_args)
                frame_args[0] = str(Path(frame_args[0]).relative_to(self.path))  # type: ignore
                template_data[1]["frame"] = frame_args, frame_kwargs

                if template.mask is not None:
                    mask_args, mask_kwargs = template.mask.dump()
                    mask_args = list(mask_args)
                    mask_args[0] = str(Path(mask_args[0]).relative_to(self.path))  # type: ignore
                    template_data[1]["mask"] = mask_args, mask_kwargs
                else:
                    template_data[1]["mask"] = None

                device_data[1]["templates"].append(template_data)

            device_data[1]["templates"] = tuple(device_data[1]["templates"])

            config.append(device_data)

        return tuple(config)

    def _read_config(self) -> _CONFIG_VALIDATOR:
        with self.__reader as reader:
            return json.loads(reader.read())

    @validate_call
    def _write_config(self, __config: _CONFIG_VALIDATOR, /):
        with self.__reader as reader:
            reader.write(json.dumps(__config).encode())

    @property
    def path(self) -> Path:
        return self.__path

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__path!r})"


__all__ = ("FileRepository",)
