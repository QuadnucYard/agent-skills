import { test } from "bun:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, readdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { root } from "../scripts/install.mjs";
import { verifySkill } from "../scripts/verify.mjs";

async function runInstall(skills) {
  const sandbox = mkdtempSync(path.join(tmpdir(), "agent-skills-test-"));
  const home = path.join(sandbox, "home");
  const bin = path.join(sandbox, "bin");
  mkdirSync(bin);
  const env = Object.fromEntries(
    Object.entries(process.env).filter(([key]) => key.toLowerCase() !== "path"),
  );
  env.PATH = bin;
  assert.equal(Bun.which("node", { PATH: bin }), null, "Node must be unavailable");
  const result = Bun.spawn(
    [process.execPath, path.join(root, "scripts", "install.mjs"), "--skill", ...skills, "--yes"],
    {
      cwd: sandbox,
      stdout: "pipe",
      stderr: "pipe",
      env: {
        ...env,
        HOME: home,
        USERPROFILE: home,
        CODEX_HOME: path.join(home, ".codex"),
        DISABLE_TELEMETRY: "1",
        DO_NOT_TRACK: "1",
        CI: "1",
      },
    },
  );
  const [status, stdout, stderr] = await Promise.all([
    result.exited,
    new Response(result.stdout).text(),
    new Response(result.stderr).text(),
  ]);
  assert.equal(status, 0, stdout + stderr);
  return sandbox;
}

test("real skills CLI installs available skills with every resource", async () => {
  const sandbox = await runInstall(["*"]);
  const source = path.join(root, "skills");
  const installed = path.join(sandbox, ".agents", "skills");
  const names = readdirSync(source);
  assert.ok(names.length > 0, "Repository must contain installable skills");
  assert.deepEqual(readdirSync(installed).sort(), names.sort());
  function compare(a, b) {
    assert.deepEqual(readdirSync(b).sort(), readdirSync(a).sort());
    for (const entry of readdirSync(a, { withFileTypes: true })) {
      if (entry.isDirectory()) compare(path.join(a, entry.name), path.join(b, entry.name));
      else
        assert.deepEqual(
          readFileSync(path.join(b, entry.name)),
          readFileSync(path.join(a, entry.name)),
        );
    }
  }
  for (const name of names) {
    compare(path.join(source, name), path.join(installed, name));
    verifySkill(path.join(installed, name));
  }
}, 30000);
