# Copyright (c) 2024 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import asyncclick as click
from tvt_agents.examples.threaded_target import run_example as threaded_example


@click.group
def example():
    """Run selected example."""


@example.command
@click.option("--count", default=1000, help="Number of messages to process.")
async def threadedtarget(count: int):
    """Run the example for ThreadedDistributionTarget."""
    await threaded_example(count)
