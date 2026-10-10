import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { root } from "./install.mjs";

export function verifySkill(directory) {
  const entry = readFileSync(path.join(directory, "SKILL.md"), "utf8");
  const header = entry.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  if (!header || !/^name:\s*\S+/m.test(header) || !/^description:\s*\S+/m.test(header)) {
    throw new Error(`Missing skill name/description: ${directory}`);
  }
  const name = header.match(/^name:\s*([^\r\n]+)/m)[1].trim();
  if (name !== path.basename(directory))
    throw new Error(`Skill name does not match folder: ${directory}`);
  function visit(folder) {
    for (const item of readdirSync(folder, { withFileTypes: true })) {
      const filename = path.join(folder, item.name);
      if (item.isSymbolicLink()) throw new Error(`Skill resources must be real files: ${filename}`);
      if (item.isDirectory()) {
        visit(filename);
        continue;
      }
      if (!item.name.endsWith(".md")) continue;
      const text = readFileSync(filename, "utf8");
      for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
        const target = match[1].split("#")[0];
        if (!target || /^[a-z]+:\/\//i.test(target)) continue;
        const resolved = path.resolve(folder, target);
        if (!resolved.startsWith(directory + path.sep) || !existsSync(resolved)) {
          throw new Error(`Missing or non-local reference in ${filename}: ${target}`);
        }
      }
    }
  }
  visit(directory);
}

export function verifyRepository() {
  const skills = path.join(root, "skills");
  const directories = readdirSync(skills, { withFileTypes: true }).filter((item) =>
    item.isDirectory(),
  );
  for (const item of directories) verifySkill(path.join(skills, item.name));
  console.log(`Verified ${directories.length} skill resource trees.`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    verifyRepository();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
