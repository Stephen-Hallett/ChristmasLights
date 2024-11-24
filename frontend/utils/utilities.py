from pathlib import Path

import toml


def load_streamlit_config(path: str = "./.streamlit/config.toml") -> dict:
    with Path(path).open() as f:
        return toml.load(f)
    return FileExistsError(f'File not found at "{path}"')
