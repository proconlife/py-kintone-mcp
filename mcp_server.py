from dotenv import load_dotenv
import os
from mcp.server.fastmcp import FastMCP
from kintone_api import kintone_request, get_app_revision, get_form_fields

# .env ファイルから環境変数を読み込む
load_dotenv()

mcp = FastMCP("Kintone MCP")

@mcp.tool()
def create_kintone_app(app_name: str, form_fields: dict = None, app_permissions: dict = None):
    """
    kintoneアプリを作成します。

    Args:
        app_name (str): 作成するアプリの名前。
        form_fields (dict, optional): アプリのフォーム設定。kintone REST APIのAdd Form Fieldsのrequest body形式。
        app_permissions (dict, optional): アプリのアクセス権限設定。kintone REST APIのUpdate App Permissionsのrequest body形式。

    Returns:
        dict: 作成されたアプリのIDを含む辞書。
    """
    payload = {
        "name": app_name
    }
    try:
        response = kintone_request("POST", "/k/v1/preview/app.json", json=payload)
        app_id = response.get("app")

        if form_fields:
            if not form_fields.get("properties"):
                raise ValueError("form_fields.properties が空です")
            # フォーム設定の更新
            form_payload = {"app": app_id, "properties": form_fields.get("properties", {})}
            kintone_request("PUT", "/k/v1/preview/app/form/fields.json", json=form_payload)

        if app_permissions:
            # アプリ権限の更新
            permission_payload = {"app": app_id, "rights": app_permissions}
            kintone_request("PUT", "/k/v1/preview/app/acl.json", json=permission_payload)

        # アプリの公開
        deploy_payload = {"apps": [{"app": app_id}]}
        kintone_request("POST", "/k/v1/preview/app/deploy.json", json=deploy_payload)

        # デプロイ完了のポーリング
        while True:
            deploy_status = kintone_request("GET", "/k/v1/preview/app/deploy.json", params={"app": app_id})
            if deploy_status["apps"][0]["status"] == "SUCCESS":
                break
            elif deploy_status["apps"][0]["status"] == "FAIL":
                raise Exception("App deployment failed.")
            import time
            time.sleep(5) # 5秒待機

        return {"app_id": app_id}
    except Exception as e:
        print(f"Error creating kintone app: {e}")
        raise

@mcp.tool()
def update_kintone_app(app_id: int, form_fields: dict = None, app_permissions: dict = None):
    """
    kintoneアプリを変更します。

    Args:
        app_id (int): 変更するアプリのID。
        form_fields (dict, optional): アプリのフォーム設定。kintone REST APIのAdd Form Fieldsのrequest body形式。
                                      例: {"properties": {"my_text_field": {"type": "SINGLE_LINE_TEXT", "code": "my_text_field", "label": "My Text Field"}}}
                                      `properties` キーの下にフィールドコードをキーとした辞書を配置してください。
        app_permissions (dict, optional): アプリのアクセス権限設定。kintone REST APIのUpdate App Permissionsのrequest body形式。

    Returns:
        dict: 変更されたアプリのIDを含む辞書。
    """
    try:
        revision = get_app_revision(app_id)
        if form_fields:
            # 現在のフォームフィールド定義を取得
            current_form_fields = get_form_fields(app_id)
            
            # 新しいフィールド定義をマージ
            merged_form_fields = current_form_fields.copy()
            merged_form_fields.update(form_fields.get("properties") or form_fields)

            # フォーム設定の更新
            form_payload = {
                "app": app_id,
                "revision": revision,
                "properties": merged_form_fields
            }
            kintone_request("PUT", "/k/v1/preview/app/form/fields.json", json=form_payload)

        if app_permissions:
            # アプリ権限の更新
            permission_payload = {
                "app": app_id,
                "revision": revision,
                "rights": (app_permissions.get("rights") or app_permissions)
            }
            kintone_request("PUT", "/k/v1/preview/app/acl.json", json=permission_payload)

        # アプリの公開
        deploy_payload = {"apps": [{"app": app_id}]}
        kintone_request("POST", "/k/v1/preview/app/deploy.json", json=deploy_payload)

        # デプロイ完了のポーリング
        while True:
            deploy_status = kintone_request("GET", "/k/v1/preview/app/deploy.json", params={"app": app_id})
            if deploy_status["apps"][0]["status"] == "SUCCESS":
                break
            elif deploy_status["apps"][0]["status"] == "FAIL":
                raise Exception("App deployment failed.")
            import time
            time.sleep(5) # 5秒待機

        return {"app_id": app_id}
    except Exception as e:
        print(f"Error updating kintone app: {e}")
        raise

if __name__ == "__main__":
    # テスト用のapp_idを設定してください
    TEST_APP_ID = 52 # 実際のアプリIDに置き換えてください

    print(f"Testing update_kintone_app for app_id: {TEST_APP_ID}")
    try:
        # 既存のテキストフィールドのラベルを変更する例
        test_form_fields = {"properties": {"foo": {"type": "SINGLE_LINE_TEXT", "code": "foo", "label": "Foo"}}}
        result = update_kintone_app(app_id=TEST_APP_ID, form_fields=test_form_fields)
        print(f"Test successful: {result}")
    except Exception as e:
        print(f"Test failed: {e}")
    # mcp.run()