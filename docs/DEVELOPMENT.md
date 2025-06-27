# 開発環境セットアップガイド

本プロジェクトの開発環境をセットアップするための手順を説明します。

## 1. 前提条件

*   Python 3.9+ がインストールされていること。
*   `pip` および `venv` が利用可能であること。
*   Git がインストールされていること。
*   GitHub CLI (`gh`) がインストールされ、認証済みであること。

## 2. リポジトリのクローン

まず、本プロジェクトのリポジトリをクローンします。

```bash
git clone https://github.com/proconlife/py-kintone-mcp.git
cd py-kintone-mcp
```

## 3. 仮想環境のセットアップ

プロジェクトの依存関係を管理するために、仮想環境を使用することを強く推奨します。

### 3.1. 仮想環境の作成

```bash
python3 -m venv venv
```

### 3.2. 仮想環境の有効化

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```bash
venc\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
venc\Scripts\Activate.ps1
```

## 4. 依存関係のインストール

仮想環境を有効化した後、必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

## 5. 環境変数の設定

kintoneへの接続情報など、機密性の高い情報は環境変数で管理します。

プロジェクトルートに `.env` ファイルを作成し、以下の形式で記述してください。

```
KINTONE_SUBDOMAIN=your_subdomain
KINTONE_API_TOKEN=your_api_token
# または
# KINTONE_USERNAME=your_username
# KINTONE_PASSWORD=your_password
```

*   `your_subdomain`: kintoneのサブドメイン（例: `example` なら `example.kintone.com`）
*   `your_api_token`: kintone APIトークン（アプリごとに発行可能）
*   `your_username`, `your_password`: ユーザー名とパスワードで認証する場合

**注意:** `.env` ファイルはGit管理から除外されています（`.gitignore` に記載済み）ので、コミットされないように注意してください。

## 6. 開発サーバーの起動

（MCPサーバーの実装後に追記予定）

## 7. テストの実行

（テストコードの実装後に追記予定）
