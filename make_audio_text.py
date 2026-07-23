#!/usr/bin/env python3
"""digest.json を音声読み上げ用のプレーン文に変換して標準出力へ。

画面表示用テキストと違い、聴いて分かりやすいよう記号・URL・テーブル区切りを除去し、
文の区切りに句点・改行を補う。
"""
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).parent


class Speechify(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.buf = []

    def flush(self):
        t = "".join(self.buf).strip()
        if t:
            self.lines.append(t)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h3", "h4", "p", "li", "tr", "br"):
            self.flush()

    def handle_endtag(self, tag):
        if tag in ("h3", "h4", "p", "li", "tr", "td", "th", "ul", "section"):
            self.flush()

    def handle_data(self, data):
        self.buf.append(data)


def clean(text):
    # 記号・URL・番号を読み上げ向けに整える
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("・", "")
    text = text.replace("▼", "")
    text = re.sub(r"^\d+\.\s*", "", text)  # 「1. 見出し」の番号を除去
    text = text.replace("P/L", "損益").replace("B/S", "貸借対照表")
    text = text.replace("→", "、その結果、")
    text = re.sub(r"\s+", " ", text).strip()
    return text


d = json.loads((BASE / "digest.json").read_text(encoding="utf-8"))
gen = datetime.fromisoformat(d["generated"])

p = Speechify()
p.feed(d["html"])
p.flush()

out = [f"日経モーニングブリーフ。{gen.month}月{gen.day}日の朝の経済ダイジェストです。"]
for line in p.lines:
    c = clean(line)
    if not c or c.endswith("作成") or "作成" in c[-4:]:
        continue
    # 見出し末尾に句点がなければ足す（間を作る）
    if not c.endswith(("。", "、", "！", "？")):
        c += "。"
    out.append(c)
out.append("以上、本日の日経モーニングブリーフでした。")

print("\n".join(out))
