# 固定メンバー向け自己署名証明書

VJ Controller ProのWindows実行ファイルは、固定メンバーへ配布するための自己署名Authenticode証明書で署名します。Windowsはこの証明書を標準では信頼しないため、利用者ごとに公開証明書の登録が必要です。

## 証明書

- Subject: `CN=VJ Controller Pro, O=ariki41`
- SHA-1 thumbprint: `743A44349826D9D8C7367487FBBD81BE74E5C34B`
- SHA-256 fingerprint: `92E30CC0890CBCF62ECEF326AF18C0ECD04C458640EC13DDB677E20DC7E7B01E`
- 有効期間: 2026年8月19日 03:20:12 UTCから2029年8月18日 03:20:12 UTCまで

公開証明書は[`certs/vj-controller-pro-code-signing.cer`](../certs/vj-controller-pro-code-signing.cer)です。秘密鍵は含まれていません。

## 初回のみ: 証明書を信頼する

1. GitHub Releaseから次の4ファイルを同じフォルダへダウンロードします。
   - `vj-controller-pro.exe`
   - `vj-controller-pro-code-signing.cer`
   - `install-windows-signing-certificate.ps1`
   - `SHA256SUMS.txt`
2. `SHA256SUMS.txt`と各ファイルのSHA-256を照合します。
3. PowerShellでそのフォルダを開き、次を実行します。

SHA-256は次のコマンドで表示できます。`SHA256SUMS.txt`の同じファイル名の値と一致することを確認してください。

```powershell
Get-FileHash .\vj-controller-pro.exe -Algorithm SHA256
Get-FileHash .\vj-controller-pro-code-signing.cer -Algorithm SHA256
Get-FileHash .\install-windows-signing-certificate.ps1 -Algorithm SHA256
```

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-windows-signing-certificate.ps1
```

WindowsからTrusted Root Certification Authoritiesへの追加確認が表示されたら、表示された証明書と上記の指紋が一致することを確認して承認します。証明書は現在のユーザーの`Cert:\CurrentUser\Root`と`Cert:\CurrentUser\TrustedPublisher`へ登録されます。管理者権限や他ユーザーへの登録は行いません。

`Root`への登録により、この証明書で署名されたファイルをWindowsが信頼するようになります。公式GitHub Releaseから入手し、指紋を確認したこの証明書だけを登録してください。

## 署名を確認する

```powershell
$signature = Get-AuthenticodeSignature .\vj-controller-pro.exe
$signature | Format-List Status, StatusMessage
$signature.SignerCertificate | Format-List Subject, Thumbprint, NotAfter
```

`Status`が`Valid`、`Thumbprint`が`743A44349826D9D8C7367487FBBD81BE74E5C34B`であることを確認します。

自己署名証明書はMicrosoftや公開認証局による本人確認を受けた証明書ではありません。公式GitHub Release以外から入手した証明書や実行ファイルを信頼しないでください。

## 信頼を解除する

同じフォルダで次を実行します。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-windows-signing-certificate.ps1 -Remove
```

現在のWindowsユーザーの`Root`と`TrustedPublisher`へ登録した、この指紋の証明書だけを削除します。
