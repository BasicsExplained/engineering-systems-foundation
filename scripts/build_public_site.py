#!/usr/bin/env python3
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'release-config.json').read_text())
UNLOCKED_UNTIL = int(CONFIG.get('unlocked_until', 1))
SITE_SOURCE = ROOT / 'site-source'
CHECKPOINTS = ROOT / 'checkpoints'
OUT = ROOT / 'public-site'


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_code = False
    in_ul = False
    in_table = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append('</ul>')
            in_ul = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append('</table>')
            in_table = False

    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2).replace(".md", ".html")}">{m.group(1)}</a>', s)
        return s

    for line in lines:
        raw = line.rstrip('\n')
        stripped = raw.strip()
        if stripped.startswith('```'):
            close_ul(); close_table()
            if not in_code:
                out.append('<pre><code>')
                in_code = True
            else:
                out.append('</code></pre>')
                in_code = False
            continue
        if in_code:
            out.append(html.escape(raw))
            continue
        if not stripped:
            close_ul(); close_table()
            continue
        if stripped.startswith('|') and stripped.endswith('|'):
            close_ul()
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if all(set(c) <= set('-: ') for c in cells):
                continue
            if not in_table:
                out.append('<table>')
                in_table = True
            out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
            continue
        close_table()
        if raw.startswith('# '):
            close_ul(); out.append(f'<h1>{inline(raw[2:].strip())}</h1>')
        elif raw.startswith('## '):
            close_ul(); out.append(f'<h2>{inline(raw[3:].strip())}</h2>')
        elif raw.startswith('### '):
            close_ul(); out.append(f'<h3>{inline(raw[4:].strip())}</h3>')
        elif raw.startswith('- '):
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{inline(raw[2:].strip())}</li>')
        else:
            close_ul(); out.append(f'<p>{inline(stripped)}</p>')
    close_ul(); close_table()
    if in_code:
        out.append('</code></pre>')
    return '\n'.join(out)


def page(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 920px; margin: 0 auto; padding: 32px 18px; line-height: 1.6; color: #172033; }}
    nav {{ margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #ddd; }}
    nav a {{ margin-right: 14px; }}
    code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
    pre {{ background: #f4f4f4; padding: 14px; overflow-x: auto; border-radius: 8px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td, th {{ border: 1px solid #ddd; padding: 8px; }}
    h1, h2, h3 {{ line-height: 1.25; }}
  </style>
</head>
<body>
<nav><a href="/engineering-systems-foundation/">Home</a><a href="/engineering-systems-foundation/ROADMAP.html">Roadmap</a><a href="/engineering-systems-foundation/COURSE_STATUS.html">Status</a><a href="/engineering-systems-foundation/unlocked/README.html">Unlocked Checkpoints</a></nav>
{body}
</body>
</html>'''


def convert_all_md(root: Path):
    for md in list(root.rglob('*.md')):
        rel_title = md.stem.replace('-', ' ').title()
        body = markdown_to_html(md.read_text(encoding='utf-8'))
        html_path = md.with_suffix('.html')
        html_path.write_text(page(rel_title, body), encoding='utf-8')
        if md.name == 'index.md':
            (md.parent / 'index.html').write_text(page('Engineering Systems Foundation', body), encoding='utf-8')
        md.unlink()


if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SITE_SOURCE, OUT)

unlocked_dir = OUT / 'unlocked'
unlocked_dir.mkdir(exist_ok=True)

checkpoint_pattern = re.compile(r'checkpoint-(\d{2})-')
all_checkpoints = []
for item in sorted(CHECKPOINTS.iterdir()):
    if not item.is_dir():
        continue
    match = checkpoint_pattern.match(item.name)
    if not match:
        continue
    number = int(match.group(1))
    all_checkpoints.append((number, item.name))
    if number <= UNLOCKED_UNTIL:
        shutil.copytree(item, unlocked_dir / item.name)

status_lines = [
    '# Course Status',
    '',
    f'Unlocked until: **Checkpoint {UNLOCKED_UNTIL:02d}**',
    '',
    '| Checkpoint | Status |',
    '|---|---|',
]
for number, name in all_checkpoints:
    status = 'Released' if number <= UNLOCKED_UNTIL else 'Locked'
    label = name.replace('-', ' ').title()
    status_lines.append(f'| {label} | {status} |')
status_lines.append('')
(OUT / 'COURSE_STATUS.md').write_text('\n'.join(status_lines), encoding='utf-8')

nav = ['# Unlocked Checkpoints', '']
for number, name in all_checkpoints:
    if number <= UNLOCKED_UNTIL:
        nav.append(f'- [Checkpoint {number:02d}: {name}](./{name}/README.md)')
nav.append('')
(unlocked_dir / 'README.md').write_text('\n'.join(nav), encoding='utf-8')

convert_all_md(OUT)

print(f'Built public site: {OUT}')
print(f'Unlocked until checkpoint {UNLOCKED_UNTIL:02d}')
