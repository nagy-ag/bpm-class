# No provider credentials are read. Configures native Power Query on a fresh copy.
param([string]$Workbook, [string]$QuotesJson)
$ErrorActionPreference = 'Stop'
$bpaRoot = Split-Path -Parent $PSScriptRoot
if (-not $Workbook) { $Workbook = Join-Path $bpaRoot '.bpa/projects/CMC_auto_refresh/CMC_Auto_Refresh.xlsx' }
if (-not $QuotesJson) { $QuotesJson = Join-Path $bpaRoot '.bpa/projects/CMC_auto_refresh/quotes/quotes.json' }
$resolvedBook = (Resolve-Path -LiteralPath $Workbook).Path
$allowedRoot = [IO.Path]::GetFullPath((Join-Path $bpaRoot '.bpa')) + [IO.Path]::DirectorySeparatorChar
if (-not $resolvedBook.StartsWith($allowedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Only configure a fresh workbook inside .bpa; preserve reference evidence.'
}
$quotePath = [IO.Path]::GetFullPath($QuotesJson)
if (-not $quotePath.StartsWith($allowedRoot, [StringComparison]::OrdinalIgnoreCase)) { throw 'Quotes must be inside .bpa.' }
$excel = $null
$book = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AutomationSecurity = 3
    $book = $excel.Workbooks.Open($resolvedBook, 0, $false)
    if ($book.Queries.Count -lt 1) { throw 'Expected native Power Query in reference workbook.' }
    $changed = 0
    foreach ($query in $book.Queries) {
        $formula = [string]$query.Formula
        if ($formula -match 'File\.Contents\("[^"]*quotes\.json"\)') {
            $query.Formula = [regex]::Replace($formula, 'File\.Contents\("[^"]*quotes\.json"\)',
                { param($match) 'File.Contents("' + $quotePath.Replace('"','""') + '")' })
            $changed++
        }
    }
    if ($changed -lt 1) { throw 'Expected quotes.json source not found; do not guess the query.' }
    $book.Save()
    Write-Host 'Native workbook query source configured. No fetch or refresh performed.'
} finally {
    if ($book) { $book.Close($false); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($book) }
    if ($excel) { $excel.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel) }
}
