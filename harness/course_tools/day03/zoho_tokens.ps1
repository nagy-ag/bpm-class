# Local adaptation of the supplied nap03 Zoho Colab token scripts.
# Run from the BPA root:
#   powershell -NoProfile -File .\nap03\working\zoho_tokens.ps1
# Later, refresh with:
#   powershell -NoProfile -File .\nap03\working\zoho_tokens.ps1 -Action Refresh
[CmdletBinding()]
param(
    [ValidateSet('Auto', 'Exchange', 'Refresh')]
    [string]$Action = 'Auto',
    [string]$EnvFile = (Join-Path $PSScriptRoot '..\..\..\.env.local')
)

$ErrorActionPreference = 'Stop'
$envPath = [System.IO.Path]::GetFullPath($EnvFile)
if (-not [System.IO.File]::Exists($envPath)) {
    throw 'The .env.local file was not found.'
}
$originalText = [System.IO.File]::ReadAllText($envPath)
$credentials = @{}
foreach ($line in ($originalText -split '\r?\n')) {
    if ($line -match '^\s*([A-Z][A-Z0-9_]*)\s*=(.*)$') {
        $key = $Matches[1]
        if ($credentials.ContainsKey($key)) { throw "Duplicate field: $key" }
        $value = $Matches[2].Trim()
        if ($value.Length -ge 2 -and (
            ($value.StartsWith('"') -and $value.EndsWith('"')) -or
            ($value.StartsWith("'") -and $value.EndsWith("'")))) {
            $value = $value.Substring(1, $value.Length - 2)
        }
        $credentials[$key] = $value
    }
}
if ($Action -eq 'Auto') {
    if (-not [string]::IsNullOrWhiteSpace($credentials['ZOHO_GRANT_CODE'])) { $Action = 'Exchange' }
    elseif (-not [string]::IsNullOrWhiteSpace($credentials['ZOHO_REFRESH_TOKEN'])) { $Action = 'Refresh' }
    else { $Action = 'Exchange' }
}
$requiredKeys = @('ZOHO_CLIENT_ID', 'ZOHO_CLIENT_SECRET')
if ($Action -eq 'Exchange') { $requiredKeys += 'ZOHO_GRANT_CODE' }
else { $requiredKeys += 'ZOHO_REFRESH_TOKEN' }
foreach ($key in $requiredKeys) {
    if ([string]::IsNullOrWhiteSpace($credentials[$key])) {
        throw "Fill $key in .env.local first. For Exchange, generate a fresh Self Client code just before running."
    }
}

$body = @{
    client_id = $credentials['ZOHO_CLIENT_ID']
    client_secret = $credentials['ZOHO_CLIENT_SECRET']
}
if ($Action -eq 'Exchange') {
    $body.grant_type = 'authorization_code'
    $body.code = $credentials['ZOHO_GRANT_CODE']
} else {
    $body.grant_type = 'refresh_token'
    $body.refresh_token = $credentials['ZOHO_REFRESH_TOKEN']
}
try {
    $response = Invoke-RestMethod -Method Post `
        -Uri 'https://accounts.zoho.eu/oauth/v2/token' `
        -ContentType 'application/x-www-form-urlencoded' -Body $body -TimeoutSec 30
} catch {
    # Do not print raw request/response data or exception details with secrets.
    throw 'Zoho token request failed. Check your connection and EU client credentials. No values were saved.'
}
if ([string]::IsNullOrWhiteSpace($response.access_token)) {
    switch ([string]$response.error) {
        'invalid_code' { throw 'Zoho rejected the code/token. For Exchange, generate a new unused grant code; for Refresh, check whether the refresh token was revoked.' }
        'invalid_client' { throw 'Zoho rejected the Client ID/Secret. Check that both belong to this EU Self Client.' }
        'invalid_scope' { throw 'Zoho rejected the scope. Generate a new code with the course scope ZohoCRM.modules.ALL.' }
        default { throw 'Zoho did not return an access token. No values were saved.' }
    }
}
if ($response.api_domain -ne 'https://www.zohoapis.eu') {
    throw 'The token is not for the EU production CRM used by the course. No values were saved.'
}
$updates = @{ ZOHO_ACCESS_TOKEN = [string]$response.access_token }
$validForSeconds = 3600
if ($response.expires_in -and [int]::TryParse([string]$response.expires_in, [ref]$validForSeconds)) {
    $validForSeconds = [Math]::Max(1, $validForSeconds)
}
$updates['ZOHO_ACCESS_TOKEN_EXPIRES_AT'] = [string]([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + $validForSeconds)
if (-not [string]::IsNullOrWhiteSpace($response.refresh_token)) {
    $updates['ZOHO_REFRESH_TOKEN'] = [string]$response.refresh_token
}
if ($Action -eq 'Exchange') { $updates['ZOHO_GRANT_CODE'] = '' }

$updatedText = $originalText
foreach ($key in $updates.Keys) {
    $replacement = $key + '=' + $updates[$key]
    $pattern = '(?m)^[ \t]*' + [regex]::Escape($key) + '=[^\r\n]*'
    if ([regex]::IsMatch($updatedText, $pattern)) {
        $updatedText = [regex]::Replace($updatedText, $pattern,
            [System.Text.RegularExpressions.MatchEvaluator]{ param($match) $replacement })
    } else {
        $updatedText = $updatedText.TrimEnd("`r", "`n") + "`r`n" + $replacement + "`r`n"
    }
}
if ([System.IO.File]::ReadAllText($envPath) -cne $originalText) {
    throw '.env.local changed while the request ran. It was not overwritten. For Exchange, generate a fresh code before retrying.'
}
$tempPath = $envPath + '.tmp'
try {
    [System.IO.File]::WriteAllText($tempPath, $updatedText, [System.Text.UTF8Encoding]::new($false))
    [System.IO.File]::Replace($tempPath, $envPath, [NullString]::Value)
} finally {
    if ([System.IO.File]::Exists($tempPath)) { [System.IO.File]::Delete($tempPath) }
}
Write-Output "Success: $Action saved Zoho tokens in .env.local without displaying their values."
if ($Action -eq 'Exchange' -and [string]::IsNullOrWhiteSpace($response.refresh_token)) {
    Write-Warning 'Zoho returned no refresh token. The access token was saved; check Self Client authorization before you need to refresh.'
}
