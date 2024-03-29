# Copyright (c) 2024 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from time import perf_counter
import asyncclick as click
from tvt_agents.example.threaded_target import run_example as threaded_example


@click.group
def timing():
    """Get timing information of the selected example."""


@timing.command
@click.option("--count", default=1000, help="Number of messages to process.")
async def threadedtarget(count: int):
    """Measure execution time of ThreadedDistributionTarget."""
    start_time = perf_counter()
    await threaded_example(count)
    print(f"Elapsed time: {(perf_counter() - start_time):0.6f}")
