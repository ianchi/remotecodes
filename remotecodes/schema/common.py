"""General schema validations and helpers."""
from __future__ import annotations

import re
from typing import Any

import voluptuous as vol  # type: ignore
from remoteprotocols import ProtocolRegistry
from remoteprotocols import validators as val

REGISTRY = ProtocolRegistry()


def validate_source(value: Any) -> str:
    """Validate a codes source reference."""

    source = val.string_strict(value)

    if not re.match(r"^[a-z0-9][a-z0-9_\-]*\.[a-z0-9][a-z0-9_\-]*\.[0-9]+", source):
        raise vol.Invalid("Source must be in the form <brand>.<type>.<number>")

    return source


def validate_command(value: Any) -> str:
    """Validate a command or list of commands."""

    cmd = REGISTRY.parse_command(value)

    return cmd.command


VALID_CATEGORIES = [
    "air_conditioner",
    "audio_player",
    "av_receiver",
    "fan",
    "light",
    "projector",
    "settopbox",
    "speaker",
    "switch",
    "tuner",
    "tv",
    "video_player",
]
COMMAND_SCHEMA = vol.All(val.coerce_list(","), [validate_command], vol.Length(min=1))
NAME_SCHEMA = vol.Match(
    r"^[a-zA-Z0-9][a-zA-Z0-9_\- ]*$", msg="Invalid characters for name"
)


INFO_SCHEMA = vol.Schema(
    {
        vol.Required("brand"): val.string_strict,
        vol.Required("category"): vol.In(VALID_CATEGORIES),
        vol.Required("models"): vol.All([val.string_strict], vol.Length(min=1)),
        vol.Optional("notes", default=None): val.string_strict,
    }
)


CUSTOM_SCHEMA = vol.All({vol.Optional(NAME_SCHEMA): COMMAND_SCHEMA}, vol.Length(min=1))
