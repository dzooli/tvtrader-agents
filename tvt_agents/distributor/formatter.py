"""
This module contains the formatter interface and default formatter implementation.
"""

from abc import ABC, abstractmethod


class IFormatter(ABC):
    """
    Interface for message formatters.
    """

    @abstractmethod
    def format(self, message: str) -> str:
        """
        Formats the given message.

        Args:
            message (str): The message to format.

        Returns:
            str: The formatted message.
        """
        pass


class DefaultFormatter(IFormatter):
    """
    Default formatter that returns the message as is.
    """

    def format(self, message: str) -> str:
        """
        Returns the message as is.

        Args:
            message (str): The message to format.

        Returns:
            str: The original message.
        """
        return message
