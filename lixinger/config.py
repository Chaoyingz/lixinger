from __future__ import annotations

import os
import pathlib

from dynaconf import Dynaconf, Validator

DEFAULT_SETTINGS_PATH: pathlib.Path = (
    pathlib.Path(__file__).resolve().parent / "settings.toml"
)
USER_SETTINGS_PATH: pathlib.Path = (
    pathlib.Path(
        os.getenv("LIXINGER_SETTINGS_PATH", "~/.config/lixinger/settings.toml")
    )
    .expanduser()
    .resolve()
)


settings_cast_map = {}


def cast(v: str) -> callable:
    """Decorator to register cast function for a setting."""

    def decorator(func) -> callable:
        settings_cast_map[v] = func
        return func

    return decorator


class TypedDynaconf(Dynaconf):
    url: str
    token: str


def get_validators() -> list[Validator]:
    """Get validators for settings.

    Cast settings to their types.
    """
    settings_types = vars(TypedDynaconf)["__annotations__"]
    return [
        Validator(key, cast=cast(settings_cast_map.get(key, type_)))
        for key, type_ in settings_types.items()
    ]


def load_settings(
    path: pathlib.Path = DEFAULT_SETTINGS_PATH,
    user_settings_path: pathlib.Path = USER_SETTINGS_PATH,
) -> TypedDynaconf:
    """Load settings from default settings and user settings file."""
    settings_files = (
        [path] if not user_settings_path.exists() else [path, user_settings_path]
    )
    default_settings = TypedDynaconf(
        settings_files=settings_files,
        merge_enabled=True,
        environments=True,
        validators=get_validators(),
        validate=True,
    )
    return default_settings


settings = load_settings()
