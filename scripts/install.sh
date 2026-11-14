#!/usr/bin/env bash
# Copy the launcher to ~/launchers/hf-launch.html (override with HF_LAUNCH_DIR).
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
dest_dir="${HF_LAUNCH_DIR:-$HOME/launchers}"
mkdir -p "$dest_dir"
cp "$here/hf-launch.html" "$dest_dir/hf-launch.html"
echo "$dest_dir/hf-launch.html"
