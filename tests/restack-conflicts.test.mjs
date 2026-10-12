import { afterAll, test } from "bun:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { root } from "../scripts/install.mjs";

const jj = process.env.RESTACK_JJ || Bun.which("jj");
const mergiraf = process.env.RESTACK_MERGIRAF || Bun.which("mergiraf");
const rustc = Bun.which("rustc");
assert.ok(jj && mergiraf && rustc,
  "Conflict tests require jj, mergiraf, and rustc; RESTACK_JJ/RESTACK_MERGIRAF can select binaries.");
const profile = path.join(root, "skills/jj-clean-restack/assets/mergiraf.toml");
const sandboxes = [];

afterAll(() => {
  for (const sandbox of sandboxes) {
    assert.equal(path.dirname(sandbox), path.resolve(tmpdir()));
    assert.ok(path.basename(sandbox).startsWith("restack conflicts "));
    rmSync(sandbox, { recursive: true, force: true });
  }
});

function command(args, cwd, env, timeout = 15000) {
  const result = spawnSync(args[0], args.slice(1), {
    cwd, env, encoding: "utf8", windowsHide: true, timeout,
  });
  assert.ifError(result.error);
  return result;
}

function successful(args, cwd, env, timeout) {
  const result = command(args, cwd, env, timeout);
  assert.equal(result.status, 0, result.stdout + result.stderr);
  return result.stdout;
}

function repository() {
  const sandbox = mkdtempSync(path.join(path.resolve(tmpdir()), "restack conflicts "));
  sandboxes.push(sandbox);
  const directory = path.join(sandbox, "repo");
  const config = path.join(sandbox, "user.toml");
  writeFileSync(config, '[user]\nname = "Conflict Fixture"\nemail = "fixture@example.invalid"\n[signing]\nbehavior = "drop"\n[ui]\neditor = ["editor-must-not-run"]\n');
  const env = { ...process.env, JJ_CONFIG: config };
  successful([jj, "--no-pager", "git", "init", directory], sandbox, env);
  const args = [jj, "--no-pager", "--color", "never", "--config-file", profile,
    "--config", `merge-tools.mergiraf.program=${JSON.stringify(mergiraf.replaceAll("\\", "/"))}`];
  const repo = {
    sandbox, directory, env,
    run: (...tail) => successful([...args, ...tail], directory, env),
    attempt: (...tail) => command([...args, ...tail], directory, env),
    write(filename, content) {
      const target = path.join(directory, filename);
      mkdirSync(path.dirname(target), { recursive: true });
      writeFileSync(target, content);
    },
    id(revision = "@") { return this.run("log", "-r", revision, "--no-graph", "-T", "commit_id").trim(); },
    change(revision = "@") { return this.run("log", "-r", revision, "--no-graph", "-T", "change_id").trim(); },
    text(revision, filename = "station fixture.rs") { return this.run("file", "show", "-r", revision, `root:${filename}`); },
    conflicted(revision) { return this.run("log", "-r", `conflicts() & (${revision})`, "--no-graph", "-T", "commit_id").trim() !== ""; },
    new(parent, description) { this.run("new", parent, "-m", description); return this.change(); },
    duplicate(source, parent) {
      const ids = () => this.run("log", "-r", "all()", "--no-graph", "-T", 'commit_id ++ "\\n"').trim().split("\n");
      const before = new Set(ids());
      this.run("duplicate", source, "--onto", parent);
      const added = ids().filter((id) => !before.has(id));
      assert.equal(added.length, 1, "Identify the actual duplicate, excluding preexisting empty children");
      return this.change(added[0]);
    },
    resolve(destination, filename = "station fixture.rs") {
      const correction = this.new(destination, "Resolve structural overlap");
      this.run("resolve", "-r", correction, "--tool", "mergiraf", `root:${filename}`);
      return correction;
    },
    fold(correction, destination) {
      assert.equal(this.conflicted(correction), false);
      this.run("squash", "--from", correction, "--into", destination, "--use-destination-message");
    },
    testRust(revision, filename = "station fixture.rs", extraTests = "") {
      const build = mkdtempSync(path.join(sandbox, "build "));
      const files = this.run("file", "list", "-r", revision).trim().split("\n");
      for (const file of files) {
        const target = path.join(build, file.trim());
        mkdirSync(path.dirname(target), { recursive: true });
        writeFileSync(target, this.text(revision, file.trim()));
      }
      const source = path.join(build, filename);
      writeFileSync(source, readFileSync(source, "utf8") + extraTests);
      const executable = path.join(build, process.platform === "win32" ? "behavior.exe" : "behavior");
      // Cold Windows runners need more time for the compiler and linker.
      successful([rustc, "--test", source, "--crate-name", "behavior", "-o", executable], build, env, 60000);
      successful([executable, "--quiet"], build, env);
    },
  };
  return repo;
}

