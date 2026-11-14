#!/usr/bin/env python3
"""Build hf-launch.html from data/tasks.json.

Usage:
    uv run scripts/build.py            # build from the vendored data/tasks.json
    uv run scripts/build.py --refresh  # re-pull tasks from HF-URLs on GitHub first

Stdlib only. Output: hf-launch.html at the repo root (committed).
"""
from __future__ import annotations

import html
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "tasks.json"
OUT = ROOT / "hf-launch.html"
UPSTREAM = "https://raw.githubusercontent.com/danielrosehill/HF-URLs/main/data/hf-urls.json"

# Section order and names as in the huggingface.co/models sidebar.
SECTIONS = [
    ("Multimodal", "Multimodal"),
    ("Vision", "Computer Vision"),
    ("Text", "Natural Language Processing"),
    ("Audio", "Audio"),
    ("Tabular", "Tabular"),
    ("Reinforcement learning", "Reinforcement Learning"),
    ("Other", "Other"),
]
FIELDS = ("id", "label", "category", "summary", "page", "models_url",
          "datasets_url", "models_count", "datasets_count")


def refresh() -> None:
    with urllib.request.urlopen(UPSTREAM, timeout=30) as r:
        d = json.load(r)
    out = {
        "source": "https://github.com/danielrosehill/HF-URLs (data/hf-urls.json)",
        "source_generated": d["generated"],
        "tasks": [{k: t.get(k) for k in FIELDS} for t in d["tasks"]],
    }
    DATA.write_text(json.dumps(out, indent=1) + "\n")
    print(f"refreshed {len(out['tasks'])} tasks from {UPSTREAM}")


def fmt(n: int | None) -> str:
    if n is None:
        return ""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k".replace(".0k", "k")
    return str(n)


def link(url: str | None, label: str, count: int | None, cls: str) -> str:
    if not url:
        return f'<span class="btn {cls} off" title="No {label.lower()} tag for this task on the Hub">{label} —</span>'
    c = f' <span class="n">{fmt(count)}</span>' if count else ""
    return f'<a class="btn {cls}" href="{html.escape(url)}">{label}{c}</a>'


def build() -> None:
    d = json.loads(DATA.read_text())
    by_cat: dict[str, list[dict]] = {}
    for t in d["tasks"]:
        by_cat.setdefault(t["category"], []).append(t)
    known = {k for k, _ in SECTIONS}
    sections = SECTIONS + [(c, c) for c in by_cat if c not in known]

    parts = []
    for key, title in sections:
        tasks = sorted(by_cat.get(key, []), key=lambda t: t["label"])
        if not tasks:
            continue
        cards = []
        for t in tasks:
            if t["label"] == t["id"]:  # dataset-only tags come through unlabelled
                t["label"] = t["id"].replace("-", " ").title()
            summary = html.escape(t.get("summary") or "")
            cards.append(
                f'<div class="card" data-q="{html.escape((t["label"] + " " + t["id"]).lower())}">'
                f'<div class="t" title="{summary}">{html.escape(t["label"])}'
                + (f'<a class="about" href="{html.escape(t["page"])}" title="Task explainer page">?</a>' if t.get("page") else "")
                + '</div>'
                f'<div class="links">{link(t["models_url"], "Models", t["models_count"], "m")}'
                f'{link(t["datasets_url"], "Datasets", t["datasets_count"], "d")}</div></div>'
            )
        parts.append(f'<section><h2>{html.escape(title)}</h2><div class="grid">{"".join(cards)}</div></section>')

    page = TEMPLATE.replace("{{SECTIONS}}", "\n".join(parts)).replace(
        "{{GENERATED}}", html.escape(d.get("source_generated", "")[:10])
    ).replace("{{N}}", str(len(d["tasks"])))
    OUT.write_text(page)
    print(f"wrote {OUT} ({len(d['tasks'])} tasks)")


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HF Launcher</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤗</text></svg>">
<style>
:root{--bg:#f7f7f8;--fg:#1f2328;--mut:#6b7280;--card:#fff;--line:#e5e7eb;--m:#2563eb;--d:#dc2626}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#e6e6e6;--mut:#9aa0a6;--card:#171a21;--line:#2a2f3a;--m:#60a5fa;--d:#f87171}}
*{box-sizing:border-box}
body{margin:0;font:14px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
header{position:sticky;top:0;z-index:1;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 24px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
h1{font-size:18px;margin:0}
h1 a{color:inherit;text-decoration:none}
#q{flex:1;min-width:200px;max-width:360px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);font:inherit}
.top a{color:var(--mut);margin-right:12px;text-decoration:none}
.top a:hover{color:var(--fg)}
main{padding:8px 24px 40px;max-width:1400px;margin:0 auto}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:24px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.t{font-weight:600;margin-bottom:8px;display:flex;justify-content:space-between;gap:8px}
.about{color:var(--mut);text-decoration:none;font-weight:400;border:1px solid var(--line);border-radius:50%;width:18px;height:18px;font-size:11px;display:inline-flex;align-items:center;justify-content:center;flex:none}
.about:hover{color:var(--fg)}
.links{display:flex;gap:6px}
.btn{flex:1;text-align:center;padding:5px 6px;border-radius:6px;text-decoration:none;font-size:13px;border:1px solid}
.btn.m{color:var(--m);border-color:color-mix(in srgb,var(--m) 40%,transparent)}
.btn.d{color:var(--d);border-color:color-mix(in srgb,var(--d) 40%,transparent)}
.btn.m:hover{background:color-mix(in srgb,var(--m) 12%,transparent)}
.btn.d:hover{background:color-mix(in srgb,var(--d) 12%,transparent)}
.btn.off{color:var(--mut);border-color:var(--line);opacity:.6}
.n{opacity:.7;font-size:11px}
footer{color:var(--mut);font-size:12px;padding:0 24px 24px;text-align:center}
footer a{color:inherit}
.hide{display:none}
</style>
</head>
<body>
<header>
<h1><a href="https://huggingface.co">🤗 HF Launcher</a></h1>
<input id="q" type="search" placeholder="Filter tasks…  (press / )" autofocus>
<nav class="top"><a href="https://huggingface.co/models">All models</a><a href="https://huggingface.co/datasets">All datasets</a><a href="https://huggingface.co/spaces">Spaces</a><a href="https://huggingface.co/tasks">Tasks</a></nav>
</header>
<main>
{{SECTIONS}}
</main>
<footer>{{N}} tasks · counts as of {{GENERATED}} · data from <a href="https://github.com/danielrosehill/HF-URLs">HF-URLs</a> · <a href="https://github.com/danielrosehill/HF-Model-Explorer-Launcher">source</a> · unofficial, not affiliated with Hugging Face</footer>
<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();
document.querySelectorAll('section').forEach(s=>{let any=false;
s.querySelectorAll('.card').forEach(c=>{const hit=!v||c.dataset.q.includes(v);c.classList.toggle('hide',!hit);any||=hit});
s.classList.toggle('hide',!any)})});
document.addEventListener('keydown',e=>{if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus()}
if(e.key==='Escape'){q.value='';q.dispatchEvent(new Event('input'))}});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    if "--refresh" in sys.argv:
        refresh()
    build()
