#!/usr/bin/env python3
"""GoogleニュースRSS経由で日経記事を取得し data.json を生成する。

GitHub Actions から毎朝実行される想定。標準ライブラリのみ使用。
"""
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
MAX_PER_CAT = 8

CATEGORIES = [
    {"id": "top",   "label": "本日のトップ",   "emoji": "🗞",  "query": "site:nikkei.com when:1d"},
    {"id": "stock", "label": "株価",           "emoji": "📈", "query": "site:nikkei.com (株価 OR 日経平均 OR 株式市場) when:2d"},
    {"id": "fx",    "label": "為替",           "emoji": "💱", "query": "site:nikkei.com (円相場 OR 為替 OR 円安 OR 円高) when:2d"},
    {"id": "rate",  "label": "金利",           "emoji": "🏦", "query": "site:nikkei.com (金利 OR 国債 OR 日銀) when:2d"},
    {"id": "fcy",   "label": "外貨・ドル建て", "emoji": "💵", "query": "site:nikkei.com (外貨 OR ドル建て OR 米国債 OR 米金利) when:3d"},
    {"id": "yen",   "label": "円建て・保険",   "emoji": "🛡",  "query": "(円建て OR 外貨建て保険 OR 生命保険 OR 終身保険) when:7d"},
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

# 記事として意味のない見出しを除外
EXCLUDE_PATTERNS = ["印刷画面", "人事、", "訃報"]


def fetch_feed(query: str) -> list[dict]:
    url = (
        "https://news.google.com/rss/search?q="
        + urllib.parse.quote(query)
        + "&hl=ja&gl=JP&ceid=JP:ja"
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as res:
        xml_text = res.read().decode("utf-8", errors="replace")
    root = ET.fromstring(xml_text)
    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        source = (it.findtext("source") or "").strip()
        # タイトル末尾の「 - 媒体名」を除去
        m = re.match(r"^(.*)\s[-–]\s([^-–]+)$", title)
        if m:
            title = m.group(1).strip()
            if not source:
                source = m.group(2).strip()
        pub = it.findtext("pubDate") or ""
        try:
            dt = datetime.strptime(pub, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
            date_iso = dt.astimezone(JST).isoformat()
        except ValueError:
            date_iso = ""
        items.append(
            {
                "title": title,
                "source": source,
                "link": (it.findtext("link") or "").strip(),
                "date": date_iso,
            }
        )
    return items


def main() -> None:
    seen_titles: set[str] = set()
    out_categories = []
    for cat in CATEGORIES:
        try:
            items = fetch_feed(cat["query"])
        except Exception as e:  # 1カテゴリの失敗で全体を止めない
            print(f"[warn] {cat['id']}: {e}")
            items = []
        picked = []
        for it in items:
            if not it["title"] or it["title"] in seen_titles:
                continue
            if any(p in it["title"] for p in EXCLUDE_PATTERNS):
                continue
            picked.append(it)
            seen_titles.add(it["title"])
            if len(picked) >= MAX_PER_CAT:
                break
        out_categories.append({**{k: cat[k] for k in ("id", "label", "emoji")}, "items": picked})
        print(f"[ok] {cat['id']}: {len(picked)}件")

    data = {
        "updated": datetime.now(JST).isoformat(timespec="seconds"),
        "categories": out_categories,
    }
    out = Path(__file__).parent / "data.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(len(c["items"]) for c in out_categories)
    print(f"data.json 更新完了: 合計{total}件")


if __name__ == "__main__":
    main()