const base = `#[derive(PartialEq)]
enum Color { Red, Blue, Green }
struct Station { id: u8, occupied: bool, color: Color }
struct Lawnmower { stations: Vec<Station> }
impl Lawnmower {
    fn find_home_station(&self) -> Option<&Station> {
        self.stations.iter().find(|station| {
            station.id == 1
                && !station.occupied
                && station.color == Color::Red
        })
    }
}
#[test]
fn selects_intended_station() {
    let lawnmower = Lawnmower { stations: vec![
        Station { id: 1, occupied: false, color: Color::Red },
        Station { id: 1, occupied: false, color: Color::Blue },
        Station { id: 1, occupied: false, color: Color::Green },
    ] };
    assert!(lawnmower.find_home_station().unwrap().color == Color::Red);
}
`;

function select(text, color) {
  return text.replace(/(&& station.color == Color::|unwrap\(\).color == Color::)(Red|Blue|Green)/g, `$1${color}`);
}

function extract(text) {
  const condition = /            station.id == 1\n                && !station.occupied\n                && station.color == Color::(Red|Blue|Green)\n        \}\)\n    \}/;
  assert.match(text, condition);
  return text.replace(condition, (_, color) => `            self.is_suitable_home(station)
        })
    }
    fn is_suitable_home(&self, station: &Station) -> bool {
        station.id == 1
            && !station.occupied
            && station.color == Color::${color}
    }`);
}

function sourceStack(repo, withFixup = false) {
  repo.write("station fixture.rs", base);
  repo.run("describe", "-m", "Establish station behavior");
  const baseId = repo.id();
  repo.new(baseId, "Select blue station");
  repo.write("station fixture.rs", select(base, "Blue"));
  const feature = repo.id();
  repo.new(feature, "Extract suitability method");
  repo.write("station fixture.rs", extract(select(base, "Blue")));
  const refactor = repo.id();
  if (withFixup) {
    repo.new(refactor, "Correct selection to green");
    repo.write("station fixture.rs", extract(select(base, "Green")));
  }
  const tip = repo.id();
  repo.run("tag", "set", "original-fixture", "-r", tip);
  repo.run("bookmark", "create", "existing-source", "-r", tip);
  return { baseId, feature, refactor, tip };
}

function assertPreserved(repo, source) {
  assert.equal(repo.id("original-fixture"), source.tip);
  assert.equal(repo.id("existing-source"), source.tip);
  for (const id of [source.baseId, source.feature, source.refactor, source.tip]) {
    assert.equal(repo.id(id), id);
  }
}

