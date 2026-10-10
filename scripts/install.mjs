import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const root = fileURLToPath(new URL("../", import.meta.url));

export const skillDependencies = Object.freeze({
  "jj-review-restack": ["jj-clean-restack"],
});

export function expandSkillDependencies(input) {
  const args = [...input];
  const selected = [];
  for (let index = 0; index < args.length; index++) {
    if (!["--skill", "-s"].includes(args[index])) continue;
    while (args[index + 1] && !args[index + 1].startsWith("-")) {
      selected.push(args[++index]);
    }
  }
  if (selected.includes("*")) return args;

  const seen = new Set(selected);
  const queue = [...selected];
  const dependencies = [];
  while (queue.length) {
    const skill = queue.shift();
    for (const dependency of skillDependencies[skill] ?? []) {
      if (seen.has(dependency)) continue;
      seen.add(dependency);
      queue.push(dependency);
      dependencies.push(dependency);
    }
  }
  if (dependencies.length) args.push("--skill", ...dependencies);
  return args;
}

export async function install(input = process.argv.slice(2)) {
  let args = [...input];
  let source = root;
  const sourceIndex = args.indexOf("--source");
  if (sourceIndex !== -1) {
    if (!args[sourceIndex + 1] || args[sourceIndex + 1].startsWith("-")) {
      throw new Error("--source requires a repository URL or local path");
    }
    source = args.splice(sourceIndex, 2)[1];
  }
  const cli = path.join(root, "node_modules", "skills", "bin", "cli.mjs");
  if (!existsSync(cli))
    throw new Error("Run bun install --frozen-lockfile in the skills repository first.");
  if (!args.some((arg) => ["--agent", "-a"].includes(arg))) args.push("--agent", "codex");
  if (!args.some((arg) => ["--skill", "-s"].includes(arg))) args.push("--skill", "*");
  args = expandSkillDependencies(args);
  const result = Bun.spawn([process.execPath, cli, "add", source, ...args], {
    cwd: process.cwd(),
    stdin: "inherit",
    stdout: "inherit",
    stderr: "inherit",
    env: process.env,
  });
  return await result.exited;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    process.exitCode = await install();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
