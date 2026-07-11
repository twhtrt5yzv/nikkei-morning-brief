#!/usr/bin/env python3
"""Claudeが生成したHTML断片を検証して digest.json に格納する。"""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
SRC = Path(__file__).parent / "digest_body.html.tmp"
OUT = Path(__file__).parent / "digest.json"

body = SRC.read_text(encoding="utf-8").strip()

# 万一コードフェンスが付いていたら除去
body = re.sub(r"^```[a-z]*\s*", "", body)
body = re.sub(r"\s*```$", "", body)

# 検証: セクション見出しがあり、危険なタグを含まないこと
if "<h3" not in body or len(body) < 800:
    print("[error] ダイジェストが不完全（h3なし or 短すぎ）", file=sys.stderr)
    sys.exit(1)
for bad in ("<script", "<iframe", "javascript:", "onerror=", "onclick="):
    if bad in body.lower():
        print(f"[error] 禁止タグ/属性を検出: {bad}", file=sys.stderr)
        sys.exit(1)

OUT.write_text(
    json.dumps(
        {"generated": datetime.now(JST).isoformat(timespec="seconds"), "html": body},
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
print(f"digest.json 更新完了（{len(body)}文字）")
