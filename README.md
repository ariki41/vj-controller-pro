# VJ Controller Pro セットアップ手順

## 1. 必要なもの
- Python 3.10以降
- （Windowsの場合）https://www.python.org/downloads/ からインストールし、
  インストール時に「Add python.exe to PATH」にチェックを入れてください。

## 2. フォルダ構成
```
project_root/
  ├─ main.py
  ├─ requirements.txt
  ├─ videos/             # ダウンロード・アップロードした動画/画像の保存先(空のままでOK)
  └─ public/
      ├─ index.html      # コントローラー画面
      └─ stage.html      # プロジェクター投影用出力画面
```
このフォルダ構成のまま丸ごと展開してください。

## 3. セットアップ(最初の1回だけ)
このフォルダをコマンドプロンプト(またはターミナル)で開き、以下を実行して必要なライブラリをインストールします。

```
pip install -r requirements.txt
```

## 4. 起動方法
同じフォルダで以下を実行します。

```
python main.py
```

「Uvicorn running on http://0.0.0.0:8000」のような表示が出たら起動完了です。
ブラウザで以下のURLを開いてください。

```
http://localhost:8000/static/control.html
```

もしアクセスできない場合は、上記URLの`control.html`の部分を実際のファイル名(`index.html`)に読み替えてみてください。

## 5. 使い方の要点
- 左上の「window (画面投影)」ボタンで投影用ウィンドウが開きます。これをプロジェクター側のディスプレイにドラッグしてフルスクリーン表示してください。
- 素材一覧の「更新」ボタンで、`videos`フォルダに追加した動画/画像ファイルを反映できます。
- 対応ファイル形式: mp4 / webm / mov / m4v / gif / png / jpg / jpeg / webp

## 6. 終了方法
起動したコマンドプロンプト/ターミナルの画面で `Ctrl + C` を押すとサーバーが停止します。

## 7. 開発への参加

ブランチの作成、動作確認、Pull Request、レビューのルールは[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。
