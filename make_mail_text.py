#!/usr/bin/env python3
"""digest.json をメール配信用のプレーンテキストに変換して標準出力へ。"""
import json
import re
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path

JST = timezone(timedelta(hours=9))
BASE = Path(__file__).parent
APP_URL = "https://twhtrt5yzv.github.io/nikkei-morning-brief/"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.buf = []
        self.in_table = False
        self.row = []

    def flush(self):
        text = "".join(self.buf).strip()
        if text:
            self.lines.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.flush()
            self.lines.append("")
            self.buf.append("■ ")
        elif tag == "h4":
            self.flush()
            self.buf.append("◇ ")
        elif tag == "li":
            self.flush()
            self.buf.append("・")
        elif tag == "p":
            self.flush()
        elif tag == "table":
            self.flush()
            self.in_table = True
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.buf = []
        elif tag == "br":
            self.buf.append("\n")

    def handle_endtag(self, tag):
        if tag in ("h3", "h4", "li", "p", "ul", "section"):
            self.flush()
        elif tag in ("td", "th"):
            self.row.append("".join(self.buf).strip())
            self.buf = []
        elif tag == "tr":
            if self.row:
                self.lines.append("｜".join(c for c in self.row if c))
            self.row = []
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        self.buf.append(data)


def html_to_text(html):
    p = TextExtractor()
    p.feed(html)
    p.flush()
    # 連続空行を1つに
    out = []
    for line in p.lines:
        if line == "" and (not out or out[-1] == ""):
            continue
        out.append(line)
    return "\n".join(out).strip()


d = json.loads((BASE / "digest.json").read_text(encoding="utf-8"))
body = html_to_text(d["html"])
gen = datetime.fromisoformat(d["generated"])

print(f"""おはようございます。
本日の日経モーニングブリーフをお届けします。（{gen.month}/{gen.day} {gen.hour:02d}:{gen.minute:02d} 自動生成）

{body}

----------------------------------------
🎧 音声で聴く（約16分・通勤中にどうぞ）
{APP_URL}brief.m4a

▼ アプリ（記事一覧・連携文作成）
{APP_URL}

▼ 本日の提案資料（1枚もの）
・提案プレゼン: {APP_URL}shiryo.html?doc=presentation
・メカニズム図解: {APP_URL}shiryo.html?doc=mechanism

※このメールは毎朝自動配信されています（日経モーニングブリーフ）""")
