// Builds the two presets from the vendored data. Any task a view doesn't place lands in "Not yet classified",
// so new upstream tasks never disappear silently.
import tasksData from "../../data/tasks.json";
import hfOrder from "../../data/hf-tasks-order.json";
import daniel from "../../views/daniels-view.json";

export type Task = (typeof tasksData.tasks)[number];
export interface Sub { title: string; tasks: string[] }
export interface Group { title: string; tasks: string[]; subgroups: Sub[] }
export interface View { id: string; name: string; description: string; groups: Group[] }

export const tasks: Record<string, Task> = Object.fromEntries(tasksData.tasks.map((t) => [t.id, t]));
export const generated = tasksData.source_generated.slice(0, 10);
export const hfOrderFetched = hfOrder.fetched.slice(0, 10);

// API category name -> /tasks page heading
const API_TO_PAGE: Record<string, string> = {
  Text: "Natural Language Processing", Vision: "Computer Vision", "Reinforcement learning": "Reinforcement Learning",
};

/** Global HF order: the /tasks page order, then tasks only on /models, alphabetically within category. */
export const hfRank: Record<string, number> = {};

function finish(v: { id: string; name: string; description: string; groups: any[] }): View {
  const groups: Group[] = v.groups.map((g) => ({
    title: g.title,
    tasks: (g.tasks ?? []).filter((id: string) => tasks[id]),
    subgroups: (g.subgroups ?? []).map((s: Sub) => ({ title: s.title, tasks: s.tasks.filter((id) => tasks[id]) })),
  }));
  const placed = new Set(groups.flatMap((g) => [...g.tasks, ...g.subgroups.flatMap((s) => s.tasks)]));
  const rest = Object.keys(tasks).filter((id) => !placed.has(id)).sort();
  if (rest.length) groups.push({ title: "Not yet classified", tasks: rest, subgroups: [] });
  return { ...v, groups };
}

function huggingFaceView(): View {
  const groups = hfOrder.groups.map((g) => ({ title: g.title, tasks: g.tasks.filter((id) => tasks[id]) }));
  const onPage = new Set(groups.flatMap((g) => g.tasks));
  const extra = Object.values(tasks).filter((t) => !onPage.has(t.id)).sort((a, b) => a.label.localeCompare(b.label));
  for (const t of extra) {
    const title = API_TO_PAGE[t.category] ?? t.category;
    let g = groups.find((x) => x.title === title);
    if (!g) groups.push((g = { title, tasks: [] }));
    g.tasks.push(t.id);
  }
  let i = 0;
  for (const g of groups) for (const id of g.tasks) hfRank[id] = i++;
  return finish({
    id: "hf",
    name: "Hugging Face",
    description: "Categories and order as on huggingface.co/tasks; tasks listed only on /models are appended to their category.",
    groups,
  });
}

// Daniel's View first: it is the default (DEFAULT_VIEW in index.astro). huggingFaceView() also fills hfRank.
const hf = huggingFaceView();
export const views: View[] = [finish(daniel), hf];
