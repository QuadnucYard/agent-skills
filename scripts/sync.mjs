import { fileURLToPath } from "node:url";
import { install, root } from "./install.mjs";

function git(args) {
  const result = Bun.spawnSync(["git", "-C", root, ...args], { stdout: "pipe", stderr: "pipe" });
  if (result.exitCode !== 0)
    throw new Error(new TextDecoder().decode(result.stderr).trim() || "Git command failed");
  return new TextDecoder().decode(result.stdout).trim();
}

try {
  if (process.argv.length > 2 && !process.argv.includes("--install"))
    throw new Error("Installation options require --install.");
  if (git(["status", "--porcelain"]))
    throw new Error("Commit or preserve local changes before syncing.");
  console.log(git(["pull", "--ff-only"]));
  const check = Bun.spawn(
    [process.execPath, fileURLToPath(new URL("./verify.mjs", import.meta.url))],
    {
      cwd: root,
      stdin: "inherit",
      stdout: "inherit",
      stderr: "inherit",
    },
  );
  if ((await check.exited) !== 0)
    throw new Error("Repository verification failed; installation was skipped.");
  if (process.argv.includes("--install")) {
    process.exitCode = await install(process.argv.slice(2).filter((arg) => arg !== "--install"));
  } else if (process.argv.length > 2) {
    throw new Error("Installation options require --install.");
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
