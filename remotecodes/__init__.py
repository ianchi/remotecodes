"""Managa remote codes files."""

from __future__ import annotations

import codecs
import pathlib
import re
from typing import Any

import voluptuous as vol  # type:ignore
import yaml

from .schema import CODES_SCHEMA, validate_source

__version__ = "0.0.1"


def get_codes(
    source: str, domain: str | None = None, custom_paths: list[str] | None = None
) -> dict[str, Any]:
    """Fetch and validate a codes file.

    <source> brand.type.number || brand:model
    <paths> Search first in the provided root folders, before builtin codes
    <domain> raise error if domain is not present
    """

    paths: list[pathlib.Path] = []
    if custom_paths:
        paths = [pathlib.Path(path).resolve() for path in custom_paths]

    paths.append(pathlib.Path(__file__).parent / "codes")

    parts = source.split(".")

    validate_source(source)

    file: pathlib.Path | None

    for root_path in paths:

        if not root_path.exists() or not root_path.is_dir():
            raise NotADirectoryError(root_path.as_posix())

        file = root_path / "/".join(parts[:2]) / (source + ".yaml")

        if file.exists():
            break
        file = None

    if file is None:
        raise FileNotFoundError()

    data = validate_codes_file(file)
    if domain and domain not in data:
        raise vol.Invalid(
            f"No codes definition for domain '{domain}' in file {file.as_posix()}"
        )

    return data


def validate_codes_file(file: pathlib.Path) -> dict[str, Any]:
    """Load and validates codes file."""

    # Validate Path
    folders = file.parts[-3:-1]
    name = file.name.split(".")[:-2]

    if folders[0] != name[0] or folders[1] != name[1]:
        raise vol.Invalid(
            f"File name ({file.name}) doesn't match folder structure ({'/'.join(folders)})"
        )

    re_path = re.compile(r"^[a-z0-9][a-z0-9_\-]*$")

    if not re_path.match(folders[0]) or not re_path.match(folders[1]):
        raise vol.Invalid(
            f"Folder names must be only lowercases, digits or _ - but got '{'/'.join(folders)}'"
        )

    # Validate content
    try:
        with codecs.open(file.as_posix(), "r", encoding="utf-8") as f_handle:
            data = yaml.safe_load(f_handle)
    except yaml.MarkedYAMLError as err:
        mark = err.problem_mark
        if mark:
            raise vol.Invalid(
                f"Error parsing yaml file {file}[{mark.line + 1}:{mark.column + 1}]: {err.problem}"
            )
        raise err

    data = CODES_SCHEMA(data)

    if data["info"]["brand"].lower() != name[0].lower():
        raise vol.Invalid(
            f"Brand '{data['info']['brand']}' doesn't match filename ({name[0]})"
        )
    if data["info"]["category"].lower() != name[1].lower():
        raise vol.Invalid(
            f"Category '{data['info']['category']}' doesn't match filename ({name[1]})"
        )

    return data  # type: ignore
