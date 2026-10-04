[CmdletBinding()]
param(
    [Parameter()]
    [string]$Repository = "."
)

$repo = (Resolve-Path -LiteralPath $Repository).Path
$jj = Join-Path $repo ".jj"
$heads = Join-Path $jj "repo\op_heads\heads"
$operations = Join-Path $jj "repo\op_store\operations"
$checkout = Join-Path $jj "working_copy\checkout"

function Convert-Id([byte[]]$Bytes) {
    [Convert]::ToHexString($Bytes).ToLowerInvariant()
}

function Read-Varint([byte[]]$Bytes, [ref]$Offset) {
    [UInt64]$value = 0
    [int]$shift = 0
    while ($true) {
        if ($Offset.Value -ge $Bytes.Length -or $shift -gt 63) {
            throw "Invalid protobuf varint"
        }
        [byte]$current = $Bytes[$Offset.Value]
        $Offset.Value++
        $value = $value -bor (([UInt64]($current -band 0x7f)) -shl $shift)
        if (($current -band 0x80) -eq 0) {
            return $value
        }
        $shift += 7
    }
}

function Read-Operation([string]$OperationId) {
    $path = Join-Path $operations $OperationId
    if (-not (Test-Path -LiteralPath $path)) {
        return [PSCustomObject]@{ View = $null; Parents = @(); Error = "Operation record is absent" }
    }

    $bytes = [System.IO.File]::ReadAllBytes($path)
    [int]$offset = 0
    $view = $null
    $parents = [System.Collections.Generic.List[string]]::new()
    try {
        while ($offset -lt $bytes.Length) {
            [UInt64]$tag = Read-Varint $bytes ([ref]$offset)
            [int]$field = $tag -shr 3
            [int]$wire = $tag -band 7
            switch ($wire) {
                0 { [void](Read-Varint $bytes ([ref]$offset)) }
                1 { $offset += 8 }
                2 {
                    [int]$length = Read-Varint $bytes ([ref]$offset)
                    if ($length -lt 0 -or $offset + $length -gt $bytes.Length) {
                        throw "Invalid length-delimited field"
                    }
                    $value = [byte[]]::new($length)
                    [Array]::Copy($bytes, $offset, $value, 0, $length)
                    $offset += $length
                    if ($length -eq 64) {
                        $id = Convert-Id $value
                        if ($field -eq 1) { $view = $id }
                        if ($field -eq 2) { $parents.Add($id) }
                    }
                }
                5 { $offset += 4 }
                default { throw "Unsupported protobuf wire type $wire" }
            }
            if ($offset -gt $bytes.Length) { throw "Truncated protobuf field" }
        }
        return [PSCustomObject]@{ View = $view; Parents = @($parents); Error = $null }
    } catch {
        return [PSCustomObject]@{ View = $view; Parents = @($parents); Error = $_.Exception.Message }
    }
}

if (-not (Test-Path -LiteralPath $jj)) {
    throw "No .jj directory exists under $repo"
}

Write-Output "Repository: $repo"
Write-Output "Git status:"
& git --no-optional-locks -C $repo status --short --branch
Write-Output "Git HEAD:"
& git --no-optional-locks -C $repo log -n 3 --format='%H%x09%s' HEAD

$checkoutId = $null
if (Test-Path -LiteralPath $checkout) {
    $checkoutBytes = [System.IO.File]::ReadAllBytes($checkout)
    if ($checkoutBytes.Length -ge 66 -and $checkoutBytes[0] -eq 0x12 -and $checkoutBytes[1] -eq 0x40) {
        $checkoutId = Convert-Id $checkoutBytes[2..65]
    }
}
Write-Output "Checkout operation: $checkoutId"

if (-not (Test-Path -LiteralPath $heads)) {
    throw "Jujutsu operation-head directory is absent"
}

$headIds = @(Get-ChildItem -LiteralPath $heads -File | ForEach-Object Name | Sort-Object)
if ($headIds.Count -eq 0) {
    Write-Output "Active operation heads: none"
    exit 0
}

foreach ($headId in $headIds) {
    $operation = Read-Operation $headId
    Write-Output "Active head: $headId"
    Write-Output "  View: $($operation.View)"
    foreach ($parent in $operation.Parents) {
        Write-Output "  Parent: $parent"
    }
    if ($operation.Error) {
        Write-Output "  Parse error: $($operation.Error)"
    }
}
