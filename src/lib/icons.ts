// Task id -> lucide-static icon name (https://lucide.dev). Unknown tasks fall back to "shapes".
import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

export const TASK_ICONS: Record<string, string> = {
  "any-to-any": "shuffle", "audio-text-to-text": "audio-lines", "document-question-answering": "file-question-mark",
  "visual-document-retrieval": "file-search", "image-text-to-text": "scan-text", "image-text-to-image": "image-plus",
  "image-text-to-video": "clapperboard", "video-text-to-text": "square-play", "visual-question-answering": "message-circle-question-mark",
  "feature-extraction": "binary", "fill-mask": "text-cursor-input", "question-answering": "circle-help",
  "sentence-similarity": "equal-approximately", "summarization": "align-left", "table-question-answering": "sheet",
  "text-classification": "tags", "text-generation": "pen-line", "text-ranking": "arrow-down-wide-narrow",
  "token-classification": "highlighter", "translation": "languages", "zero-shot-classification": "sparkles",
  "multiple-choice": "list-checks", "table-to-text": "table", "text-retrieval": "text-search",
  "depth-estimation": "layers", "image-classification": "image", "image-feature-extraction": "scan",
  "image-segmentation": "shapes", "image-to-image": "images", "image-to-text": "captions", "image-to-video": "film",
  "keypoint-detection": "person-standing", "mask-generation": "square-dashed", "object-detection": "scan-search",
  "video-classification": "video", "text-to-image": "wand-sparkles", "text-to-video": "clapperboard",
  "unconditional-image-generation": "dices", "video-to-video": "repeat", "zero-shot-image-classification": "scan-eye",
  "zero-shot-object-detection": "crosshair", "text-to-3d": "box", "image-to-3d": "rotate-3d",
  "audio-classification": "audio-waveform", "audio-to-audio": "sliders-horizontal", "automatic-speech-recognition": "mic",
  "text-to-speech": "speech", "text-to-audio": "music", "voice-activity-detection": "activity",
  "tabular-classification": "table-properties", "tabular-regression": "trending-up", "time-series-forecasting": "chart-spline",
  "tabular-to-text": "table", "reinforcement-learning": "gamepad-2", "robotics": "bot", "graph-ml": "network",
};

export const GROUP_ICONS: Record<string, string> = {
  "Multimodal": "blend", "Natural Language Processing": "type", "Computer Vision": "eye", "Audio": "volume-2",
  "Tabular": "table", "Reinforcement Learning": "gamepad-2", "Other": "shapes", "Not yet classified": "folder-tree",
};

export const UI_ICONS = ["star", "download", "upload", "chevron-down", "external-link"];

const dir = join(dirname(createRequire(import.meta.url).resolve("lucide-static/package.json")), "icons");

/** One <symbol> per icon, referenced with <use href="#i-name">. */
export function sprite(names: Iterable<string>): string {
  return [...new Set(names)].map((n) => {
    const f = join(dir, `${n}.svg`);
    if (!existsSync(f)) throw new Error(`lucide icon not found: ${n}`);
    const inner = readFileSync(f, "utf8").replace(/^[\s\S]*?<svg[^>]*>/, "").replace(/<\/svg>\s*$/, "");
    return `<symbol id="i-${n}" viewBox="0 0 24 24">${inner}</symbol>`;
  }).join("");
}

export const taskIcon = (id: string) => TASK_ICONS[id] ?? "shapes";
export const groupIcon = (title: string) => GROUP_ICONS[title] ?? "shapes";
