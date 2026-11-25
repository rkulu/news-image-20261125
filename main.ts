// News-image entry for 25 November 2026 (Node 22, standard library only).
// The front page itself is entry.png next to this file, drawn by
// draw_entry.py: one image summing up the world news of Wednesday
// 25 November 2026. This program writes that exact image out to
// /output/entry.png, byte for byte, every run.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, "entry.png"));
writeFileSync(join(outDir, "entry.png"), bytes);
