import json
from typing import Generator, Optional, Mapping

from pydantic import ConfigDict, validate_call, AnyHttpUrl

from .. import BaseRepository, _CONFIG_VALIDATOR
from ...exceptions.duplicate_identifier import DuplicateIdentifier
from ...models.device import Device
from ...models.template import Template
from ...readers.remote_http import BaseHTTPReader
from ...readers.remote_http.requests import RequestsReader


class RequestsRepository(BaseRepository):
    @validate_call
    def __init__(
        self,
        __url: AnyHttpUrl,
        /,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ):
        self.__url = __url
        self.__headers = headers or {}
        self.__reader = RequestsReader(f"{__url!s}/config.json", headers=headers)

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
                frame_args[0] = f"{self.__url!s}/{frame_args[0]}"
                frame = RequestsReader.load((frame_args, frame_kwargs))

                if template_data[1].get("mask") is not None:
                    mask_args, mask_kwargs = template_data[1].pop("mask")
                    mask_args = list(mask_args)
                    mask_args[0] = f"{self.__url!s}/{mask_args[0]}"
                    mask = RequestsReader.load((mask_args, mask_kwargs))
                else:
                    mask = None

                Template.load(
                    template_data,
                    reader_cls=RequestsReader,
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

                assert isinstance(template.frame, BaseHTTPReader)
                assert template.frame.url.startswith(self.__url)  # type: ignore
                if template.mask is not None:
                    assert isinstance(template.mask, BaseHTTPReader)
                    assert template.mask.url.startswith(self.__url)  # type: ignore

                template_data = template.dump(
                    exclude_device=True,
                    exclude_frame=True,
                    exclude_mask=True,
                )

                frame_args, frame_kwargs = template.frame.dump()
                frame_args = list(frame_args)
                frame_args[0] = frame_args[0].lstrip(str(self.__url))
                template_data[1]["frame"] = frame_args, frame_kwargs

                if template.mask is not None:
                    mask_args, mask_kwargs = template.mask.dump()
                    mask_args = list(mask_args)
                    mask_args[0] = mask_args[0].lstrip(str(self.__url))
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self.__url)!r}, headers={self.__headers!r})"


__all__ = ("RequestsRepository",)
