import math
from pathlib import Path

import toml


def load_streamlit_config(path: str = "./.streamlit/config.toml") -> dict:
    with Path(path).open() as f:
        return toml.load(f)
    return FileExistsError(f'File not found at "{path}"')


def get_alpha(pps: float, elapsed: float) -> float:
    """
    Calculate the alpha value for Christmas lights preview.

    :param pps: Pulse Per Second. The number of complete waves which should occur per second.
    :param elapsed: The elapsed time in seconds
    :return: Alpha value for the light strip preview.
    """
    return (math.sin((2 * math.pi * pps) * elapsed) + 1) / 2


def effects2frontend(effects: dict) -> dict:
    """Convert effects retrieved from db to the frontend version.

    :param effects: effects dictionary
    :return: frontend corresponding effects dictionary
    """
    eff = {}
    chasing_val = effects.pop("chasing")
    eff["breathing"] = round(effects.pop("breathing") * 60)
    eff["chasing"] = round(60 / chasing_val) if chasing_val else 0
    eff["sparkle"] = round(effects.pop("sparkle") * 100)
    return eff


def effects2backend(effects: dict) -> dict:
    """Convert effects retrieved from db to the frontend version.

    :param effects: effects dictionary
    :return: frontend corresponding effects dictionary
    """
    eff = {}
    chasing_val = effects.pop("chasing")
    eff["breathing"] = effects.pop("breathing") / 60
    eff["chasing"] = 60 / chasing_val if chasing_val else 0
    eff["sparkle"] = effects.pop("sparkle") / 100
    return eff
