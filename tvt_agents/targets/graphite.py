"""
This module contains the Graphite target.
"""

from tvt_agents.targets.network import TcpTarget


class GraphiteTarget(TcpTarget):
    """
    A target for sending data to a Graphite server.
    """

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    def process(self, message: str):
        """Process the message."""
        # Graphite expects metrics in the format: <metric_path> <value> <timestamp>\n
        # For simplicity, we'll assume the result is a string in the correct format.
        # In a real-world scenario, you might want to add more robust parsing and error handling.
        self.send(f"{message}\n")

    def on_cancel(self, result):
        """Callback for when the future is cancelled."""
        pass

    def on_complete(self, result):
        """Callback for when the future is completed."""
        pass

    def on_error(self, exception):
        """Callback for when the future has an exception."""
        pass

    def on_timeout(self, result):
        """Callback for when the future is timed out."""
        pass
