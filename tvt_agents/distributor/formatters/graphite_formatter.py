"""
This module contains the Graphite formatter.
"""

from typing import Union

import orjson
from datetime import datetime

from tvt_agents.distributor.formatter import IFormatter


class GraphiteFormatter(IFormatter):
    """
    Formatter for Graphite metrics from TradingView alerts.
    """

    def format(self, message: Union[str, dict, object]) -> str:
        """
        Formats the given message into Graphite-compatible metrics.

        Args:
            message (Union[str, dict, object]): The message representing a TradingView alert.

        Returns:
            str: A string containing two Graphite metrics, separated by a newline.
        """
        alert_data: dict
        if isinstance(message, str):
            alert_data = orjson.loads(message)
        elif isinstance(message, dict):
            alert_data = message
        else:
            # Attempt to convert object to dictionary, assuming it has accessible attributes
            try:
                alert_data = message.__dict__
            except AttributeError:
                raise TypeError("Unsupported message type. Expected str, dict, or object with __dict__.")

        strategy_name = alert_data["name"]
        symbol = alert_data["symbol"].replace(":", ".")
        direction = alert_data["direction"]
        price = alert_data["price"]
        timestamp_str = alert_data["timestamp"]

        # Convert ISO 8601 timestamp to Unix timestamp
        # Remove 'Z' and parse, then get timestamp
        timestamp_dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        timestamp_unix = int(timestamp_dt.timestamp())

        # Determine directional value
        direction_value = 0
        if direction.lower() == "buy":
            direction_value = 1
        elif direction.lower() == "sell":
            direction_value = -1

        # Construct metric paths
        direction_metric_path = f"tvt_agents.{strategy_name}.{symbol}.direction"
        price_metric_path = f"tvt_agents.{strategy_name}.{symbol}.price"

        # Format metrics
        direction_metric = f"{direction_metric_path} {direction_value} {timestamp_unix}"
        price_metric = f"{price_metric_path} {price} {timestamp_unix}"

        return f"{direction_metric}\n{price_metric}"