#!/bin/zsh
# digest.json から音声ファイル brief.m4a を生成する（圧縮済み・スマホ向け）
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
REPO="$HOME/.local/nikkei-morning-brief"
cd "$REPO" || exit 1

python3 make_audio_text.py > audio_text.tmp 2>/dev/null || exit 1
[ -s audio_text.tmp ] || exit 1

# 日本語音声Kyokoで一旦AIFF生成 → AAC 48kbpsモノラルに圧縮
say -v "O-ren" -r 180 -f audio_text.tmp -o brief_raw.aiff 2>/dev/null || { rm -f audio_text.tmp; exit 1; }
afconvert brief_raw.aiff brief.m4a -d aac -f m4af -b 48000 --mix 2>/dev/null || { rm -f audio_text.tmp brief_raw.aiff; exit 1; }
rm -f audio_text.tmp brief_raw.aiff
echo "brief.m4a 生成完了 ($(du -h brief.m4a | cut -f1))"
