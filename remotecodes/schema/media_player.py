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

NUMBERS_SCHEMA = vol.Schema(
    {
        vol.Required(0): COMMAND_SCHEMA,
        vol.Required(1): COMMAND_SCHEMA,
        vol.Required(2): COMMAND_SCHEMA,
        vol.Required(3): COMMAND_SCHEMA,
        vol.Required(4): COMMAND_SCHEMA,
        vol.Required(5): COMMAND_SCHEMA,
        vol.Required(6): COMMAND_SCHEMA,
        vol.Required(7): COMMAND_SCHEMA,
        vol.Required(8): COMMAND_SCHEMA,
        vol.Required(9): COMMAND_SCHEMA,
    }
)

MEDIA_SCHEMA = vol.Schema(
    {
        vol.Optional("play"): COMMAND_SCHEMA,
        vol.Optional("pause"): COMMAND_SCHEMA,
        vol.Optional("play_pause"): COMMAND_SCHEMA,
        vol.Optional("stop"): COMMAND_SCHEMA,
        vol.Inclusive(
            "next_track", "track", msg="Must also define 'next_track'"
        ): COMMAND_SCHEMA,
        vol.Inclusive(
            "prev_track", "track", msg="Must also define 'prev_track'"
        ): COMMAND_SCHEMA,
        vol.Inclusive(
            "fast_forward", "seek", msg="Must also define 'fast_forward'"
        ): COMMAND_SCHEMA,
        vol.Inclusive(
            "rewind", "seek", msg="Must also define 'rewind'"
        ): COMMAND_SCHEMA,
    }
)

NAVIGATE_SCHEMA = vol.Schema(
    {
        vol.Inclusive("up", "seek", msg="Must also define 'up'"): COMMAND_SCHEMA,
        vol.Inclusive("down", "seek", msg="Must also define 'down'"): COMMAND_SCHEMA,
        vol.Inclusive("left", "seek", msg="Must also define 'left'"): COMMAND_SCHEMA,
        vol.Inclusive("right", "seek", msg="Must also define 'right'"): COMMAND_SCHEMA,
        vol.Optional("select"): COMMAND_SCHEMA,
        vol.Optional("back"): COMMAND_SCHEMA,
    }
)

MEDIA_PLAYER_SCHEMA = vol.All(
    {
        vol.Optional("power"): POWER_SCHEMA,
        vol.Optional("volume"): VOLUME_SCHEMA,
        vol.Optional("sources"): SOURCES_SCHEMA,
        vol.Optional("sound_modes"): SOUND_MODES_SCHEMA,
        vol.Optional("numbers"): NUMBERS_SCHEMA,
        vol.Optional("media"): MEDIA_SCHEMA,
        vol.Optional("navigate"): NAVIGATE_SCHEMA,
    },
    vol.Length(min=1),
)
