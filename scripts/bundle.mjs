import { mkdirSync, readFileSync, writeFileSync, readdirSync, copyFileSync } from "node:fs";
import path from "node:path";
import { root } from "./install.mjs";

const source = path.join(root, "skills", "jj-clean-restack");
const destination = path.join(root, "skills", "jj-review-restack", "references", "restack");
mkdirSync(path.join(destination, "references"), { recursive: true });
const entry = readFileSync(path.join(source, "SKILL.md"), "utf8").replace(
  /^---\r?\n[\s\S]*?\r?\n---\r?\n/,
  "",
);
writeFileSync(path.join(destination, "overview.md"), entry);
for (const name of readdirSync(path.join(source, "references"))) {
  copyFileSync(path.join(source, "references", name), path.join(destination, "references", name));
}
console.log("Bundled jj-clean-restack guidance for standalone jj-review-restack installation.");
