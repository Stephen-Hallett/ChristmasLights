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
