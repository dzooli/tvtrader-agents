# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, Future
import concurrent.futures as mod_futures
from typing import TypeVar

from ..base import AbstractDistributorEndpoint

CAbstractDistributionTarget = TypeVar("CAbstractDistributionTarget", bound="AbstractDistributionTarget")


class AbstractDistributionTarget(AbstractDistributorEndpoint, metaclass=ABCMeta):
    @abstractmethod
    async def on_message(self, message: str):
        self.process(message)

    @abstractmethod
    def process(self, message: str):
        ...


CThreadedDistributionTarget = TypeVar("CThreadedDistributionTarget", bound="ThreadedDistributionTarget")


class ThreadedDistributionTarget(AbstractDistributionTarget):
    """ThreadPool based distribution target base class.

    Usable as a base class for processing multiple events (task, messages) using threading.
    In derived classes you could setup callback functions to process the result of the process() method.
    """

    def __init__(self, poolsize: int = 10, initializer: Callable | None = None):
        """Initializes the class

        Args:
            poolsize (int, optional): Size of the thread-pool. Defaults to 10.
            initializer (Callable | None, optional): Custom initialization function for the processing threads. Defaults to None.
        """
        self._pool = ThreadPoolExecutor(poolsize, initializer=initializer if initializer is not None else None)

    def open(self):
        """Opened and started by the constructor."""

    def _check_complete(self, result: Future):
        """Check the thread status for completion, timeout or cancellation

        Handles the thread execution status with calling the related callback function.

        Args:
            result: (Future): The result of the threaded task execution.
        """
        res = None
        try:
            res = result.result()
        except mod_futures.TimeoutError:
            return self.on_timeout(res)
        except mod_futures.CancelledError:
            return self.on_cancel(res)
        except BaseException as exc:
            return self.on_error(exc)
        self.on_complete(res)

    @abstractmethod
    def on_complete(self, result):
        """Callback for completed tasks

        Override it based on your processing needs.

        Args:
            result (Any): The result of the processing.
        """

    @abstractmethod
    def on_timeout(self, result):
        """Callback for timed-out threads

        Args:
            result (Any): The result of the timed-out processing thread.
        """

    @abstractmethod
    def on_cancel(self, result):
        """Callback for the cancelled threads

        Args:
            result (Any): The result of the cancelled processing thread.
        """

    @abstractmethod
    def on_error(self, exception):
        """Callback method for exception raised in the process() call."""

    async def on_message(self, message: str):
        """Submit a task with the given message as a parameter and set the callback functions

        Args:
            message (str): Parameters for processing
        """
        task = self._pool.submit(self.process, message)
        task.add_done_callback(self._check_complete)

    @abstractmethod
    def process(self, message: str):
        """Task processing routine

        Receives the message and processes it. This is the main functionality of the class.
        Override it in derived classes based on your processing target.

        Args:
            message (str): The message to process.
        """

    def close(self, code: int = -1, reason: str = ""):
        """Close the thread-pool

        Args:
            code (int, optional): Exit status code. Defaults to -1.
            reason (str, optional): Reason of the shutdown. Defaults to "".

        Returns:
            nothing: by default. Could be overridden.
        """
        self._pool.shutdown(wait=True, cancel_futures=False)
        return super().close(code, reason)
