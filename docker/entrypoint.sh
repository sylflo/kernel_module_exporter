#!/bin/sh

if [ -z "$EXPORTER_PORT" ]; then
  EXPORTER_PORT=8000
fi

if [ -z "$CONFIG_PATH" ]; then
  CONFIG_PATH=/app/config.yml
fi

export EXPORTER_PORT
export CONFIG_PATH

python kernel_module_exporter.py