import json
from typing import Generator

from pydantic import ConfigDict, validate_call

from .. import BaseRepository, _CONFIG_VALIDATOR
from ...exceptions.duplicate_identifier import DuplicateIdentifier
from ...models.device import Device
from ...models.template import Template
from ...readers.io.bytesio import BytesIOReader


class BytesIORepository(BaseRepository):
    """
    A repository that handles BytesIO-based configuration and device operations.
    """

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def __init__(self, __reader: BytesIOReader, /):
        """
        :param __reader: The BytesIOReader object used to read
                         configurations from a BytesIO stream.
        """
        self.__reader = __reader

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

                Template.load(
                    template_data,
                    reader_cls=BytesIOReader,
                    excluded_device=device,
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

                assert isinstance(template.frame, BytesIOReader)
                if template.mask is not None:
                    assert isinstance(template.mask, BytesIOReader)

                device_data[1]["templates"].append(template.dump(exclude_device=True))

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__reader!r})"


__all__ = ("BytesIORepository",)
