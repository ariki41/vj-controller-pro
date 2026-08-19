# VJ Controller Proへのコントリビューション

このドキュメントでは、VJ Controller Proを複数人で安全に開発するための共通ルールを定めます。

## 開発を始める前に

1. 作業内容に対応するGitHub Issueを作成し、目的・完了条件・担当者を明確にします。
2. `main`を最新にしてから、Issueごとの作業ブランチを作成します。
3. 仕様や設計に判断が必要な場合は、実装前にIssueで合意します。

```bash
git switch main
git pull --ff-only
git switch -c feature/12-websocket-sync
```

## ブランチ名

`<種類>/<Issue番号>-<短い説明>`の形式を使用します。

- `feature/12-websocket-sync`: 機能追加
- `fix/18-upload-filename`: バグ修正
- `chore/23-add-ci`: 設定や依存関係の変更
- `docs/27-update-setup-guide`: ドキュメント更新
- `hotfix/31-download-failure`: 緊急修正

ブランチは短期間で完了させ、複数の目的を混在させないでください。

## 開発環境

Python 3.10以降を使用します。仮想環境を作成して依存関係をインストールしてください。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShellでは、仮想環境を次のコマンドで有効化します。

```powershell
.venv\Scripts\Activate.ps1
```

## 実装時のルール

- PythonはPEP 8を基本とし、責務の小さい関数に分割します。
- UI変更はコントローラー画面と投影画面の両方への影響を確認します。
- APIの入出力や既存URLを変更する場合は、READMEと関連ドキュメントも更新します。
- `.env`、認証情報、個人情報、ダウンロード・アップロードした動画や画像はコミットしません。
- 自動生成ファイルや目的と無関係な整形を変更に混ぜません。

## コミット

1コミットにつき1つの目的を目安にします。メッセージは変更内容が分かる短い命令形にしてください。

```text
Add WebSocket stage synchronization
Fix unsafe upload filenames
Update Windows setup guide
```

## 変更の確認

Pull Requestを作成する前に、最低限次を実行します。

```bash
python -m compileall -q main.py
python -c "import main"
git diff --check
```

機能を変更した場合は`python main.py`で起動し、関連画面とAPIを手動確認します。テストが追加されている場合は、そのテストもすべて実行してください。

## Pull Request

1. 作業ブランチをGitHubへpushします。
2. 早い段階でDraft Pull Requestを作成します。
3. テンプレートに沿って目的、変更内容、確認方法、画面変更を記載します。
4. CIが成功したらDraftを解除し、レビューを依頼します。
5. 指摘への対応後、すべての会話を解決済みにします。
6. 承認後、Squash mergeで`main`へ統合し、作業ブランチを削除します。

作成者自身による承認だけでマージせず、原則として1人以上の別の開発者による承認を受けてください。

## リリース

バージョン番号にはSemantic Versioningを使用します。

- 互換性のあるバグ修正ではPATCHを上げます（例: `0.1.0`から`0.1.1`）。
- 互換性のある機能追加ではMINORを上げます（例: `0.1.1`から`0.2.0`）。
- 安定版で破壊的変更を行う場合はMAJORを上げます（例: `1.2.0`から`2.0.0`）。

リリース担当者は次の手順で作業します。

1. `release/vX.Y.Z`ブランチで`VERSION`と`CHANGELOG.md`を更新します。
2. Pull RequestのレビューとCI成功を確認して`main`へマージします。
3. 最新の`main`に注釈付きタグを作成し、GitHubへpushします。

```bash
git switch main
git pull --ff-only
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0
```

タグと`VERSION`が一致すると、GitHub ActionsがWindows 64-bit向けの単一実行ファイル`vj-controller-pro.exe`をビルドし、GitHub Releaseとリリースノートを自動作成します。カスタムRelease assetには、この実行ファイル以外を添付しません。公開済みタグの移動や再利用はせず、修正は新しいPATCHバージョンとしてリリースしてください。

## ライセンス

このプロジェクトへのコントリビューションは、リポジトリの[MIT License](LICENSE)に基づいて公開されます。

## レビューの観点

- Issueの完了条件を満たしているか
- 既存機能を壊していないか
- 入力値、ファイル操作、外部URLを安全に扱っているか
- エラー時に状態が不整合にならないか
- 複雑さに対してテストや説明が十分か
