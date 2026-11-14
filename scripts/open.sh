#!/usr/bin/env bash
# Open the installed launcher in the default browser (installs it first if missing).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
f="${HF_LAUNCH_DIR:-$HOME/launchers}/hf-launch.html"
[ -f "$f" ] || "$here/install.sh" >/dev/null
if command -v xdg-open >/dev/null; then xdg-open "$f" >/dev/null 2>&1 &
elif command -v open >/dev/null; then open "$f"
else echo "Open file://$f in your browser"; fi
echo "file://$f"
