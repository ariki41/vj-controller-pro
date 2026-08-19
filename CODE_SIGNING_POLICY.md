# Code signing policy

VJ Controller Proの公式Windows実行ファイルは、GitHub Releasesで公開します。コード署名導入後の公式実行ファイルは、GitHub Actionsでこのリポジトリのソースコードからビルドし、SignPathへ送信して署名したものに限定します。

Free code signing provided by [SignPath.io](https://signpath.io/), certificate by [SignPath Foundation](https://signpath.org/).

## 対象

- リポジトリ: [ariki41/vj-controller-pro](https://github.com/ariki41/vj-controller-pro)
- 成果物: `vj-controller-pro.exe`
- 配布先: [GitHub Releases](https://github.com/ariki41/vj-controller-pro/releases)

ソースアーカイブや開発中のビルドは、コード署名の対象外です。

## チームの役割

- Committers and reviewers: [@ariki41](https://github.com/ariki41)
- Approvers: [@ariki41](https://github.com/ariki41)

外部コントリビューターによる変更は、署名対象のリリースへ含める前にリポジトリ管理者がレビューします。署名要求はリリースごとにApproverが手動で承認します。

## 署名手順

1. Pull Requestをレビューし、CIが成功した変更だけを`main`へマージします。
2. `VERSION`と一致するタグから、GitHub-hosted Windows runnerで実行ファイルをビルドします。
3. 未署名の成果物をGitHub Actions artifactとして保存し、SignPathのGitHub連携を通じて署名要求を送信します。
4. ApproverがSignPath上で署名要求を確認して承認します。
5. Authenticode署名と製品バージョンを検証し、検証済みの実行ファイルだけをGitHub Releaseへ添付します。

秘密鍵はSignPathのHSMで管理し、このリポジトリやGitHub Actionsのrunnerには配置しません。SignPath APIトークンなどの認証情報はGitHub Secretsで管理します。

## 現在の状態

SignPath Foundationの審査と連携設定が完了するまで、既存のGitHub Releaseには未署名の実行ファイルが含まれる場合があります。各ファイルの署名状態は、Windowsのファイルプロパティにある「デジタル署名」タブで確認してください。

## セキュリティとプライバシー

アプリの通信と保存データについては[プライバシーポリシー](PRIVACY.md)を参照してください。署名済み成果物に不審な点がある場合は、公開Issueへ機密情報を書き込まず、GitHubのリポジトリ管理者へ連絡してください。
