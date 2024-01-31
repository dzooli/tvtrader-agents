# Copyright (c) 2024 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import logging
import asyncclick as click
from . import DEFAULT_LOG_LEVEL
from ..distributor.target.collector import collect_dist_targets


@click.group
def show():
    """Show various internal information."""


@show.command
@click.option(
    "--verbose",
    default=False,
    is_flag=True,
    help="Display target's documentation if exists.",
)
@click.option(
    "--log_level",
    type=click.Choice(["DEBUG", "ERROR", "WARNING", "INFO", "CRITICAL"], case_sensitive=False),
    default=DEFAULT_LOG_LEVEL,
    help="Set logging level.",
)
def targets(verbose, log_level):
    """Show loadable distribution targets"""
    dist_targets = []
    logging.basicConfig()
    logging.getLogger().setLevel(log_level)
    dist_targets = collect_dist_targets()
    print("\nInitialized targets: ")
    for obj in dist_targets:
        print("-", type(obj), "from module:", obj.__module__)
        if verbose:
            print("  Documentation:")
            print("   ", obj.__doc__)
