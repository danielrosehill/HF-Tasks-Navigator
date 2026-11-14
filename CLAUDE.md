# HF-Model-Explorer-Launcher

Release tier: small (`v1.0`, `v1.1`, ...).

Static launcher page. Edit `scripts/build.py` (template + section order), never `hf-launch.html` by hand; rebuild and
commit both. Task data comes from the HF-URLs repo (`~/repos/github/data/HF-URLs`, `data/hf-urls.json`); fix URL or
count problems there, then `uv run scripts/build.py --refresh` here.
