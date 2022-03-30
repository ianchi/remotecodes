"""Schema validations for media_player."""

from __future__ import annotations

import voluptuous as vol  # type:ignore

from .common import COMMAND_SCHEMA, NAME_SCHEMA

POWER_SCHEMA = vol.All(
    {
        vol.Inclusive(
            "power_on", "power", msg="Must also define 'power_on'"
        ): COMMAND_SCHEMA,
        vol.Inclusive(
            "power_off", "power", msg="Must also define 'power_off'"
        ): COMMAND_SCHEMA,
        vol.Optional("power_toggle"): COMMAND_SCHEMA,
    },
    vol.Length(min=1, msg="Must have either toggle or on/off"),
)

VOLUME_SCHEMA = vol.Schema(
    {
        vol.Inclusive("up", "level", msg="Must also define 'up'"): COMMAND_SCHEMA,
        vol.Inclusive("down", "level", msg="Must also define 'down'"): COMMAND_SCHEMA,
        vol.Inclusive(
            "mute_on", "mute", msg="Must also define 'mute_on'"
        ): COMMAND_SCHEMA,
        vol.Inclusive(
            "mute_off", "mute", msg="Must also define 'mute_off'"
        ): COMMAND_SCHEMA,
        vol.Optional("mute_toggle"): COMMAND_SCHEMA,
        # TODO: volume_set
    },
)

SOURCES_SCHEMA = vol.All(
    {vol.Optional(NAME_SCHEMA): COMMAND_SCHEMA},
    vol.Length(min=1, msg="Must have at least one source"),
)

SOUND_MODES_SCHEMA = vol.All(
    {vol.Optional(NAME_SCHEMA): COMMAND_SCHEMA},
    vol.Length(min=1, msg="Must have at least one sound mode"),
)


MEDIA_PLAYER_SCHEMA = vol.All(
    {
        vol.Optional("power"): POWER_SCHEMA,
        vol.Optional("volume"): VOLUME_SCHEMA,
        vol.Optional("sources"): SOURCES_SCHEMA,
        vol.Optional("sound_modes"): SOUND_MODES_SCHEMA,
    },
    vol.Length(min=1),
)
