#!/usr/bin/env bash

set -euo pipefail

find . \
    \( \
    -name ".pytest_cache" -o \
    -name ".ruff_cache" -o \
    -name ".mypy_cache" -o \
    -name "__pycache__" -o \
    -name "build" -o \
    -name "dist" \
    \) \
    -type d \
    -exec rm -rf {} +

find . \
    \( \
    -name "*.pyc" -o \
    -name "*.pyo" \
    \) \
    -type f \
    -delete
