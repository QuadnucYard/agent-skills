# Shared read-only jj access. All paths and revision identities stay structured.
export def jj-read [session: record, args: list<string>] {
    let result = (do {
        run-external ...[$session.jj --no-pager --color never --ignore-working-copy
            --at-operation $session.operation --repository $session.repository] ...$args
    } | complete)
    if $result.exit_code != 0 {
        # Do not echo jj diagnostics containing full commit/operation IDs.
        error make {msg: $"jj ($args | first) failed; check the revision, repository, and jj capabilities"}
    }
    $result.stdout
}

export def session [repository: string, jj: string] {
    let initial = {repository: ($repository | path expand), jj: $jj, operation: "@"}
    let operation = (jj-read $initial [op log --limit "1" --no-graph -T id] | str trim)
    let pinned = ($initial | update operation $operation)
    $pinned | update repository (jj-read $pinned [root] | str trim)
}

export def revisions [session: record, expression: string] {
    let template = ('"{\"revision\":" ++ json(self) ++ '
        + '",\"conflicts\":[" ++ conflicted_files.map(|f| json(f.path())).join(",") ++ "]}\n"')
    jj-read $session [log -r $expression --no-graph --reversed -T $template]
    | from json --objects | each {|record|
        let rev = $record.revision
        {
            id: $rev.commit_id, parents: $rev.parents,
            change: ($rev.change_id | str substring 0..11),
            description: ($rev.description | split row "\n" | first), conflicts: $record.conflicts
        }
    }
}

export def revision [session: record, expression: string] {
    let found = (revisions $session $expression)
    if ($found | length) != 1 {
        error make {msg: "Each revision argument must resolve to exactly one revision"}
    }
    $found | first
}

export def stack [session: record, base: string, tip: string, limit: int] {
    let start = (revision $session $base)
    let end = (revision $session $tip)
    let chain = (revisions $session $"($start.id)::($end.id)")
    if ($chain | is-empty) or ($chain | first | get id) != $start.id or ($chain | last | get id) != $end.id {
        error make {msg: "BASE must be an ancestor of TIP"}
    }
    let suffix = ($chain | skip 1)
    if ($suffix | length) > $limit {
        error make {msg: "Stack exceeds --max-commits; select a smaller scope or raise the limit"}
    }
    mut parent = $start.id
    for rev in $suffix {
        if ($rev.parents | length) != 1 or $rev.parents.0 != $parent {
            error make {msg: "Analysis requires a linear stack without merges"}
        }
        $parent = $rev.id
    }
    if ($suffix | get change | uniq | length) != ($suffix | length) {
        error make {msg: "Stack contains ambiguous versions or colliding short change IDs"}
    }
    {base: $start, tip: $end, changes: $suffix}
}

export def file-content [session: record, rev: string, file: record, max_bytes: int] {
    if $file.kind != "file" {
        return ($file | merge {content: null, issue: (if $file.kind == "absent" {null} else {$"unsupported file kind: ($file.kind)"})})
    }
    let content = (jj-read $session [file show -r $rev $'root-file:($file.path | to json -r)'])
    if ($content | into binary | bytes length) > $max_bytes {
        return ($file | merge {content: null, issue: "file exceeds --max-file-bytes"})
    }
    $file | merge {content: ($content | encode base64), issue: null}
}

export def delta [session: record, rev: record, max_bytes: int] {
    if ($rev.parents | length) != 1 {
        error make {msg: "A source change must have exactly one parent"}
    }
    let template = ('"{\"status\":" ++ json(status) ++ '
        + '",\"old_path\":" ++ json(source.path()) ++ '
        + '",\"old_kind\":" ++ json(if(source.normal_value() || source.conflict(), source.file_type(), "absent")) ++ '
        + '",\"old_executable\":" ++ json(source.executable()) ++ '
        + '",\"new_path\":" ++ json(target.path()) ++ '
        + '",\"new_kind\":" ++ json(if(target.normal_value() || target.conflict(), target.file_type(), "absent")) ++ '
        + '",\"new_executable\":" ++ json(target.executable()) ++ "}\n"')
    let entries = (jj-read $session [diff -r $rev.id -T $template]
        | from json --objects | each {|entry|
            {
                status: $entry.status,
                before: (file-content $session $rev.parents.0 {
                    path: $entry.old_path, kind: $entry.old_kind, executable: $entry.old_executable
                } $max_bytes),
                after: (file-content $session $rev.id {
                    path: $entry.new_path, kind: $entry.new_kind, executable: $entry.new_executable
                } $max_bytes)
            }
        })
    $rev | insert entries $entries
}

export def snapshot [session: record, rev: record] {
    let template = ('"{\"path\":" ++ json(path) ++ '
        + '",\"kind\":" ++ json(file_type) ++ '
        + '",\"executable\":" ++ json(executable) ++ "}\n"')
    jj-read $session [file list -r $rev.id -T $template] | from json --objects
}

export def absent [name: string] {
    {path: $name, kind: absent, executable: false, content: null, issue: null}
}

export def python-analysis [python: string, request: record] {
    let helper = ($env.FILE_PWD | path join hunk_lineage.py)
    let result = ($request | to json -r | do { run-external ...[$python -B $helper] } | complete)
    if $result.exit_code != 0 {
        error make {msg: $"Hunk analysis failed: ($result.stderr | str trim)"}
    }
    $result.stdout | from json
}

