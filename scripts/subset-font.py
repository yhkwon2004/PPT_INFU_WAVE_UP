#!/usr/bin/env python3
"""index.html · charts/charts.js에 쓰인 글자만 담은 Pretendard 서브셋(fonts/pretendard-pitch.woff2)을 다시 만듭니다.

덱 문구를 고쳐 새 글자가 생기면 실행합니다(없는 글자는 시스템 서체로 보입니다).

  pip install fonttools brotli
  python3 scripts/subset-font.py path/to/PretendardVariable.ttf

PretendardVariable.ttf는 https://github.com/orioncactus/pretendard 릴리스(또는 npm 패키지 pretendard의
dist/public/variable/)에 있습니다.
"""
import os, string, sys
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) != 2:
    sys.exit(__doc__)
src = sys.argv[1]
html = os.path.join(ROOT, 'index.html')
out = os.path.join(ROOT, 'fonts', 'pretendard-pitch.woff2')

text = open(html, encoding='utf-8').read()
charts = os.path.join(ROOT, 'charts', 'charts.js')
if os.path.exists(charts):
    text += open(charts, encoding='utf-8').read()
chars = set(text) | set(string.printable) | set('·—–…“”‘’「」→←↔↓↑×−±①②③※%')
chars = {c for c in chars if c.isprintable() and not c.isspace()} | {' ', ' '}

opts = subset.Options()
opts.flavor = 'woff2'
opts.layout_features = ['*']
opts.name_IDs = ['*']
opts.notdef_outline = True
font = subset.load_font(src, opts)
sub = subset.Subsetter(opts)
sub.populate(unicodes=sorted(ord(c) for c in chars))
sub.subset(font)
os.makedirs(os.path.dirname(out), exist_ok=True)
subset.save_font(font, out, opts)
print(out, len(chars), 'glyphs', os.path.getsize(out) // 1024, 'KB')
