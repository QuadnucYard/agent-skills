"""Track textual edit spans through frozen, linear jj deltas supplied by Nu.

No repository access, subprocesses, third-party packages, or history mutation.
Ranges are zero-based half-open internally; reports use one-based start/count.
"""

import base64
import difflib
import json
import sys
from collections.abc import Sequence
from typing import Literal, NotRequired, TypedDict, cast


AnalysisMode = Literal["touches", "dependencies"]
Relation = Literal["overlap", "adjacent", "same-file", "uncertain", "metadata", "rename", "path"]
HunkKind = Literal["text", "whole-file", "metadata", "path"]
Opcode = tuple[str, int, int, int, int]
Range = tuple[int, int]


class Snapshot(TypedDict):
    path: str
    kind: str
    executable: bool
    content: str | None
    issue: str | None


class Entry(TypedDict):
    status: str
    before: Snapshot
    after: Snapshot
    old: NotRequired[list[str]]
    new: NotRequired[list[str]]
    ops: NotRequired[Sequence[Opcode]]
    issue: NotRequired[str]


class Change(TypedDict):
    change: str
    description: str
    entries: list[Entry]
    conflicts: NotRequired[list[str]]


class AnalysisRequest(TypedDict):
    mode: AnalysisMode
    base: str
    tip: str
    changes: list[Change]
    path: str | None
    hunk: str | None
    whole_file: NotRequired[bool]


class Span(TypedDict):
    start: int
    count: int


class Hunk(TypedDict):
    change: str
    description: str
    hunk: str
    path: str
    kind: HunkKind
    before: Span
    after: Span


class EventIdentity(TypedDict):
    source: str
    hunk: str
    later: str
    description: str
    path: str


class Event(EventIdentity):
    relation: Relation
    before: NotRequired[Span]
    after: NotRequired[Span]
    from_path: NotRequired[str]


class Issue(TypedDict):
    change: str
    path: str
    reason: str


class Dependency(TypedDict):
    prerequisite: str
    dependent: str
    hunk: str
    path: str
    evidence: Relation
    classification: Literal["candidate"]


class Scope(TypedDict):
    base: str
    tip: str


class AnalysisReport(TypedDict):
    schema_version: Literal[1]
    mode: AnalysisMode
    scope: Scope
    complete: bool
    hunks: list[Hunk]
    events: list[Event]
    dependencies: list[Dependency]
    limitations: list[str]
    issues: list[Issue]


def span(start: int, end: int) -> Span:
    return {"start": start + 1, "count": end - start}


def lines(file: Snapshot) -> list[str]:
    issue = file["issue"]
    if issue:
        raise ValueError(issue)
    if file["kind"] == "absent":
        return []
    if file["kind"] != "file":
        raise ValueError("unsupported file kind: " + file["kind"])
    content = file["content"]
    if content is None:
        raise ValueError("missing file content")
    data = base64.b64decode(content, validate=True)
    if b"\0" in data:
        raise ValueError("binary content")
    # Keep CRLF and missing-final-newline differences observable.
    parts = data.decode("utf-8").split("\n")
    result = [part + "\n" for part in parts[:-1]]
    if parts[-1]:
        result.append(parts[-1])
    if len(result) > 20000:
        raise ValueError("file exceeds 20000-line analysis limit")
    return result


def prepare(changes: list[Change]) -> None:
    for change in changes:
        for entry in change["entries"]:
            try:
                old, new = lines(entry["before"]), lines(entry["after"])
                if len(old) * len(new) > 25000000:
                    raise ValueError("diff exceeds 25000000 line-pair analysis budget")
                entry["old"], entry["new"] = old, new
                entry["ops"] = difflib.SequenceMatcher(
                    None, old, new, autojunk=False
                ).get_opcodes()
            except ValueError as error:
                entry["issue"] = str(error)


def occurrences(haystack: Sequence[str], needle: Sequence[str]) -> int:
    if not needle:
        return 0
    return sum(haystack[i:i + len(needle)] == needle
               for i in range(len(haystack) - len(needle) + 1))


def relation(start: int, end: int, left: int, right: int) -> Literal["overlap", "adjacent"] | None:
    if start == end or left == right:
        if start == end and left == right:
            return "overlap" if start == left else None
        if start == end:
            return "overlap" if left < start < right else (
                "adjacent" if start in (left, right) else None)
        return "overlap" if start < left < end else (
            "adjacent" if left in (start, end) else None)
    if max(start, left) < min(end, right):
        return "overlap"
    if end == left or right == start:
        return "adjacent"
    return None


