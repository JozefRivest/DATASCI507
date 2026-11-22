from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

MIC = "https://www.soumu.go.jp/senkyo/senkyo_s/links/senkan/index.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (academic research; DATASCI507)"}


def prefecture_homepages():
    return prefs  # 47 entries, in JIS order, so the index + 1 = pref_code


test = prefecture_homepages()

KEYWORDS = ("衆議院", "総選挙", "選挙公報", "過去の選挙", "選挙結果")
