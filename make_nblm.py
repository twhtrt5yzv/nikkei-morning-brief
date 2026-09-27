#!/usr/bin/env python3
"""digest.json を NotebookLM に貼り付けやすいプレーンテキスト（brief.txt）にする。

メール用（make_mail_text.py）と違い、リンクや定型の挨拶を入れず、
音声化したい本文だけを出力する。
"""
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).parent
WEEKDAYS = "月火水木金土日"


class TextExtractor(HTMLParser):
    """ダイジェストのHTML断片を、読み上げやすい素のテキストに変換する。"""

    def __init__(self):
        super().__init__()
        self.lines = []
        self.buf = []
        self.row = []
        # ポンチ絵のコード（pre）と改善ポイント等（section.meta）は音声化しない
        self.skip = 0

    def flush(self):
        text = "".join(self.buf).strip()
        if text:
            self.lines.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag in ("section", "pre"):
                self.skip += 1
            return
        classes = (dict(attrs).get("class") or "").split()
        if tag == "pre" or (tag == "section" and "meta" in classes):
            self.flush()
            self.skip = 1
            return
        if tag in ("h3", "h4"):
            self.flush()
            self.lines.append("")
        elif tag == "li":
            self.flush()
            self.buf.append("・")
        elif tag == "p":
            self.flush()
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.buf = []
        elif tag == "br":
            self.buf.append("\n")

    def handle_endtag(self, tag):
        if self.skip:
            if tag in ("section", "pre"):
                self.skip -= 1
            return
        if tag in ("h3", "h4", "li", "p", "ul", "section"):
            self.flush()
        elif tag in ("td", "th"):
            self.row.append("".join(self.buf).strip())
            self.buf = []
        elif tag == "tr":
            if self.row:
                # 表は「項目：値」の読み上げやすい形に
                self.lines.append("、".join(c for c in self.row if c))
            self.row = []

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)


def html_to_text(html: str) -> str:
    p = TextExtractor()
    p.feed(html)
    p.flush()
    out = []
    for line in p.lines:
        if line == "" and (not out or out[-1] == ""):
            continue
        out.append(line)
    return "\n".join(out).strip()


d = json.loads((BASE / "digest.json").read_text(encoding="utf-8"))
gen = datetime.fromisoformat(d["generated"])
body = html_to_text(d["html"])
# 先頭に入る「〇年〇月〇日（曜）作成」は見出しと重複するので落とす
body = re.sub(r"^\d{4}年\d{1,2}月\d{1,2}日（.）作成[^\n]*\n+", "", body)

header = f"日経モーニングブリーフ　{gen.year}年{gen.month}月{gen.day}日（{WEEKDAYS[gen.weekday()]}）"
text = f"""{header}

生命保険会社の法人営業（支社チーム）向けに、今朝の日経新聞朝刊をもとにした「経営者との対話ネタ・営業トーク（6本）」です。
経営者との関係づくりを第一に、資産分散・手元流動性・事業承継などの提案へ自然につなげる観点でまとめています。

{body}
"""

out = BASE / "brief.txt"
out.write_text(text, encoding="utf-8")
print(f"brief.txt 生成完了（{len(text)}文字）")
