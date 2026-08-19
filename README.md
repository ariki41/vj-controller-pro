# VJ Controller Pro

ブラウザーから動画・画像素材を操作し、別ウィンドウへ投影するVJコントローラーです。

通常利用では、Windows向けの単一実行ファイル`vj-controller-pro.exe`だけを使用します。Pythonのインストールやソースコードの展開は不要です。

## Windows実行ファイルで使う

### 必要なもの

- 64-bit Windows
- Chrome、EdgeなどのWebブラウザー
- 動画をダウンロードする場合はインターネット接続

### ダウンロード

1. [最新のGitHub Release](https://github.com/ariki41/vj-controller-pro/releases/latest)を開きます。
2. `Assets`から次の4ファイルをダウンロードします。
   - `vj-controller-pro.exe`
   - `vj-controller-pro-code-signing.cer`
   - `install-windows-signing-certificate.ps1`
   - `SHA256SUMS.txt`
3. 4ファイルを`ドキュメント\VJControllerPro`など、書き込み可能な同じフォルダへ移動します。
4. 初回のみPowerShellでそのフォルダを開き、公開証明書を現在のWindowsユーザーへ登録します。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-windows-signing-certificate.ps1
```

証明書の登録後、通常利用で起動するファイルは`vj-controller-pro.exe`だけです。GitHubが自動表示する`Source code (zip)`と`Source code (tar.gz)`は開発者向けであり、アプリの実行には使用しません。

### 起動

1. `vj-controller-pro.exe`をダブルクリックします。
2. コンソールに`Uvicorn running on http://0.0.0.0:8000`と表示されるまで待ちます。
3. ブラウザーでコントローラー画面を開きます。

```text
http://localhost:8000/static/control.html
```

起動中はコンソールを閉じないでください。Windows Defenderファイアウォールの確認が表示された場合は、信頼できるプライベートネットワークだけを許可してください。

`v0.1.3`以降の実行ファイルは、固定メンバー向けの自己署名証明書で署名します。自己署名証明書はWindowsから標準では信頼されないため、初回に上記の登録が必要です。証明書の指紋、署名確認、信頼解除については[固定メンバー向け自己署名証明書](docs/SELF_SIGNED_CERTIFICATE.md)を確認してください。

### 素材ファイル

初回起動時に、exeと同じフォルダへ`videos`フォルダが自動作成されます。アップロードまたはダウンロードした動画・画像は、このフォルダに保存されます。

ファイルを直接`videos`へ追加した場合は、コントローラー画面の「更新」ボタンを押してください。

対応形式:

- 動画: mp4 / webm / mov / m4v
- 画像: gif / png / jpg / jpeg / webp

### 投影画面

コントローラー画面左上の「window（画面投影）」ボタンを押します。開いたウィンドウをプロジェクター側のディスプレイへ移動し、フルスクリーン表示してください。

投影画面を直接開く場合は、次のURLを使用します。

```text
http://localhost:8000/static/stage.html
```

### 終了

exeを起動したコンソールで`Ctrl + C`を押します。コンソールを閉じても終了できます。

### バージョン確認

PowerShellでexeのあるフォルダを開き、次を実行します。

```powershell
.\vj-controller-pro.exe --version
```

## トラブルシューティング

### 画面を開けない

- `vj-controller-pro.exe`のコンソールが起動中か確認します。
- URLが`http://localhost:8000/static/control.html`になっているか確認します。
- ポート8000を別のアプリが使用していないか確認します。

### 素材が表示されない

- `videos`フォルダがexeと同じ場所にあるか確認します。
- ファイル形式が対応一覧に含まれているか確認します。
- コントローラー画面の「更新」ボタンを押します。

### ネットワーク利用時の注意

このアプリにはユーザー認証がありません。公共Wi-Fiなど信頼できないネットワークでは使用せず、Windows Defenderファイアウォールではプライベートネットワークだけを許可してください。

## ソースコードから起動する

開発する場合はPython 3.10以降を使用します。

```text
project_root/
  ├─ main.py
  ├─ VERSION
  ├─ requirements.txt
  ├─ videos/
  └─ public/
      ├─ control.html
      └─ stage.html
```

仮想環境を作成し、依存関係をインストールします。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Windows PowerShellで仮想環境を有効化する場合:

```powershell
.venv\Scripts\Activate.ps1
```

起動後は、exe版と同じURLでコントローラー画面を開きます。

## 開発への参加

ブランチの作成、動作確認、Pull Request、レビューのルールは[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## バージョンとリリース

現在のバージョンは[VERSION](VERSION)、変更内容は[CHANGELOG.md](CHANGELOG.md)で管理します。

カスタムRelease assetとして、Windows 64-bit向けの`vj-controller-pro.exe`、公開証明書、信頼登録スクリプト、SHA-256チェックサムを添付します。

## Code signing policy

公式Windows実行ファイルの署名対象、ビルド元、承認者、検証手順は[Code signing policy](CODE_SIGNING_POLICY.md)に記載しています。

この自己署名は固定メンバー向けです。Microsoftや公開認証局による発行者の本人確認を示すものではなく、一般公開配布でSmartScreenの信頼を得る用途には使用しません。

## プライバシー

通信内容とローカルに保存するデータについては[プライバシーポリシー](PRIVACY.md)を参照してください。

## ライセンス

このプロジェクトは[MIT License](LICENSE)で公開しています。
