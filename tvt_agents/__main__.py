# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import sys

from urllib3 import util as url_util
import asyncclick as click
import ws4py
import wsaccel

from tvt_agents.cli import DEFAULT_LOG_LEVEL
from tvt_agents.distributor.target.collector import collect_dist_targets
from tvt_agents.distributor import Distributor
from tvt_agents.distributor.source.websocket import WebSocketSource

from tvt_agents.cli.show import show as cli_show
from tvt_agents.cli.example import example as cli_example
from tvt_agents.cli.timing import timing as cli_timing


DEFAULT_LOG_INT = -1
try:
    DEFAULT_LOG_INT = logging.getLevelNamesMapping()[DEFAULT_LOG_LEVEL]
except KeyError:
    print(f"Invalid default log level! ({DEFAULT_LOG_LEVEL})")
    sys.exit(1)


def setup_logging(level: int = logging.DEBUG):
    res_logger = ws4py.configure_logger(level=level)
    fmt = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] REL:%(relativeCreated)d - PID:%(process)d - %(levelname)s - %(module)s:%(filename)s:%(lineno)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    for h in res_logger.handlers:
        h.setFormatter(fmt)
    return res_logger


logger = setup_logging(DEFAULT_LOG_INT)


@click.group
def cli():
    """CLI for distributed trading agents."""


async def run_websocket_source_loop(logger, websocket_url: str | None = None, targets=None):
    if not targets:
        logger.error("No distribution targets specified!")
        raise ValueError
    if not websocket_url:
        logger.error("WS source not specified!")
        raise ValueError
    wsaccel.patch_ws4py()
    dist = Distributor(logger)
    dist.logger = logger
    ws_source = WebSocketSource(
        websocket_url,
        protocols=["http-only", "chat"],
    )
    ws_source.logger = logger
    dist.add_source(ws_source)
    for target in targets:
        target.logger = logger
        dist.add_target(target)
    dist.connect()

    try:
        await dist.run()
    except KeyboardInterrupt:
        await dist.shutdown()


def validate_url_scheme(url: str, req_scheme: str = "ws") -> bool:
    logger.info("Validating URL scheme...")
    p_url = url_util.parse_url(url)
    return isinstance(p_url, url_util.Url) and isinstance(p_url.scheme, str) and p_url.scheme.startswith(req_scheme)


#
# The main CLI implementation
#
@cli.command
@click.option(
    "--log_level",
    type=click.Choice(["DEBUG", "ERROR", "WARNING", "INFO", "CRITICAL"], case_sensitive=False),
    default=DEFAULT_LOG_LEVEL,
    help="Set logging level.",
)
@click.option("--src", default="targets", help="Directory for dynamic target modules.")
@click.option("--ws_url", default="wss://socketsbay.com/wss/v2/1/demo/", help="Websocket distribution source URL.")
async def start(src: str, log_level: str, ws_url: str):
    """Start the distributor with WS source and targets from [src] directory.

    src: is './targets' by default.

    Each dynamic target module must define a create_<targetname>_target() function to be detectable as a target module.
    """
    logger.setLevel(log_level)
    dist_targets = collect_dist_targets(src, logger)
    if not validate_url_scheme(ws_url):
        click.secho("Invalid ws_url!", fg="red")
        return
    logger.info("Starting the distributor...")
    await run_websocket_source_loop(logger, ws_url, dist_targets)


def main():
    cli.add_command(cli_show)
    cli.add_command(cli_example)
    cli.add_command(cli_timing)
    cli()


if __name__ == "__main__":
    main()
    sys.exit()
