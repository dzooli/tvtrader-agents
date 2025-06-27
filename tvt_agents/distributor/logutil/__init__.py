"""
A helper module for flexible logging inside inherited classes.
"""

import logging
from attrs import define, field, validators


@define
class LoggingMixin:
    """Use this logger trait where needed."""

    _logger: logging.Logger = (
        field(
            init=True,
            validator=validators.optional(validators.instance_of(logging.Logger)),
        ),
    )

    def __init__(self):
        self._logger: logging.Logger

    @property
    def logger(self) -> logging.Logger:
        """The underlying logger."""
        try:
            return self._logger
        except AttributeError:
            raise AttributeError(
                "Logger not set! Please set the logger before using it."
            )
        except TypeError:
            raise TypeError("Logger must be an instance of logging.Logger, not None.")

    @logger.setter
    def logger(self, logger: logging.Logger):
        """Set the logger."""
        if not isinstance(logger, logging.Logger):
            raise TypeError("Logger must be an instance of logging.Logger.")
        if not logger.hasHandlers():
            raise ValueError("Logger must have at least one handler attached.")
        if not logger.level:
            raise ValueError("Logger must have a valid logging level set.")
        if not logger.name:
            raise ValueError("Logger must have a name set.")
        self._logger = logger

    def log(self, level: int, item) -> bool:
        """Use the logger."""
        try:
            logger_fn = getattr(self._logger, str(logging.getLevelName(level)).lower())
        except AttributeError:
            return False
        logger_fn(item)
        return True