def translate(start: int, end: int, ops: Sequence[Opcode]) -> list[Range]:
    """Carry surviving pieces, replacement content, and deletion tombstones."""
    pieces: list[Range] = []
    for tag, a, b, c, d in ops:
        if tag == "equal":
            lo, hi = max(start, a), min(end, b)
            if lo < hi or (start == end and a <= start <= b):
                pieces.append((c + lo - a, c + hi - a))
        elif relation(start, end, a, b) == "overlap":
            pieces.append((c, d))
    if not pieces:
        # A tombstone at an edit boundary follows the end of the preceding edit.
        offset = 0
        for _, a, b, c, d in ops:
            if b <= start:
                offset = d - b
        pieces.append((start + offset, end + offset))
    return sorted(set(pieces))


def make_event(identity: EventIdentity, kind: Relation, before: Span | None = None,
               after: Span | None = None, from_path: str | None = None) -> Event:
    result: Event = {
        "source": identity["source"], "hunk": identity["hunk"],
        "later": identity["later"], "description": identity["description"],
        "path": identity["path"], "relation": kind,
    }
    if before is not None:
        result["before"] = before
    if after is not None:
        result["after"] = after
    if from_path is not None:
        result["from_path"] = from_path
    return result


def moved_candidates(entry: Entry, tracked: Sequence[Range], later: Change) -> list[str]:
    """Flag exact removed fragments found in other insertions; never infer identity."""
    candidates: set[str] = set()
    for operation in entry["ops"]:
        tag, a, b, _, _ = operation
        if tag not in ("delete", "replace"):
            continue
        for lo, hi in tracked:
            start, end = max(lo, a), min(hi, b)
            if start >= end:
                continue
            fragment = entry["old"][start:end]
            for other in later["entries"]:
                if other.get("issue"):
                    continue
                for other_op in other["ops"]:
                    kind, _, _, c, d = other_op
                    if kind not in ("insert", "replace") or (other is entry and other_op == operation):
                        continue
                    if occurrences(other["new"][c:d], fragment):
                        candidates.add(other["after"]["path"])
    return sorted(candidates)


