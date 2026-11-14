# HF-Model-Explorer-Launcher

A single static HTML page, bookmarkable, that lists every Hugging Face Hub task grouped the way the
[huggingface.co/models](https://huggingface.co/models) sidebar groups them. Each task has two buttons:

- **Models** → the filtered model list, `https://huggingface.co/models?pipeline_tag=<task>`
- **Datasets** → the filtered dataset list, `https://huggingface.co/datasets?task_categories=task_categories:<task>`

The point is to skip the [huggingface.co/tasks](https://huggingface.co/tasks) explainer pages and land straight on
the lists. The small `?` on each card still links the explainer. Counts are the Hub's result counts at build time.
A greyed `—` button means the Hub has no matching tag on that side (e.g. no `task_categories:keypoint-detection`
for datasets). Type to filter tasks; `/` focuses the filter, `Esc` clears it. Light and dark mode follow the system.

Unofficial; not affiliated with Hugging Face.

## Use

```bash
scripts/install.sh   # copies hf-launch.html to ~/launchers/hf-launch.html (override dir: HF_LAUNCH_DIR=...)
scripts/open.sh      # opens ~/launchers/hf-launch.html in the default browser (installs first if missing)
```

Then bookmark the page in the browser.

## Data and rebuilding

`data/tasks.json` is a trimmed copy of the `tasks` array in
[HF-URLs](https://github.com/danielrosehill/HF-URLs) `data/hf-urls.json`, which holds the checked
task → URL mapping and counts (built from `https://huggingface.co/api/tasks` plus the Hub tag APIs).

```bash
uv run scripts/build.py            # regenerate hf-launch.html from data/tasks.json
uv run scripts/build.py --refresh  # pull the latest tasks from HF-URLs on GitHub first, then regenerate
scripts/install.sh                 # re-copy to ~/launchers
```

Section order and names (Multimodal, Computer Vision, Natural Language Processing, Audio, Tabular,
Reinforcement Learning, Other) are set in `SECTIONS` in `scripts/build.py`; any new category from upstream is
appended at the end. Some counts are blank where the HF-URLs build hit rate limits (429) — the link still works.
Stdlib Python only; `hf-launch.html` is self-contained (no external assets) and committed.
