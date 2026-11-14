#!/usr/bin/env python3
"""Refresh the vendored data.

  data/tasks.json            trimmed `tasks` array from HF-URLs data/hf-urls.json (URLs + counts)
  data/hf-tasks-order.json   category + task order as shown on https://huggingface.co/tasks

Usage: uv run scripts/refresh-data.py   (then `pnpm build`)
Stdlib only.
"""
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = "https://raw.githubusercontent.com/danielrosehill/HF-URLs/main/data/hf-urls.json"
TASKS_PAGE = "https://huggingface.co/tasks"
FIELDS = ("id", "label", "category", "summary", "page", "models_url",
          "datasets_url", "models_count", "datasets_count")


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "hf-tasks-navigator-refresh"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def main() -> None:
    d = json.loads(get(UPSTREAM))
    tasks = {
        "source": "https://github.com/danielrosehill/HF-URLs (data/hf-urls.json)",
        "source_generated": d["generated"],
        "tasks": [{k: t.get(k) for k in FIELDS} for t in d["tasks"]],
    }
    (ROOT / "data/tasks.json").write_text(json.dumps(tasks, indent=1) + "\n")

    # The /tasks page is server-rendered: <h2>Category</h2> followed by href="/tasks/<id>" links.
    page = get(TASKS_PAGE)
    groups: list[dict] = []
    for m in re.finditer(r'<h2[^>]*>([^<]+)</h2>|href="/tasks/([a-z0-9-]+)"', page):
        if m.group(1):
            groups.append({"title": m.group(1).strip(), "tasks": []})
        elif groups and m.group(2) not in groups[-1]["tasks"]:
            groups[-1]["tasks"].append(m.group(2))
    groups = [g for g in groups if g["tasks"]]
    if len(groups) < 5:
        raise SystemExit(f"/tasks parse found only {len(groups)} groups; page layout changed?")
    order = {
        "source": TASKS_PAGE,
        "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "groups": groups,
    }
    (ROOT / "data/hf-tasks-order.json").write_text(json.dumps(order, indent=1) + "\n")
    print(f"{len(tasks['tasks'])} tasks; /tasks page: {len(groups)} groups, "
          f"{sum(len(g['tasks']) for g in groups)} tasks")


if __name__ == "__main__":
    main()
