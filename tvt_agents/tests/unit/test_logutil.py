import pytest

from tvt_agents.distributor.logutil import LoggingMixin


def test_logutil_init():
    lmixin = LoggingMixin()
    logger = lmixin.logger
    assert logger is None
