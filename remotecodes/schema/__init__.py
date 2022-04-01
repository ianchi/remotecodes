"""Schema validations for codes files."""
from __future__ import annotations

import voluptuous as vol  # type: ignore

# flake8: noqa: F401
from .common import CUSTOM_SCHEMA, INFO_SCHEMA, validate_source
from .media_player import MEDIA_PLAYER_SCHEMA

CODES_SCHEMA = vol.All(
    {
        vol.Required("info"): INFO_SCHEMA,
        vol.Optional("media_player"): MEDIA_PLAYER_SCHEMA,
        vol.Optional("custom"): CUSTOM_SCHEMA,
    },
    vol.Length(min=2),
)
