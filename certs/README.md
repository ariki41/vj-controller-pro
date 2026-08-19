# Windowsコード署名証明書

`vj-controller-pro-code-signing.cer`は、固定メンバー向けReleaseのAuthenticode署名に使用する公開証明書です。公開証明書に秘密鍵は含まれません。

- Subject: `CN=VJ Controller Pro, O=ariki41`
- SHA-1 thumbprint: `743A44349826D9D8C7367487FBBD81BE74E5C34B`
- SHA-256 fingerprint: `92E30CC0890CBCF62ECEF326AF18C0ECD04C458640EC13DDB677E20DC7E7B01E`
- Valid from: 2026-08-19 03:20:12 UTC
- Valid until: 2029-08-18 03:20:12 UTC

秘密鍵、PFX、パスワードはこのディレクトリやGitリポジトリへ保存しないでください。暗号化したPFXとパスワードは、それぞれGitHub Actions Secretsの`WINDOWS_CODE_SIGNING_PFX_BASE64`と`WINDOWS_CODE_SIGNING_PASSWORD`で管理します。
