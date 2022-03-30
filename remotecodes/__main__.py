"""Main program for command line utility."""

from __future__ import annotations

import argparse
import logging as log
import pathlib
import sys

import voluptuous as vol  # type: ignore

from . import __version__, validate_codes_file

CMD_VALIDATE_CODES = "validate"

PROGRAM_NAME = "remotecodes"


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Convert command line arguments in an object."""

    options_parser = argparse.ArgumentParser(add_help=False)
    options_parser.add_argument(
        "-v", "--version", help="Show version information.", action="store_true"
    )
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=f"{PROGRAM_NAME} v{__version__}",
        parents=[options_parser],
    )

    subparsers = parser.add_subparsers(
        help="Command to run:", dest="command", metavar="command"
    )
    subparsers.required = True

    parser_config = subparsers.add_parser(
        CMD_VALIDATE_CODES, help="Validate remote codes definition file."
    )
    parser_config.add_argument("folder", help="Root folder of definitions.", nargs=1)

    return parser.parse_args(argv[1:])


def cmd_validate_codes(root: str) -> int:
    """Run validate command."""

    root_path = pathlib.Path(root).resolve()
    if not root_path.exists() or not root_path.is_dir():
        raise NotADirectoryError(root_path.as_posix())

    for file in root_path.glob("**/*.yaml"):

        try:
            validate_codes_file(file)

        except vol.MultipleInvalid as errs:
            log.error("Invalid format in file %s", file.name)
            for err in errs.errors:
                log.error(err)
                # print(err.__dict__)
            return 1

        except vol.Invalid as err:
            log.error("Invalid format in file %s", file.name)
            log.error(err)
            return 1

    print("Codes definitions are OK")
    return 0


def run(argv: list[str]) -> int:
    """Run the requested command."""

    if sys.version_info < (3, 8, 0):
        log.error("You need Python 3.8+ to run %s", PROGRAM_NAME)
        return 1

    args = parse_args(argv)

    if args.version:
        print(f"Version: {__version__}")

    if args.command == CMD_VALIDATE_CODES:
        return cmd_validate_codes(args.folder[0])

    return 0


def main() -> int:
    """Run main entry point for command line."""

    log.basicConfig(format="%(levelname)s: %(message)s")
    try:
        return run(sys.argv)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
