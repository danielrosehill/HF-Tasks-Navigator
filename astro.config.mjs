import { defineConfig } from "astro/config";

// Single self-contained page: CSS inlined, scripts are is:inline, so dist/index.html works from file://.
export default defineConfig({
  build: { format: "file", inlineStylesheets: "always" },
  devToolbar: { enabled: false },
});
