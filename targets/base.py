# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from collections.abc import Callable

from tvt_agents.distributor.target import ThreadedDistributionTarget


class ThreadedBase(ThreadedDistributionTarget):
    def __init__(self, poolsize: int = 10, initializer: Callable | None = None):
        super().__init__(poolsize, initializer)

    def on_complete(self, result):
        return super().on_complete(result)

    def on_cancel(self, result):
        return super().on_cancel(result)

    def on_error(self, exception):
        return super().on_error(exception)

    def on_timeout(self, result):
        return super().on_timeout(result)
