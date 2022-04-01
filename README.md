![CI workflow](https://github.com/ianchi/remotecodes/actions/workflows/ci.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/remotecodes.svg)](https://pypi.org/project/remotecodes/)

# remotecodes

`remotecodes` is a curated repository of crowd-sourced IR / RF remote codes intended to be useful in home automation scenarios.

Thus codes are not just an arbitrary list of key-value pairs, but must adhere to a strict schema per device domain, that gives
functional meaning to each code, which can later be interpreted by a higher level integration (for instance in
[Home Assistant](https://www.home-assistant.io/)).

All codes are written using [remoteprotocols](https://github.com/ianchi/remoteprotocols#remote-command-strings) command notation
and all it's [supported protocols](https://github.com/ianchi/remoteprotocols/blob/master/PROTOCOLS.md#list-of-supported-protocols)
are available. See links for details.

A codes file is always referenced as `brand.category.seq_number`

## Usage

Codes files can be used directly from their yaml form.
If consumed from _python_, there are some helper functions available

```python
from remotecodes import get_codes
from remotecodes.schema import media_player, validate_source


#intended as voluptuous validator for source string format
source = validate_source("acme.tv.001")

# find the correct codes file, validate it and return it as a dict
# an optional <domain> can be marked as required
# optional extra root folders can be added to the search. They take priority over built-in ones.
codes = get_codes(source, "media_player", ["my_extra_codes_root"])
```

### Command line

To batch validate all codes files and their folder structure:

```bash
remotecodes validate <codes_root_folder>
```

# Contributing Codes

Codes comes from user contribution, so you are encouraged to share your files.

## Hierarchy

- Codes files are organized in folders that must adhere to the pattern:
  `brand/category/`
- Files within each folder must be named according to the pattern: `brand.category.seq_number.yaml`
- The brand and category must be consistent among folder, filename, file content

## Schema

All files must have a required `info` section and at least one domain section that follows it's respective schema. A device can have commands for more than one domain (i.e. a `fan` and a `light`).
Additionally a free `custom` section can be added to include extra commands not tied to a well defined function.

### Section `info`

```yaml
info: #required
    brand: Acme #required
    models: #required, min length: 1
        - Model A
    category: tv #required
    notes: < #optional
        This codes where learned and tested

# At least one domain section required
```

_brand_ and _category_ are validated against filename and path.

_category_ must be one of:

- air_conditioner
- audio_player
- av_receiver
- fan
- light
- projector
- settopbox
- speaker
- switch
- tuner
- tv
- video_player

### Commands

All codes are written using [remoteprotocols](https://github.com/ianchi/remoteprotocols#remote-command-strings) command notation
and all it's [supported protocols](https://github.com/ianchi/remoteprotocols/blob/master/PROTOCOLS.md#list-of-supported-protocols)
are available. See links for details.

This is often done as a single string, but if a multi command sequence is needed it can be expressed as an array of commands.
After validation all entries are converted to arrays.

```yaml
#single command
some_function: nec:0xFE:0x7E

#multi sequence
other_function:
  - nec:0x7E:0xA2
  - nec:0x7E:0xA3
```

### Section `media_player`

Used for any kind of media device. All subsections are optional, but at least one must be present.

```yaml
media_player: #cannot be empty
  power: #optional, but cannot be empty
    power_on: <command> #optional, required if 'off' is set
    power_off: <command> #optional, required if 'on' is set

    power_toggle: <command> #optional

  volume: #optional, but cannot be empty
    up: <command> #optional, required if 'down' is set
    down: <command> #optional, required if 'up' is set

    mute_on: <command> #optional, required if 'off' is set
    mute_off: <command> #optional, required if 'on' is set

    mute_toggle: <command> #optional

  sources: #optional, min length: 1
    # source names are device dependant. Valid characters: [azAZ09_- ], cannot start with a symbol
    - source_1: <command>
    - source_2: <command>

  sound_modes: #optional, min length: 1
    # modes names are device dependant. Valid characters: [azAZ09_- ], cannot start with a symbol
    - mode_1: <command>
    - mode_2: <command>

  numbers: #optional, if set ALL numbers are required
    0: <command> #required
    1: <command> #required
    2: <command> #required
    3: <command> #required
    4: <command> #required
    5: <command> #required
    6: <command> #required
    7: <command> #required
    8: <command> #required
    9: <command> #required

  media: #optional, but cannot be empty
    play: <command> #optional
    pause: <command> #optional
    play_pause: <command> #optional

    stop: <command> #optional

    next_track: <command> #optional, required if 'prev' is set
    prev_track: <command> #optional, required if 'next' is set

    fast_forward: <command> #optional, required if 'rewind' is set
    rewind: <command> #optional, required if 'fast_forward' is set

  navigate: #optional, but cannot be empty
    up: <command> #optional, required if 'down' is set
    down: <command> #optional, required if 'up' is set

    left: <command> #optional, required if 'right' is set
    right: <command> #optional, required if 'left' is set

    select: <command> #optional
    back: <command> #optional


    # clear_playlist, shuffle_set, repeat_set,
```

### Section `fan`

Used for fan device.

```yaml
#TBD
```

### Section `air_conditioner`

Used for air conditioner device.

```yaml
#TBD
```

### Section `light`

Used for light control functions.

```yaml
#TBD
```

### Section `switch`

Used for to control simple switching functions.

```yaml
#TBD
```

### Section `custom`

Used for arbitrary functions that not fall into any other category.
It is discuraged as it's unstandardized nature cannot be used by higher order components, but can be useful for manual use cases.

```yaml
custom:
  # function names are completely custom. Valid characters: [azAZ09_- ], cannot start with a symbol
  function1: <command>
  function2: <command>
```
