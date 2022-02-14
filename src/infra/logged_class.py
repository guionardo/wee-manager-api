import logging


class LoggedClass:

    def __init__(self) -> None:
        self.LOG = logging.getLogger(self.__class__.__name__)
