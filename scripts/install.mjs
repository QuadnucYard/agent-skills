import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

export const root = fileURLToPath(new URL("../", import.meta.url));

export async function install(input = process.argv.slice(2)) {
  const args = [...input];
  let source = root;
  const sourceIndex = args.indexOf("--source");
  if (sourceIndex !== -1) {
    if (!args[sourceIndex + 1] || args[sourceIndex + 1].startsWith("-")) {
      throw new Error("--source requires a repository URL or local path");
    }
    source = args.splice(sourceIndex, 2)[1];
  }
  const cli = path.join(root, "node_modules", "skills", "bin", "cli.mjs");
  if (!existsSync(cli)) throw new Error("Run bun install --frozen-lockfile in the skills repository first.");
  if (!args.some((arg) => ["--agent", "-a"].includes(arg))) args.push("--agent", "codex");
  if (!args.some((arg) => ["--skill", "-s"].includes(arg))) args.push("--skill", "*");
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
