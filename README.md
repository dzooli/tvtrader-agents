# TVTrader Agents

## Overview

This project provides a lightweight, modular, and multi-threaded message distribution system designed for high-performance network applications. It acts as a flexible message broker, enabling the distribution of alerts and messages from various sources to multiple targets with minimal overhead. The architecture emphasizes modularity, allowing for runtime-loadable sources and targets.

## Installation

To install the TVTrader Agents, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dzooli/tvtrader-agents.git
    cd tvtrader-agents/agents
    ```

1.  **Install dependencies using uv:**
    If you don't have uv installed, you can install it by following the instructions on the [uv website](https://docs.astral.sh/uv/getting-started/installation/).
    ```bash
    uv sync --extra dev
    ```

1.  **Run commands with uv:**
    You can run commands directly with uv without needing to activate a virtual environment:
    ```bash
    uv run tvtrader_distributor --help
    ```

## Usage

The primary entry point for the distributor is the `tvtrader_distributor` command-line interface.

### Starting the Distributor

To start the distributor with a WebSocket source and dynamically loaded targets, use the `start` command:

```bash
uv run tvtrader_distributor start --ws_url "wss://socketsbay.com/wss/v2/1/demo/" \
                                  --src "targets" --log_level INFO

#   `--ws_url`:    Specifies the WebSocket URL to connect to as a message source.
#                   (Default: `wss://socketsbay.com/wss/v2/1/demo/`)
#   `--src`:       Specifies the directory from which to load dynamic target modules.
#                   (Default: `targets`)
#   `--log_level`: Sets the logging level 
#                   (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). 
#                   (Default: `INFO`)
```

### Other Commands

*   `uv run tvtrader_distributor show`: Displays information about the system.
*   `uv run tvtrader_distributor example`: Runs an example scenario.
*   `uv run tvtrader_distributor timing`: Performs timing benchmarks.

For more details on each command, use the `--help` option:

```bash
uv run tvtrader_distributor start --help
```

## Plugin Architecture

The TVTrader Agents system is designed with a plugin-based architecture for its distribution sources and targets, promoting extensibility and modularity.

### Message Distribution Flow

Messages received by a source are distributed to registered targets through a defined flow:

1.  **`on_message(message: str)`**: This asynchronous method is the entry point for a new message in a `ThreadedDistributionTarget`. It's responsible for preparing the message for processing.
    -   **Formatter Application**: If a `formatter` is set on the target instance (e.g., `target_instance.formatter = MyFormatter()`), the `on_message` method will automatically apply this formatter to the incoming message before further processing. This allows for flexible message transformation without modifying the core target logic.
2.  **`process(message: str)`**: This abstract method is where the core logic for handling the message resides. It receives the message (which might have been formatted by `on_message`) and performs the target-specific action (e.g., sending it over a network, writing to a console).
3.  **`send(data: str)` (for network targets)**: For network-based targets (like `TcpTarget` or `UdpTarget`), the `process` method typically calls a `send` method to transmit the data.

### Targets

Distribution targets are dynamically loaded from a specified directory (defaulting to `targets/` ). A Python module is identified as a target plugin if it defines a function following the naming convention `create_<targetname>_target()` . This function is responsible for instantiating and returning an object that implements the `AbstractDistributionTarget` interface.

**Implementing a Custom Distribution Target Plugin:**

To create your own target, you need to:

1.  **Implement `AbstractDistributionTarget`**: Your target class must inherit from `AbstractDistributionTarget` and implement its abstract methods (`on_message`,        `process`,        `on_complete`,        `on_timeout`,        `on_cancel`,        `on_error`).
2.  **Define a `create_` function**: Create a function named `create_<your_target_name>_target()` in your module. This function will be called by the distributor to instantiate your target.
3.  **Optional: Use a Formatter**: If your target requires specific message formatting, you can set a formatter instance on your target after its creation.
  
For example, if you have a `GraphiteFormatter` :

    

```python
# targets/my_graphite_target.py
from tvt_agents.targets.network import TcpTarget
from tvt_agents.distributor.formatters.graphite_formatter import GraphiteFormatter

class MyGraphiteTarget(TcpTarget):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.formatter = GraphiteFormatter() # Set the formatter here

    def process(self, message: str):
        # The message is already formatted by self.formatter in on_message
        self.send(f"{message}\n")

def create_my_graphite_target():
    return MyGraphiteTarget("localhost", 2003) # Example host and port
```

**Example Target Module (inheriting from `ThreadedDistributionTarget` - `targets/my_custom_target.py` ):**

```python
# targets/my_custom_target.py
from tvt_agents.distributor.target import ThreadedDistributionTarget
from attrs import define

@define
class MyCustomTarget(ThreadedDistributionTarget):
    async def on_message(self, message: str):
        # If a formatter is set, it will be applied here before process()
        super().on_message(message)

    def process(self, message: str):
        print(f"MyCustomTarget received and processed: {message}")

    def on_complete(self, result):
        print(f"MyCustomTarget completed: {result}")

    def on_timeout(self, result):
        print(f"MyCustomTarget timed out: {result}")

    def on_cancel(self, result):
        print(f"MyCustomTarget cancelled: {result}")

    def on_error(self, exception):
        print(f"MyCustomTarget error: {exception}")

    def open(self):
        print("MyCustomTarget opened.")

    def close(self, code: int = -1, reason: str = ""):
        print(f"MyCustomTarget closed with code {code}: {reason}")

def create_my_custom_target():
    return MyCustomTarget()
```

When the distributor starts, it scans the `--src` directory for such functions, imports them, and uses them to register new distribution targets. This allows users to easily add custom message handling logic without modifying the core distributor code.

### Sources

Similarly, distribution sources (like the `WebSocketSource` ) are responsible for providing messages to the distributor. New sources can be integrated by implementing the `AbstractDistributionSource` interface and configuring the distributor to use them.****
