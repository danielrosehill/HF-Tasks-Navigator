# HF Tasks Navigator

Release tier: small (`v1.0`, `v1.1`, ...). Repo renamed from HF-Model-Explorer-Launcher on 2026-11-14.

Astro single page → `hf-launch.html` (committed; never hand-edit, run `pnpm build`). Output must stay self-contained
(inline CSS, `is:inline` scripts, no external assets) because it is opened from `file://`. Task URLs/counts come from
HF-URLs (`~/repos/github/data/HF-URLs`); fix data problems there, then `uv run scripts/refresh-data.py` and rebuild.
Daniel's View lives in `views/daniels-view.json`. See README for layout.
