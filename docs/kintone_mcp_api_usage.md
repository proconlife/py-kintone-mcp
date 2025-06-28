# Kintone MCP API 利用ガイド

このドキュメントは、Kintone Model Context Protocol (MCP) サーバーが提供するkintone API関連ツールの利用方法と、AIがこれらのツールを効果的に利用するためのガイドラインを提供します。

## はじめに

kintone MCPサーバーは、kintoneアプリの作成や更新を自動化するためのツールを提供します。これらのツールは、kintone REST APIをラップしており、AIがより簡単にkintone操作を行えるように設計されています。

## `create_kintone_app` ツール

新しいkintoneアプリを作成します。

### 目的と引数

- `app_name` (str): 作成するアプリの名前。
- `form_fields` (dict, optional): アプリのフォーム設定。kintone REST APIのAdd Form Fieldsのrequest body形式。
- `app_permissions` (dict, optional): アプリのアクセス権限設定。kintone REST APIのUpdate App Permissionsのrequest body形式。

### `form_fields` の例

`form_fields` は、`properties` キーの下にフィールドコードをキーとした辞書を配置します。

```json
{
  "properties": {
    "my_text_field": {
      "type": "SINGLE_LINE_TEXT",
      "code": "my_text_field",
      "label": "My Text Field"
    },
    "my_number_field": {
      "type": "NUMBER",
      "code": "my_number_field",
      "label": "My Number Field",
      "defaultValue": "0",
      "digit": false,
      "maxValue": "",
      "minValue": "",
      "unit": "",
      "unitPosition": "BEFORE"
    }
  }
}
```

### `app_permissions` の例

`app_permissions` は、`rights` キーの下にアクセス権限設定のリストを配置します。

```json
{
  "rights": [
    {
      "entity": {
        "type": "GROUP",
        "code": "Administrators"
      },
      "appEditable": true,
      "recordViewable": true,
      "recordAddable": true,
      "recordEditable": true,
      "recordDeletable": true,
      "recordImportable": true,
      "recordExportable": true,
      "fieldEditable": true
    }
  ]
}
```

## `update_kintone_app` ツール

既存のkintoneアプリを変更します。

### 目的と引数

- `app_id` (int): 変更するアプリのID。
- `form_fields` (dict, optional): アプリのフォーム設定。`create_kintone_app` と同様の形式です。
- `app_permissions` (dict, optional): アプリのアクセス権限設定。`create_kintone_app` と同様の形式です。

### `form_fields` の例

`create_kintone_app` と同様の形式です。

```json
{
  "properties": {
    "existing_field": {
      "label": "Updated Field Label",
      "type": "SINGLE_LINE_TEXT",
      "code": "existing_field"
    },
    "new_field": {
      "type": "NUMBER",
      "code": "new_field",
      "label": "New Number Field"
    }
  }
}
```

### `app_permissions` の例

`create_kintone_app` と同様の形式です。

```json
{
  "rights": [
    {
      "entity": {
        "type": "USER",
        "code": "user1"
      },
      "recordViewable": true
    }
  ]
}
```

### リビジョン番号の動的取得について

`update_kintone_app` ツールは、内部的にkintone APIから最新のリビジョン番号を自動的に取得して利用します。AIが手動でリビジョン番号を指定する必要はありません。これにより、競合エラーのリスクを軽減し、よりスムーズなアプリ更新を可能にします。
