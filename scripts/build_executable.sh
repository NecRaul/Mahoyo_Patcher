#!/usr/bin/env bash

set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

uv run pyinstaller --clean --noconfirm spec/Mahoyo_Patcher.spec
