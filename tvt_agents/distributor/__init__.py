# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Alert distributor with multiple sources and targets

"""

import queue
from queue import Queue
from time import sleep
from threading import Thread
from typing import List, TypeVar
from attrs import define, field, validators

from .source import AbstractDistributionSource
from .target import AbstractDistributionTarget
from .logutil import LoggingMixin


CDistributor = TypeVar("CDistributor", bound="Distributor")


@define
class Distributor(LoggingMixin):
    """
    A message distributor.

    Targets must implement AbstractDistributionTarget and
    sources must implement AbstractDistributionSource.
    """

    _shutdown_progress: bool = field(default=False)
    _queue: Queue = field(factory=Queue)
    _src_threadlist: list[Thread] = field(factory=list)
    _sources: List[AbstractDistributionSource] = field(factory=list)
    _targets: List[AbstractDistributionTarget] = field(factory=list)
    _send_delay: float = field(default=0.0, validator=validators.ge(0.0))

    @property
    def delay(self):
        return self._send_delay

    @delay.setter
    def delay(self, new_delay: float):
        self._send_delay = new_delay

    def add_source(self, src: AbstractDistributionSource):
        self._sources.append(src)
        self._sources[-1].set_on_message(self._thread_enqueue)
        self.logger.info("source added")

    def connect_sources(self):
        self.logger.debug("connecting sources...")
        for src in self._sources:
            src.open()

    def add_target(self, tgt: AbstractDistributionTarget):
        self._targets.append(tgt)
        self.logger.info("target added")

    def connect_targets(self):
        self.logger.debug("connecting targets...")
        for tgt in self._targets:
            tgt.open()

    def connect(self):
        self.connect_targets()
        self.connect_sources()

    def _enqueue_possible(self, message):
        """
        Checks if a message can be enqueued based on the shutdown status.

        Args:
            message (Any): The message to be checked.

        Returns:
            bool: True if the message can be enqueued, False if shutdown is in progress.
        """
        if self._shutdown_progress:
            self.logger.warning("No new messages accepted, shutdown in progress.")
            return False
        return True

    def _enqueue(self, message):
        """
        Enqueues a message into the internal queue if shutdown is not in progress.

        Args:
            message (Any): The message to be enqueued. It will be converted to a string before enqueuing.

        Returns:
            None

        Logs:
            - Warns if shutdown is in progress and the message is not accepted.
            - Errors if the queue is full and the message cannot be enqueued.
            - Info when the message is successfully enqueued.
        """
        if not self._enqueue_possible(message):
            return

        try:
            self._queue.put_nowait(str(message))
        except queue.Full:
            self.logger.error("failed to enqueue the message! Queue is full.")
            return
        self.logger.info("message enqueued...")

    def _thread_enqueue(self, message):
        """
        Starts a new thread to enqueue a message unless a shutdown is in progress.

        Args:
            message: The message object to be enqueued.

        Behavior:
            - If a shutdown is in progress (`self._shutdown_progress` is True), logs a warning and does not enqueue the message.
            - Otherwise, creates and starts a new thread that calls the `_enqueue` method with the given message.
            - Appends the new thread to `self._src_threadlist` and logs the thread start.
        """

        if not self._enqueue_possible(message):
            return

        self._src_threadlist.append(
            Thread(target=self._enqueue, kwargs={"message": message})
        )
        self.logger.debug("Starting enqueue thread...")
        self._src_threadlist[-1].start()

    async def run(self):
        while True:
            try:
                last_msg = self._queue.get(block=False)
            except queue.Empty:
                sleep(self._send_delay)
                continue
            await self._distribute_to_all(last_msg)
            self._queue.task_done()
            sleep(self._send_delay)

    async def _distribute_to_all(self, message):
        self.logger.debug(f"sending message '{message}' to all targets...")
        for tgt in self._targets:
            await tgt.on_message(message)
            self.logger.info("message distributed")

    async def flush(self):
        self.logger.info("Flushing the queue...")
        while not self._queue.empty():
            last_msg = self._queue.get(block=False)
            await self._distribute_to_all(last_msg)
            self._queue.task_done()
            sleep(self._send_delay)

    async def shutdown(self):
        self._shutdown_progress = True
        self.logger.info("closing sources...")
        for src in self._sources.copy():
            src.close(
                code=AbstractDistributionSource.DISCONNECT_SHUTDOWN,
                reason="shutdown by distributor",
            )

        await self.flush()

        self.logger.info("closing targets...")
        for tgt in self._targets.copy():
            tgt.close()

        self.logger.info("Waiting for queue threads to finish...")
        # shutting down the source queue threads
        for c_thread in self._src_threadlist:
            c_thread.join()
        self._shutdown_progress = False
