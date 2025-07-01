import logging

from tvt_agents.distributor.logutil import LoggingMixin


def test_logutil_init():
    lmixin = LoggingMixin()
    logger = lmixin.logger
    assert isinstance(logger, logging.Logger)
