import logging

from . import schemas

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def save_pattern(self, pattern: schemas.Pattern) -> str:
        pass
