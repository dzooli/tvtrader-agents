import pytest
from datetime import datetime, timezone
from typing import Union

import orjson

from tvt_agents.distributor.formatters.graphite_formatter import GraphiteFormatter


class TestGraphiteFormatter:
    @pytest.fixture
    def formatter(self):
        return GraphiteFormatter()

    @pytest.fixture
    def valid_alert_json(self):
        return '''
        {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "BINANCE:BTCUSD",
            "interval": 15,
            "direction": "BUY",
            "price": 60000.50,
            "timestamp": "2024-06-01T03:16:17Z"
        }
        '''

    @pytest.fixture
    def valid_alert_dict(self):
        return {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "BINANCE:BTCUSD",
            "interval": 15,
            "direction": "SELL",
            "price": 59000.25,
            "timestamp": "2024-06-01T03:16:17Z"
        }

    @pytest.fixture
    def valid_alert_object(self):
        class Alert:
            def __init__(self):
                self.id = 123
                self.name = "MyStrategy"
                self.symbol = "BINANCE:ETHUSD"
                self.interval = 15
                self.direction = "Close entry(s) order long"
                self.price = 3000.75
                self.timestamp = "2024-06-01T03:16:17Z"
        return Alert()

    def test_format_valid_json_buy(self, formatter, valid_alert_json):
        expected_timestamp = int(datetime(2024, 6, 1, 3, 16, 17, tzinfo=timezone.utc).timestamp())
        expected_output = (
            f"tvt_agents.MyStrategy.BINANCE.BTCUSD.15.direction 1 {expected_timestamp}\n"
            f"tvt_agents.MyStrategy.BINANCE.BTCUSD.15.price 60000.5 {expected_timestamp}"
        )
        assert formatter.format(valid_alert_json) == expected_output

    def test_format_valid_dict_sell(self, formatter, valid_alert_dict):
        expected_timestamp = int(datetime(2024, 6, 1, 3, 16, 17, tzinfo=timezone.utc).timestamp())
        expected_output = (
            f"tvt_agents.MyStrategy.BINANCE.BTCUSD.15.direction -1 {expected_timestamp}\n"
            f"tvt_agents.MyStrategy.BINANCE.BTCUSD.15.price 59000.25 {expected_timestamp}"
        )
        assert formatter.format(valid_alert_dict) == expected_output

    def test_format_valid_object_close(self, formatter, valid_alert_object):
        expected_timestamp = int(datetime(2024, 6, 1, 3, 16, 17, tzinfo=timezone.utc).timestamp())
        expected_output = (
            f"tvt_agents.MyStrategy.BINANCE.ETHUSD.15.direction 0 {expected_timestamp}\n"
            f"tvt_agents.MyStrategy.BINANCE.ETHUSD.15.price 3000.75 {expected_timestamp}"
        )
        assert formatter.format(valid_alert_object) == expected_output

    def test_format_malformed_json(self, formatter):
        malformed_json = '''{"id": 123, "name": "MyStrategy", "symbol": "BTCUSD",'''
        with pytest.raises(orjson.JSONDecodeError):
            formatter.format(malformed_json)

    def test_format_invalid_input_type(self, formatter):
        with pytest.raises(TypeError, match="Unsupported message type"):
            formatter.format(123)  # Invalid type (int)

    def test_format_missing_key(self, formatter):
        invalid_dict = {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "BTCUSD",
            "interval": 15,
            "direction": "BUY",
            "price": 60000.50,
            # "timestamp": "2024-06-01T03:16:17Z"  # Missing timestamp
        }
        with pytest.raises(KeyError):
            formatter.format(invalid_dict)

    def test_format_missing_interval(self, formatter):
        invalid_dict = {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "BTCUSD",
            "direction": "BUY",
            "price": 60000.50,
            "timestamp": "2024-06-01T03:16:17Z"
        }
        with pytest.raises(KeyError):
            formatter.format(invalid_dict)

    def test_format_missing_interval(self, formatter):
        invalid_dict = {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "BTCUSD",
            # "interval": 15,  # Missing interval
            "direction": "BUY",
            "price": 60000.50,
            "timestamp": "2024-06-01T03:16:17Z"
        }
        with pytest.raises(KeyError):
            formatter.format(invalid_dict)

    def test_format_symbol_with_colon(self, formatter):
        alert_data = {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "NASDAQ:GOOG",
            "interval": 15,
            "direction": "BUY",
            "price": 100.0,
            "timestamp": "2024-06-01T03:16:17Z"
        }
        expected_timestamp = int(datetime(2024, 6, 1, 3, 16, 17, tzinfo=timezone.utc).timestamp())
        expected_output = (
            f"tvt_agents.MyStrategy.NASDAQ.GOOG.15.direction 1 {expected_timestamp}\n"
            f"tvt_agents.MyStrategy.NASDAQ.GOOG.15.price 100.0 {expected_timestamp}"
        )
        assert formatter.format(alert_data) == expected_output

    @pytest.mark.parametrize(
        "direction_input, expected_value",
        [
            ("BUY", 1),
            ("buy", 1),
            ("SELL", -1),
            ("sell", -1),
            ("Close entry(s) order long", 0),
            ("Close entry(s) order short", 0),
            ("UNKNOWN", 0),  # Edge case for unknown direction
        ],
    )
    def test_format_different_direction_cases(self, formatter, valid_alert_dict, direction_input, expected_value):
        alert_data = {**valid_alert_dict, "direction": direction_input}
        formatted_output = formatter.format(alert_data)
        assert f"direction {expected_value}" in formatted_output

    def test_format_timestamp_conversion(self, formatter):
        alert_data = {
            "id": 123,
            "name": "MyStrategy",
            "symbol": "TEST",
            "interval": 15,
            "direction": "BUY",
            "price": 1.0,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        expected_timestamp = int(datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp())
        assert f" {expected_timestamp}" in formatter.format(alert_data)
