import os
import requests
from dotenv import load_dotenv

load_dotenv()

KINTONE_SUBDOMAIN = os.getenv('KINTONE_SUBDOMAIN')
KINTONE_API_TOKEN = os.getenv('KINTONE_API_TOKEN')
KINTONE_USERNAME = os.getenv('KINTONE_USERNAME')
KINTONE_PASSWORD = os.getenv('KINTONE_PASSWORD')

def _get_kintone_headers():
    headers = {'Content-Type': 'application/json'}
    if KINTONE_API_TOKEN:
        headers['X-Cybozu-API-Token'] = KINTONE_API_TOKEN
    return headers

def _get_kintone_auth():
    if KINTONE_USERNAME and KINTONE_PASSWORD:
        return (KINTONE_USERNAME, KINTONE_PASSWORD)
    return None

def kintone_request(method, path, json=None):
    if not KINTONE_SUBDOMAIN:
        raise ValueError("KINTONE_SUBDOMAIN is not set in environment variables.")

    url = f"https://{KINTONE_SUBDOMAIN}.{KINTONE_DOMAIN}{path}"
    print(f"DEBUG: Kintone API URL: {url}")
    headers = _get_kintone_headers(method)
    auth = _get_kintone_auth()

    try:
        response = requests.request(method, url, headers=headers, json=json, auth=auth)
        response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
        return response.json()
    except requests.exceptions.HTTPError as e:
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
