import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

KINTONE_SUBDOMAIN = os.getenv('KINTONE_SUBDOMAIN')
KINTONE_API_TOKEN = os.getenv('KINTONE_API_TOKEN')
KINTONE_USERNAME = os.getenv('KINTONE_USERNAME')
KINTONE_PASSWORD = os.getenv('KINTONE_PASSWORD')
KINTONE_DOMAIN = os.getenv('KINTONE_DOMAIN', 'cybozu.com')

def _get_kintone_headers(method):
    headers = {}
    if method not in ['GET', 'DELETE']:
        headers['Content-Type'] = 'application/json'
    if KINTONE_USERNAME and KINTONE_PASSWORD:
        # パスワード認証
        headers['X-Cybozu-Authorization'] = base64.b64encode(
            f"{KINTONE_USERNAME}:{KINTONE_PASSWORD}".encode()
        ).decode()
    elif KINTONE_API_TOKEN:
        # APIトークン認証
        headers['X-Cybozu-API-Token'] = KINTONE_API_TOKEN
    return headers

def kintone_request(method, path, json=None):
    if not KINTONE_SUBDOMAIN:
        raise ValueError("KINTONE_SUBDOMAIN is not set in environment variables.")

    url = f"https://{KINTONE_SUBDOMAIN}.{KINTONE_DOMAIN}{path}"
    print(f"DEBUG: Kintone API URL: {url}")
    headers = _get_kintone_headers(method)

    try:
        if method in ['GET', 'DELETE']:
            response = requests.request(method, url, headers=headers, timeout=30)
        else:
            response = requests.request(method, url, headers=headers, json=json, timeout=30)
        response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
        return response.json()
    except requests.exceptions.HTTPError as e:
        print("==== DEBUG INFO ====")
        print("URL:", url)
        print("Headers:", headers)
        print("Status:", e.response.status_code)
        print("Body:", e.response.text)
        print("====================")
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        raise
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        raise
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        raise