test("full-file profile transfers extraction edits in both reordered steps", () => {
  const repo = repository();
  const source = sourceStack(repo);
  const refactor = repo.duplicate(source.refactor, source.baseId);
  assert.equal(repo.conflicted(refactor), true);
  const beforeResolution = repo.id(refactor);
  const correction = repo.new(refactor, "Resolve extraction overlap");
  const fullArgs = Bun.TOML.parse(readFileSync(profile, "utf8"))["merge-tools"].mergiraf["merge-args"];
  repo.run("--config", `merge-tools.mergiraf.merge-args=${JSON.stringify([...fullArgs, "--fast"])}`,
    "resolve", "-r", correction, "--tool", "mergiraf", "root:station fixture.rs");
  assert.equal(repo.conflicted(correction), true, "Fast hunk resolution misses this extraction");
  repo.run("resolve", "-r", correction, "--tool", "mergiraf", "root:station fixture.rs");
  assert.equal(repo.conflicted(correction), false, "The conflict query succeeds with empty output after resolution");
  assert.notEqual(repo.attempt("resolve", "--list", "-r", correction).status, 0,
    "resolve --list is not a successful post-resolution check");
  assert.equal(repo.id(refactor), beforeResolution, "Only the correction child is resolved");
  assert.equal(repo.text(correction), extract(base));
  repo.testRust(correction);
  repo.fold(correction, refactor);
  repo.testRust(refactor);
  repo.run("bookmark", "create", "clean-fixture", "-r", refactor);

  const feature = repo.duplicate(source.feature, refactor);
  assert.equal(repo.conflicted(feature), true);
  const featureCorrection = repo.resolve(feature);
  repo.testRust(featureCorrection);
  repo.fold(featureCorrection, feature);
  repo.testRust(feature);
  repo.run("bookmark", "set", "clean-fixture", "-r", feature);
  assert.equal(repo.id("clean-fixture"), repo.id(feature));
  assert.equal(repo.run("diff", "--from", source.tip, "--to", feature, "--summary"), "");
  assert.equal(repo.conflicted(`${source.baseId}..${feature}`), false);
  assert.equal(repo.run("log", "-r", feature, "--no-graph", "-T", "description.first_line()"), "Select blue station");
  assert.equal(repo.run("log", "-r", refactor, "--no-graph", "-T", "description.first_line()"), "Extract suitability method");
  assertPreserved(repo, source);
});

test("mapped correction repairs an owner before resolving the extracted descendant", () => {
  const repo = repository();
  const source = sourceStack(repo, true);
  const feature = repo.duplicate(source.feature, source.baseId);
  const refactor = repo.duplicate(source.refactor, feature);
  repo.testRust(feature);
  repo.testRust(refactor);
  const fixup = repo.new(refactor, "Correct selection to green");
  repo.write("station fixture.rs", extract(select(base, "Green")));
  repo.id();
  repo.run("absorb", "--from", fixup, "--into", feature, "root:station fixture.rs");

  // Absorb's line attribution does not decide who owns the moved condition.
  const repair = repo.new(feature, "Complete the mapped feature correction");
  repo.write("station fixture.rs", select(base, "Green"));
  repo.id();
  repo.testRust(repair);
  repo.fold(repair, feature);
  repo.testRust(feature);
  assert.equal(repo.conflicted(refactor), true, "The mapped correction must exercise descendant resolution");
  const correction = repo.resolve(refactor);
  repo.testRust(correction);
  repo.fold(correction, refactor);
  repo.testRust(refactor);
  assert.equal(repo.run("diff", "--from", source.tip, "--to", refactor, "--summary"), "");
  assert.equal(repo.conflicted(`${source.baseId}..${refactor}`), false);
  assertPreserved(repo, source);
});

function conflict(repo, ancestor, ...sides) {
  repo.write("station fixture.rs", ancestor);
  repo.run("describe", "-m", "Common behavior");
  const baseId = repo.id();
  const parents = sides.map((content, index) => {
    repo.new(baseId, `Side ${index + 1} changes`);
    repo.write("station fixture.rs", content);
    return repo.id();
  });
  repo.run("new", ...parents, "-m", "Conflict fixture");
  const destination = repo.change();
  assert.equal(repo.conflicted(destination), true);
  return destination;
}

test("independent additions retain both public behaviors", () => {
  const repo = repository();
  const destination = conflict(repo, "pub fn anchor() {}\n",
    "pub fn anchor() {}\npub fn alpha() -> u8 { 1 }\n",
    "pub fn anchor() {}\npub fn beta() -> u8 { 2 }\n");
  const correction = repo.resolve(destination);
  repo.testRust(correction, "station fixture.rs",
    "\n#[test] fn both_additions_survive() { assert_eq!(alpha(), 1); assert_eq!(beta(), 2); }\n");
  repo.fold(correction, destination);
  assert.equal(repo.conflicted(destination), false);
});

test("incompatible behavior remains a native jj conflict", () => {
  const repo = repository();
  const destination = conflict(repo, "fn retries() -> usize { 3 }\n",
    "fn retries() -> usize { 5 }\n", "fn retries() -> usize { 8 }\n");
  const unchanged = repo.id(destination);
  const correction = repo.resolve(destination);
  assert.equal(repo.conflicted(correction), true);
  const text = repo.text(correction);
  for (const value of [3, 5, 8]) assert.ok(text.includes(`{ ${value} }`));
  assert.equal(repo.id(destination), unchanged);
});