def analyze(request: AnalysisRequest) -> AnalysisReport:
    changes = request["changes"]
    prepare(changes)
    report: AnalysisReport = {
        "schema_version": 1, "mode": request["mode"],
        "scope": {"base": request["base"], "tip": request["tip"]},
        "complete": True, "hunks": [], "events": [], "dependencies": [], "issues": [],
        "limitations": [
            "Textual evidence does not establish semantic dependencies or hunk ownership.",
            "Moves/extractions without a recorded rename require manual lineage review.",
        ],
    }
    issues: list[Issue] = [
        {"change": revision["change"], "path": name, "reason": "native jj conflict"}
        for revision in changes for name in revision.get("conflicts", [])
    ]
    selected_hunk = False
    selected_path = False
    for index, source in enumerate(changes):
        if request["mode"] == "touches" and index > 0:
            break
        counter = 0
        for initial in source["entries"]:
            name = initial["after"]["path"]
            path_match = request.get("path") in (
                None, name, initial["before"]["path"])
            if path_match:
                selected_path = True
            if initial.get("issue"):
                if path_match:
                    issues.append({"change": source["change"], "path": name,
                                   "reason": initial["issue"]})
                continue
            seeds: list[tuple[HunkKind, int, int, int, int]] = [
                ("text", a, b, c, d) for tag, a, b, c, d in initial["ops"] if tag != "equal"
            ]
            if request.get("whole_file"):
                seeds = [("whole-file", 0, len(initial["old"]), 0, len(initial["new"]))]
            else:
                if initial["status"] in ("added", "removed", "renamed", "copied"):
                    seeds.append(("path", 0, 0, 0, 0))
                if (initial["before"]["kind"] == initial["after"]["kind"] == "file"
                        and initial["before"]["executable"] != initial["after"]["executable"]):
                    seeds.append(("metadata", 0, 0, 0, 0))
            for hunk_kind, a, b, c, d in seeds:
                counter += 1
                hunk_id = "h" + str(counter)
                if not path_match or request.get("hunk") not in (None, hunk_id):
                    continue
                selected_hunk = True
                hunk: Hunk = {"change": source["change"], "description": source["description"],
                        "hunk": hunk_id, "path": name, "kind": hunk_kind,
                        "before": span(a, b), "after": span(c, d)}
                report["hunks"].append(hunk)
                tracked: list[Range] = [(c, d)]
                current_path = name
                alive = initial["after"]["kind"] != "absent"
                for later in changes[index + 1:]:
                    relevant = [entry for entry in later["entries"]
                                if entry["before"]["path"] == current_path
                                or entry["after"]["path"] == current_path]
                    for entry in relevant:
                        event: EventIdentity = {"source": source["change"], "hunk": hunk_id,
                                 "later": later["change"], "description": later["description"],
                                 "path": entry["after"]["path"]}
                        if entry.get("issue"):
                            issues.append({"change": later["change"], "path": current_path,
                                           "reason": entry["issue"]})
                            report["events"].append(make_event(event, "uncertain"))
                            # Resume only after an explicit known mapping; do not reuse stale offsets.
                            tracked = []
                            continue
                        if not tracked:
                            report["events"].append(make_event(event, "uncertain"))
                            continue
                        if entry["status"] == "copied" and entry["before"]["path"] == current_path:
                            issues.append({"change": later["change"], "path": current_path,
                                           "reason": "copy creates another possible lineage"})
                            report["events"].append(make_event(event, "uncertain"))
                            continue
                        if not alive:
                            report["events"].append(make_event(event, "uncertain"))
                            issues.append({"change": later["change"], "path": current_path,
                                           "reason": "path reused after deletion"})
                            continue
                        if hunk_kind in ("metadata", "path"):
                            report["events"].append(make_event(
                                event, "path" if hunk_kind == "path" else "same-file"))
                        else:
                            hits: list[Event] = []
                            for tag, left, right, new_left, new_right in entry["ops"]:
                                if tag == "equal":
                                    continue
                                kinds = [relation(lo, hi, left, right) for lo, hi in tracked]
                                kind: Literal["overlap", "adjacent"] | None = "overlap" if "overlap" in kinds else (
                                    "adjacent" if "adjacent" in kinds else None)
                                if kind:
                                    hits.append(make_event(event, kind, span(left, right), span(new_left, new_right)))
                            for lo, hi in tracked:
                                needle = entry["old"][lo:hi]
                                if needle and (occurrences(entry["old"], needle) > 1
                                               or occurrences(entry["new"], needle) > 1):
                                    issues.append({"change": later["change"], "path": current_path,
                                                   "reason": "repeated tracked text makes alignment ambiguous"})
                            candidates = moved_candidates(entry, tracked, later)
                            if candidates:
                                issues.append({"change": later["change"], "path": current_path,
                                               "reason": "possible move/extraction into: " + ", ".join(candidates)})
                            report["events"].extend(hits or [make_event(event, "same-file")])
                            if any(hit["relation"] == "overlap" and hit["after"]["count"] == 0
                                   for hit in hits):
                                issues.append({"change": later["change"], "path": current_path,
                                               "reason": "tracked text deleted; unrecorded moves require review"})
                            tracked = sorted(set(piece for lo, hi in tracked
                                                 for piece in translate(lo, hi, entry["ops"])))
                        if entry["before"]["executable"] != entry["after"]["executable"]:
                            report["events"].append(make_event(event, "metadata"))
                        if entry["status"] == "renamed":
                            report["events"].append(make_event(event, "rename", from_path=current_path))
                            current_path = entry["after"]["path"]
                        alive = entry["after"]["kind"] != "absent"
    if request.get("path") is not None and not selected_path:
        raise ValueError("--path is not changed by the interested change")
    if request.get("hunk") is not None and not selected_hunk:
        raise ValueError("--hunk does not identify an analyzed source hunk")
    seen: set[tuple[str, str, str, str, Relation]] = set()
    hunk_kinds = {(hunk["change"], hunk["hunk"]): hunk["kind"] for hunk in report["hunks"]}
    for event in report["events"]:
        owner_kind = hunk_kinds[event["source"], event["hunk"]]
        eligible = (event["relation"] == "metadata" if owner_kind == "metadata" else
                    event["relation"] == "path" if owner_kind == "path" else
                    event["relation"] in ("overlap", "rename"))
        if not eligible:
            continue
        key = (event["source"], event["later"], event["hunk"], event["path"], event["relation"])
        if key not in seen:
            seen.add(key)
            report["dependencies"].append({
                "prerequisite": event["source"], "dependent": event["later"],
                "hunk": event["hunk"], "path": event["path"],
                "evidence": event["relation"], "classification": "candidate",
            })
    report["issues"] = list({(issue["change"], issue["path"], issue["reason"]): issue for issue in issues}.values())
    report["complete"] = not report["issues"]
    return report


def main() -> int:
    try:
        # Nu owns the transport schema. Keep JSON's dynamic type at this one boundary.
        request = cast(AnalysisRequest, json.load(sys.stdin))
        result = analyze(request)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
