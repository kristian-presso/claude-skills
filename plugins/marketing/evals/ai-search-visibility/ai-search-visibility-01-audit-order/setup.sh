#!/usr/bin/env bash
# Stage this case's fixtures into the run's working directory.
set -euo pipefail
cp -R "$(cd "$(dirname "$0")" && pwd)/fixtures/." .
