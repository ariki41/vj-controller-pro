# 変更履歴

このプロジェクトの主な変更をバージョンごとに記録します。

バージョン番号は[Semantic Versioning](https://semver.org/lang/ja/)に従います。

## [0.1.3] - 2026-08-19

### 追加

- 固定メンバー向けの自己署名Authenticode証明書と信頼登録スクリプト
- MIT License、コード署名ポリシー、プライバシーポリシー
- Windows実行ファイルの製品名と製品バージョン情報

### 変更

- GitHub Actionsで自己署名し、署名・証明書指紋・タイムスタンプを検証した実行ファイルだけをReleaseへ公開
- Releaseへ公開証明書、信頼登録スクリプト、SHA-256チェックサムを同梱

## [0.1.2] - 2026-08-18

### 修正

- Windows実行ファイルへ`control.html`を同梱し、READMEと起動時に案内するURLを統一
- 動画ダウンロード用の実行時ライブラリ`brotli`と`certifi`を追加
- Windows実行ファイルのダウンロード、起動、素材配置、トラブル対応の説明を更新

## [0.1.1] - 2026-08-18

### 変更

- Windows 64-bit向けリリースを単一実行ファイル`vj-controller-pro.exe`に変更
- HTMLとバージョン情報を実行ファイルへ同梱
- 実行ファイルの起動時に、同じフォルダへ`videos`フォルダを自動作成
- `--version`オプションを追加

## [0.1.0] - 2026-08-18

### 追加

- FastAPIによるローカルWebサーバー
- 動画・画像素材のアップロード、一覧取得、配信
- yt-dlpを利用した動画ダウンロードと進捗表示
- VJコントローラー画面とプロジェクター投影画面
- Pull Request、Issue、CODEOWNERSを含む共同開発テンプレート
- Python 3.10／3.13を対象としたCI
- バージョン管理とタグ連動のGitHub Release自動作成

[0.1.3]: https://github.com/ariki41/vj-controller-pro/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/ariki41/vj-controller-pro/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ariki41/vj-controller-pro/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ariki41/vj-controller-pro/releases/tag/v0.1.0
