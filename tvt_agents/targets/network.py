"""
This module contains the network target base classes.
"""

import socket
from abc import ABC, abstractmethod

from tvt_agents.distributor.target import ThreadedDistributionTarget


class INetworkTarget(ABC):
    """
    Interface for network targets.
    """

    @abstractmethod
    def connect(self):
        """
        Connect to the target.
        """

    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the target.
        """

    @abstractmethod
    def send(self, data: str):
        """
        Send data to the target.
        """


class SocketTarget(ThreadedDistributionTarget, INetworkTarget):
    """
    Base class for socket-based targets.
    """

    def __init__(self, host: str, port: int):
        super().__init__()
        self._host = host
        self._port = port
        self._socket = None

    def connect(self):
        """
        Connect to the target.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def disconnect(self):
        """
        Disconnect from the target.
        """
        if self._socket:
            self._socket.close()
            self._socket = None

    def send(self, data: str):
        """
        Send data to the target.
        """
        if self._socket:
            self._socket.sendall(data.encode())

    def process(self, message: str):
        """
        Process the the message sending.
        """
        self.send(message)


class TcpTarget(SocketTarget):
    """
    Base class for TCP-based targets.
    """


class UdpTarget(SocketTarget):
    """
    Base class for UDP-based targets.
    """

    def connect(self):
        """
        Connect to the target.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data: str):
        """
        Send data to the target.
        """
        if self._socket:
            self._socket.sendto(data.encode(), (self._host, self._port))
