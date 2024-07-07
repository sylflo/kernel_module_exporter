import logging
import os
import subprocess
import time
from typing import Dict, List

import yaml
from prometheus_client import Gauge, start_http_server

# Configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Load module configuration from YAML file
def load_config(config_file: str) -> List[Dict[str, str]]:
    logger.info(f"Loading configuration from {config_file}")
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config["modules"]


# Define gauges for kernel modules
def create_gauges(modules: List[Dict[str, str]]) -> Dict[str, Gauge]:
    logger.info("Creating gauges for kernel modules")
    gauges = {}
    for module in modules:
        module_name = module["name"]
        gauges[module_name] = Gauge(
            f"module_{module_name}_loaded",
            f"Indicates if the {module_name} module is loaded",
        )
    return gauges


def check_module(module_name: str) -> int:
    try:
        output = subprocess.check_output(["lsmod"], text=True)
        return 1 if module_name in output else 0
    except subprocess.CalledProcessError:
        logger.error(f"Failed to check module {module_name}")
        return 0


def update_metrics(gauges: Dict[str, Gauge]) -> None:
    logger.info("Updating metrics")
    for module in gauges:
        gauges[module].set(check_module(module))


if __name__ == "__main__":
    config_file = os.getenv("CONFIG_PATH", "config.yml")
    port = int(os.getenv("EXPORTER_PORT", "8000"))

    logger.info(
        f"Starting KernelModuleExporter with config: {config_file} on port: {port}"  # noqa: E501
    )

    modules = load_config(config_file)
    module_gauges = create_gauges(modules)

    # Start the HTTP server to expose metrics
    start_http_server(port)
    logger.info(f"HTTP server started on port {port}")

    # Continuously update metrics
    while True:
        update_metrics(module_gauges)
        time.sleep(60)