test("partial structural output keeps unresolved alternatives", () => {
  const repo = repository();
  const retries = (value) => `\nfn retries() -> usize { ${value} }\n`;
  const destination = conflict(repo, base + retries(3), extract(base) + retries(5),
    select(base, "Blue") + retries(8));
  const correction = repo.resolve(destination);
  assert.equal(repo.conflicted(correction), true);
  const text = repo.text(correction);
  assert.ok(text.includes("fn is_suitable_home"));
  assert.ok(text.includes("&& station.color == Color::Blue"));
  assert.match(text, /<<<<<<<|%%%%%%%/);
  assert.ok(text.includes("{ 5 }") && text.includes("{ 8 }"));
});

test("missing resolver leaves the correction and destination intact", () => {
  const repo = repository();
  const destination = conflict(repo, "fn value() -> i32 { 1 }\n",
    "fn value() -> i32 { 2 }\n", "fn value() -> i32 { 3 }\n");
  const correction = repo.new(destination, "Resolve with unavailable tool");
  const before = repo.id(correction);
  const original = repo.id(destination);
  const missing = path.join(repo.sandbox, "does-not-exist").replaceAll("\\", "/");
  const result = repo.attempt("--config", `merge-tools.mergiraf.program=${JSON.stringify(missing)}`,
    "resolve", "-r", correction, "--tool", "mergiraf", "root:station fixture.rs");
  assert.notEqual(result.status, 0);
  assert.equal(repo.id(correction), before);
  assert.equal(repo.id(destination), original);
  assert.equal(repo.conflicted(correction), true);
});

test("three-sided conflicts are preserved for guided resolution", () => {
  const repo = repository();
  const destination = conflict(repo, "fn value() -> i32 { 1 }\n",
    "fn value() -> i32 { 2 }\n", "fn value() -> i32 { 3 }\n", "fn value() -> i32 { 4 }\n");
  const correction = repo.new(destination, "Inspect unsupported conflict");
  const before = repo.id(correction);
  const result = repo.attempt("resolve", "-r", correction, "--tool", "mergiraf", "root:station fixture.rs");
  assert.notEqual(result.status, 0);
  assert.equal(repo.id(correction), before);
  assert.equal(repo.conflicted(correction), true);
});

test("guided cross-file move preserves its compatibility boundary", () => {
  const repo = repository();
  const lib = (acceptZero, moved) => `${moved ? "mod decoder;\n" : ""}mod parser;
pub use parser::valid;
#[test] fn boundary() { assert_eq!(valid(0), ${acceptZero}); assert!(parser::valid(1)); }
`;
  const implementation = (strict) => `pub fn valid(n: i32) -> bool { n ${strict ? ">" : ">="} 0 }\n`;
  repo.write("lib.rs", lib(true, false));
  repo.write("parser.rs", implementation(false));
  repo.run("describe", "-m", "Existing parser API");
  const baseId = repo.id();
  repo.new(baseId, "Reject zero");
  repo.write("lib.rs", lib(false, false));
  repo.write("parser.rs", implementation(true));
  const featureId = repo.id();
  repo.new(featureId, "Move implementation while retaining parser API");
  repo.write("lib.rs", lib(false, true));
  repo.write("parser.rs", "pub use crate::decoder::valid;\n");
  repo.write("decoder.rs", implementation(true));
  const original = repo.id();
  repo.run("tag", "set", "original-fixture", "-r", original);
  repo.run("bookmark", "create", "existing-source", "-r", original);

  const refactor = repo.new(baseId, "Move implementation while retaining parser API");
  repo.write("lib.rs", lib(true, true));
  repo.write("parser.rs", "pub use crate::decoder::valid;\n");
  repo.write("decoder.rs", implementation(false));
  repo.id();
  repo.testRust(refactor, "lib.rs");
  const feature = repo.new(refactor, "Reject zero");
  repo.write("lib.rs", lib(false, true));
  repo.write("decoder.rs", implementation(true));
  repo.id();
  repo.testRust(feature, "lib.rs");
  assert.equal(repo.run("diff", "--from", original, "--to", feature, "--summary"), "");
  assert.equal(repo.id("original-fixture"), original);
  assert.equal(repo.id("existing-source"), original);
  assert.equal(repo.conflicted(`${baseId}..${feature}`), false);
});
