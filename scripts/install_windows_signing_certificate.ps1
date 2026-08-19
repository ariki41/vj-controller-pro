[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$CertificatePath = (Join-Path $PSScriptRoot "vj-controller-pro-code-signing.cer"),
    [switch]$Remove
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$expectedThumbprint = "743A44349826D9D8C7367487FBBD81BE74E5C34B"
$storeNames = @("Root", "TrustedPublisher")

if ($Remove) {
    foreach ($storeName in $storeNames) {
        $storePath = "Cert:\CurrentUser\$storeName"
        $installedPath = Join-Path $storePath $expectedThumbprint
        if (Test-Path -LiteralPath $installedPath) {
            if ($PSCmdlet.ShouldProcess($installedPath, "Remove trusted certificate")) {
                Remove-Item -LiteralPath $installedPath -Force
            }
        }
    }

    Write-Output "Removed VJ Controller Pro certificate from the current user's trust stores."
    exit 0
}

$resolvedCertificatePath = (Resolve-Path -LiteralPath $CertificatePath).Path
$certificate = Get-PfxCertificate -FilePath $resolvedCertificatePath
$actualThumbprint = ($certificate.Thumbprint -replace "\s", "").ToUpperInvariant()

if ($actualThumbprint -ne $expectedThumbprint) {
    throw "Certificate thumbprint mismatch. Expected $expectedThumbprint, got $actualThumbprint."
}

if ($certificate.NotAfter.ToUniversalTime() -le [DateTime]::UtcNow) {
    throw "The code-signing certificate expired on $($certificate.NotAfter.ToUniversalTime().ToString('u'))."
}

Write-Warning "This self-signed certificate trusts applications signed by VJ Controller Pro for the current Windows user. Continue only if you received these files from the official GitHub Release."

foreach ($storeName in $storeNames) {
    $storePath = "Cert:\CurrentUser\$storeName"
    $installedPath = Join-Path $storePath $expectedThumbprint
    if (-not (Test-Path -LiteralPath $installedPath)) {
        if ($PSCmdlet.ShouldProcess($storePath, "Import VJ Controller Pro certificate")) {
            & certutil.exe -user -f -addstore $storeName $resolvedCertificatePath | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "certutil.exe could not add the certificate to the current user's $storeName store."
            }
        }
    }
}

Write-Output "Trusted VJ Controller Pro certificate for the current Windows user."
Write-Output "Thumbprint: $expectedThumbprint"
