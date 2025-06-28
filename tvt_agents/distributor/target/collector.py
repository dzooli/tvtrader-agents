# Copyright (c) 2024 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
import importlib
import logging


def collect_dist_targets(
    src: str = "targets",
    logger: logging.Logger = logging.getLogger(),
):
    """Collecting the distribution target modules.

    A module is identified as a target module (plugin) when it has an exported function with ```create_XXX_target``` naming convention.
    This function should be imported and called to initialize the distributor target.

    Args:
        src (str, optional): Directory relative to the script from where target plugins should be loaded. Defaults to "targets".
    """
    dist_targets = []

    logger.info(f"Path: {os.getcwd()}")
    logger.debug("Appending $PWD to module search path...")

    sys.path.append(".")

    logger.info("Collecting custom targets...")
    targets_module = importlib.import_module(src, src)
    for name in targets_module.__all__:
        if not (
            callable(eval(f"targets_module.{name}"))
            and name.startswith("create_")
            and name.endswith("_target")
        ):
            continue
        logger.info(f"Found target factory: {name}. Registration...")
        obj = None
        try:
            obj = eval(f"targets_module.{name}")()
            if not obj:
                raise ValueError("Invalid target module! Registration falied!")
        except Exception as exc:
            logger.critical(
                f"Cannot instantiate the distributor target with: {name}. {str(exc)}"
            )
        logger.info(f"{obj} has been registered by {name}")
        logger.debug(type(obj))
        if obj not in dist_targets:
            dist_targets.append(obj)
        logger.debug(f"target count: {len(dist_targets)}")
    return dist_targets
