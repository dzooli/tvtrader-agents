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

2.  **Install dependencies using Poetry:**
    If you don't have Poetry installed, you can install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).
    ```bash
    poetry install
    ```

3.  **Activate the virtual environment:**
    ```bash
    poetry shell
    ```

## Usage

The primary entry point for the distributor is the `tvtrader_distributor` command-line interface.

### Starting the Distributor

To start the distributor with a WebSocket source and dynamically loaded targets, use the `start` command:

```bash
tvtrader_distributor start --ws_url "wss://socketsbay.com/wss/v2/1/demo/" --src "targets" --log_level INFO
```

*   `--ws_url`: Specifies the WebSocket URL to connect to as a message source. (Default: `wss://socketsbay.com/wss/v2/1/demo/`)
*   `--src`: Specifies the directory from which to load dynamic target modules. (Default: `targets`)
*   `--log_level`: Sets the logging level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). (Default: `INFO`)

### Other Commands

*   `tvtrader_distributor show`: Displays information about the system.
*   `tvtrader_distributor example`: Runs an example scenario.
*   `tvtrader_distributor timing`: Performs timing benchmarks.

For more details on each command, use the `--help` option:

```bash
tvtrader_distributor start --help
```

## Plugin Architecture

The TVTrader Agents system is designed with a plugin-based architecture for its distribution sources and targets, promoting extensibility and modularity.

### Targets

Distribution targets are dynamically loaded from a specified directory (defaulting to `targets/`). A Python module is identified as a target plugin if it defines a function following the naming convention `create_<targetname>_target()`. This function is responsible for instantiating and returning an object that implements the `AbstractDistributionTarget` interface.

**Example Target Module (`targets/my_custom_target.py`):**

```python
# targets/my_custom_target.py
from tvt_agents.distributor.target import AbstractDistributionTarget
from attrs import define

@define
class MyCustomTarget(AbstractDistributionTarget):
    async def on_message(self, message: str):
        print(f"MyCustomTarget received: {message}")

    def open(self):
        print("MyCustomTarget opened.")

    def close(self, code: int = -1, reason: str = ""):
        print(f"MyCustomTarget closed with code {code}: {reason}")

def create_my_custom_target():
    return MyCustomTarget()
```

When the distributor starts, it scans the `--src` directory for such functions, imports them, and uses them to register new distribution targets. This allows users to easily add custom message handling logic without modifying the core distributor code.

### Sources

Similarly, distribution sources (like the `WebSocketSource`) are responsible for providing messages to the distributor. New sources can be integrated by implementing the `AbstractDistributionSource` interface and configuring the distributor to use them.****
