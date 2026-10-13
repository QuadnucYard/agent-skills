use history-common.nu *

# Find later file/hunk touches or candidate textual dependencies in a linear stack.
def main [
    mode: string # touches or dependencies
    --base: string # Excluded ancestor; required
    --tip: string # Explicit included tip; required
    --change: string # Interested change; required for touches
    --path: string # Exact repository-relative path at the interested change
    --whole-file # Track the entire file at --change, even if that change did not edit it
    --hunk: string # Hunk ID from a preceding report, e.g. h1
    --repository: string = "."
    --jj: string = "jj"
    --python: string = "python3" # Use --python python on Windows if needed
    --max-commits: int = 500
    --max-file-bytes: int = 1048576
    --json # Print machine-readable JSON; otherwise return a Nu record
] {
    if $mode not-in [touches dependencies] or $base == null or $tip == null {
        error make {msg: "Use touches or dependencies with explicit --base and --tip"}
    }
    if $max_commits < 1 or $max_file_bytes < 1 {
        error make {msg: "Resource limits must be positive"}
    }
    if $mode == touches and $change == null {
        error make {msg: "touches requires --change (the file's starting revision)"}
    }
    if $mode == dependencies and ($change != null or $path != null or $hunk != null or $whole_file) {
        error make {msg: "dependencies analyzes the complete stack; selectors belong to touches"}
    }
    if $whole_file and ($path == null or $hunk != null) {
        error make {msg: "--whole-file requires --path and cannot be combined with --hunk"}
    }
    let frozen = (session $repository $jj)
    let scope = (stack $frozen $base $tip $max_commits)
    let interested = (if $change != null { revision $frozen $change } else { null })
    if $interested != null and $interested.id not-in ($scope.changes | get id) and not ($whole_file and $interested.id == $scope.base.id) {
        error make {msg: "--change must belong to BASE..TIP"}
    }
    let selected = (if $mode == dependencies { $scope.changes } else if $interested.id == $scope.base.id {
        [$interested] | append $scope.changes
    } else { $scope.changes | skip until {|rev| $rev.id == $interested.id} })
    let changes = ($selected | each {|rev|
        if $whole_file and $rev.id == $interested.id {
            let matching = (snapshot $frozen $rev | where path == $path)
            if ($matching | length) != 1 {
                error make {msg: "--path must exist at --change for --whole-file"}
            }
            let content = (file-content $frozen $rev.id ($matching | first) $max_file_bytes)
            $rev | insert entries [{status: modified, before: $content, after: $content}]
        } else {
            delta $frozen $rev $max_file_bytes
        }
    })
    let report = (python-analysis $python {
        mode: $mode, base: $scope.base.change, tip: $scope.tip.change,
        changes: $changes, path: $path, hunk: $hunk, whole_file: $whole_file
    })
    if $json { $report | to json -r } else { $report }
}
