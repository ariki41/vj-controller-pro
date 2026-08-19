# Code signing policy

VJ Controller Proの公式Windows実行ファイルは、固定メンバー向けの自己署名Authenticode証明書で署名し、GitHub Releasesで公開します。自己署名証明書はWindowsから標準では信頼されないため、利用者は公式Releaseの公開証明書を自分のWindowsユーザーへ登録する必要があります。

この署名は、実行ファイルがこのリポジトリのRelease workflowで作られ、署名後に変更されていないことを固定メンバー間で確認するためのものです。Microsoftや公開認証局による発行者の本人確認を示すものではありません。

## 対象

- リポジトリ: [ariki41/vj-controller-pro](https://github.com/ariki41/vj-controller-pro)
- 成果物: `vj-controller-pro.exe`
- 配布先: [GitHub Releases](https://github.com/ariki41/vj-controller-pro/releases)
- 対象利用者: 証明書の指紋を別途確認できる固定メンバー

ソースアーカイブ、Pull Requestのテストビルド、`v0.1.2`以前のReleaseは署名対象外です。

## 署名証明書

- Subject: `CN=VJ Controller Pro, O=ariki41`
- SHA-1 thumbprint: `743A44349826D9D8C7367487FBBD81BE74E5C34B`
- SHA-256 fingerprint: `92E30CC0890CBCF62ECEF326AF18C0ECD04C458640EC13DDB677E20DC7E7B01E`
- 有効期間: 2026年8月19日 03:20:12 UTCから2029年8月18日 03:20:12 UTCまで
- 公開証明書: [`certs/vj-controller-pro-code-signing.cer`](certs/vj-controller-pro-code-signing.cer)

証明書を更新する場合は、公開証明書、指紋、信頼登録スクリプト、GitHub Actions Secretsを同じPull Requestとリリース手順で更新し、固定メンバーへ新しい指紋を別経路で通知します。

## チームの役割

- Committers and reviewers: [@ariki41](https://github.com/ariki41)
- Release approvers: [@ariki41](https://github.com/ariki41)

外部コントリビューターによる変更は、署名対象のリリースへ含める前にリポジトリ管理者がレビューします。特にGitHub Actions workflowと署名関連ファイルの変更を確認します。

## 秘密鍵の管理

秘密鍵は暗号化PFXとしてGitHub Actions Secret `WINDOWS_CODE_SIGNING_PFX_BASE64`へ保存し、パスワードは別のSecret `WINDOWS_CODE_SIGNING_PASSWORD`へ保存します。秘密鍵、PFX、パスワードをGitリポジトリ、Release、Actions artifact、ログへ保存しません。

Release workflowはPFXをrunnerの一時ディレクトリにだけ復元し、署名処理の終了時に削除します。GitHub-hosted runner自体もジョブ終了後に破棄されます。

## リリース手順

1. Pull Requestをレビューし、CIが成功した変更だけを`main`へマージします。
2. `main`からRelease workflowを手動実行し、GitHub-hosted Windows runnerで署名処理をドライランします。
3. ドライラン成功後、`VERSION`と一致するタグから同じ手順で実行ファイルをビルドします。
4. PFXの証明書指紋が公開証明書と一致することを検証します。
5. SHA-256とRFC 3161タイムスタンプを使用して実行ファイルへAuthenticode署名します。
6. 署名状態、署名者の指紋、タイムスタンプ、アプリと製品のバージョンを検証します。
7. 検証済みexe、公開証明書、信頼登録スクリプト、SHA-256一覧だけをGitHub Releaseへ添付します。

検証に失敗した場合、workflowはGitHub Releaseを作成しません。

## 利用者による信頼と解除

固定メンバーは[自己署名証明書の利用手順](docs/SELF_SIGNED_CERTIFICATE.md)に従い、公開証明書の指紋を確認してから現在のWindowsユーザーへ登録します。メンバーから外れた場合や利用を終了する場合は、同梱スクリプトの`-Remove`オプションで信頼を解除します。

## セキュリティとプライバシー

公式GitHub Release以外から入手した証明書や実行ファイルを信頼しないでください。秘密鍵の漏えいが疑われる場合は、ただちにReleaseを停止し、証明書とSecretsを交換して固定メンバーへ通知します。

アプリの通信と保存データについては[プライバシーポリシー](PRIVACY.md)を参照してください。署名済み成果物に不審な点がある場合は、公開Issueへ機密情報を書き込まず、GitHubのリポジトリ管理者へ連絡してください。
