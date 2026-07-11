#!/usr/bin/env python3
"""生成された1枚もの資料（提案プレゼン・メカニズム図解）を検証して shiryo.json に格納する。

どちらかのtmpが欠けている場合は、既存のshiryo.jsonの該当資料を維持する。
"""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
BASE = Path(__file__).parent
OUT = BASE / "shiryo.json"

SOURCES = {
    "presentation": BASE / "shiryo_presentation.html.tmp",
    "mechanism": BASE / "shiryo_mechanism.html.tmp",
}


def clean(body: str) -> str | None:
    body = body.strip()
    body = re.sub(r"^```[a-z]*\s*", "", body)
    body = re.sub(r"\s*```$", "", body)
    if '<div class="sheet"' not in body or len(body) < 400:
        return None
    for bad in ("<script", "<iframe", "javascript:", "onerror=", "onclick=", "style="):
        if bad in body.lower():
            return None
    return body


existing = {}
if OUT.exists():
    try:
        existing = json.loads(OUT.read_text(encoding="utf-8"))
    except Exception:
        existing = {}

result = {"generated": datetime.now(JST).isoformat(timespec="seconds")}
ok = 0
for key, src in SOURCES.items():
    body = clean(src.read_text(encoding="utf-8")) if src.exists() else None
    if body:
        result[key] = body
        ok += 1
        print(f"[ok] {key}: {len(body)}文字")
    elif existing.get(key):
        result[key] = existing[key]
        print(f"[warn] {key}: 生成なし/検証NG → 前回分を維持")
    else:
        print(f"[warn] {key}: 生成なし・前回分もなし")

if ok == 0 and not existing:
    print("[error] 有効な資料がひとつもありません", file=sys.stderr)
    sys.exit(1)

OUT.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
print("shiryo.json 更新完了")
