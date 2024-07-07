# kernel_module_exporter

kernel_module_exporter is a custom Prometheus exporter that checks the status of specified kernel modules on a Linux system and exposes this information as Prometheus metrics. This allows you to monitor the presence and status of kernel modules using Prometheus.

## Table of Contents

- [kernel_module_exporter](#kernel_module_exporter)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Running with Docker](#running-with-docker)
  - [Prometheus Integration](#prometheus-integration)

## Features

- Checks the status of specified kernel modules.
- Exposes the status of kernel modules as Prometheus metrics.
- Configurable via a YAML configuration file.
- Easy deployment with Docker.

## Prerequisites

- Python 3.9+
- Prometheus
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/kernel_module_exporter.git
    cd kernel_module_exporter
    ```

2. Install dependencies using Poetry:

    ```sh
    pip install --no-cache-dir poetry
    poetry install --no-root
    ```

## Configuration

Create a configuration file config.yml to specify the kernel modules you want to monitor:

  ```sh
  modules:
    - name: ip_tables
    - name: nf_conntrack
    # Add more modules as needed
  ```

You can also specify the path to the configuration file using the CONFIG_PATH environment variable.


## Usage

Run the exporter:

  ```sh
  CONFIG_PATH=/path/to/config.yml EXPORTER_PORT=8000 python kernel_module_exporter.py
  ```

The metrics will be exposed at http://localhost:8000/metrics.

## Running with Docker

1. Build the Docker image:

    ```sh
    docker build -t kernel_module_exporter .
    ```

2. Run the Docker container:

    ```sh
    docker run -d -p 8000:8000 -e EXPORTER_PORT=8000 -e CONFIG_PATH=/path/to/config.yml kernel_module_exporter
    ```

## Prometheus Integration

Add the following scrape configuration to your Prometheus configuration file (`prometheus.yml`):

  ```sh
  scrape_configs:
    - job_name: 'kernel_module_exporter'
      static_configs:
        - targets: ['localhost:8000']
  ```

This configuration tells Prometheus to scrape the metrics exposed by the kernel_module_exporter.
