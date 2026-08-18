# SignPath Foundation導入手順

この文書は、SignPath Foundationの審査通過後にVJ Controller Proのリリース署名を有効化する手順です。

## 1. SignPath Foundationへ申請する

[SignPath Foundationの申請ページ](https://signpath.org/apply.html)から、次の情報を使って申請します。

- Project: `VJ Controller Pro`
- Repository: `https://github.com/ariki41/vj-controller-pro`
- Releases: `https://github.com/ariki41/vj-controller-pro/releases`
- License: MIT
- Artifact: Windows x64 executable (`vj-controller-pro.exe`)
- Code signing policy: `https://github.com/ariki41/vj-controller-pro/blob/main/CODE_SIGNING_POLICY.md`
- Privacy policy: `https://github.com/ariki41/vj-controller-pro/blob/main/PRIVACY.md`

審査、規約への同意、SignPathアカウントの作成は、リポジトリ所有者本人が行います。

## 2. SignPathプロジェクトを設定する

審査通過後、SignPathの案内に従って次を設定します。

1. SignPath GitHub Appをインストールし、このリポジトリへのアクセスを許可します。
2. SignPath Projectを作成し、Repository URLをこのリポジトリへ設定します。
3. Trusted Build Systemとして`GitHub.com`を追加し、Projectへ関連付けます。
4. `vj-controller-pro.exe`のサンプルを使い、Windows PE/Authenticode用のArtifact Configurationを作成して既定値にします。
5. リリース用Signing Policyを作成し、署名要求に手動承認を必須とします。
6. GitHub Actionsから署名要求を送信するユーザーとAPI tokenを作成します。

Open Source Code Signingでは、署名要求までの全ジョブをGitHub-hosted runnerで実行し、GitHub Actions artifactをSignPathへ渡します。現在のRelease workflowはこの構成に対応しています。

## 3. GitHubの変数とSecretを登録する

GitHubリポジトリの`Settings > Secrets and variables > Actions`で、次を登録します。

### Secret

- `SIGNPATH_API_TOKEN`: SignPathで作成したAPI token

### Variables

- `SIGNPATH_ORGANIZATION_ID`: SignPath organization ID
- `SIGNPATH_PROJECT_SLUG`: SignPath project slug
- `SIGNPATH_SIGNING_POLICY_SLUG`: リリース用Signing Policy slug

値が1つでも未設定の場合、Release workflowは未署名ファイルを公開せずに停止します。

## 4. 新しいリリースで確認する

既存タグは再利用せず、`VERSION`と`CHANGELOG.md`を新しいPATCHバージョンへ更新してからタグを作成します。

Release workflowは次を順番に実行します。

1. PyInstallerで製品情報付きのexeをビルド
2. 未署名exeを短期保存のGitHub Actions artifactへアップロード
3. SignPathへ署名要求を送信
4. SignPath上でApproverが手動承認
5. Authenticode署名とアプリのバージョンを検証
6. 署名済みexeだけをGitHub Releaseへ公開

Windowsで公開ファイルを右クリックし、`プロパティ > デジタル署名`に有効なSignPath Foundationの署名が表示されることを最終確認します。
