#!/usr/bin/env python3
import html
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'release-config.json').read_text())
UNLOCKED_UNTIL = int(os.environ.get('UNLOCKED_UNTIL') or CONFIG.get('unlocked_until', 1))
SITE_SOURCE = ROOT / 'site-source'
CHECKPOINTS = ROOT / 'checkpoints'
OUT = ROOT / 'public-site'


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_code = False
    in_ul = False
    in_ol = False
    in_table = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append('</ul>')
            in_ul = False

    def close_ol():
        nonlocal in_ol
        if in_ol:
            out.append('</ol>')
            in_ol = False

    def close_lists():
        close_ul()
        close_ol()

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
            close_lists(); close_table()
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
            close_lists(); close_table()
            continue
        if stripped.startswith('|') and stripped.endswith('|'):
            close_lists()
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if all(set(c) <= set('-: ') for c in cells):
                continue
            if not in_table:
                out.append('<table>')
                in_table = True
            out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
            continue
        close_table()
        ordered = re.match(r'^\d+\.\s+(.*)$', raw)
        if raw.startswith('# '):
            close_lists(); out.append(f'<h1>{inline(raw[2:].strip())}</h1>')
        elif raw.startswith('## '):
            close_lists(); out.append(f'<h2>{inline(raw[3:].strip())}</h2>')
        elif raw.startswith('### '):
            close_lists(); out.append(f'<h3>{inline(raw[4:].strip())}</h3>')
        elif raw.startswith('- '):
            close_ol()
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{inline(raw[2:].strip())}</li>')
        elif ordered:
            close_ul()
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            out.append(f'<li>{inline(ordered.group(1).strip())}</li>')
        else:
            close_lists(); out.append(f'<p>{inline(stripped)}</p>')
    close_lists(); close_table()
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
    :root {{ --ink:#172033; --muted:#5f6b7a; --line:#dfe5ee; --soft:#f6f8fb; --brand:#1f4fd8; --brand-soft:#eaf0ff; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 980px; margin: 0 auto; padding: 24px 18px 56px; line-height: 1.7; color: var(--ink); background: #ffffff; }}
    nav {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 0 0 28px; padding: 12px; border: 1px solid var(--line); border-radius: 16px; background: var(--soft); position: sticky; top: 8px; z-index: 5; }}
    nav a {{ display: inline-block; text-decoration: none; color: var(--brand); background: #fff; border: 1px solid var(--line); border-radius: 999px; padding: 8px 12px; font-weight: 650; }}
    nav a:hover {{ background: var(--brand-soft); }}
    main {{ display: block; }}
    h1 {{ font-size: clamp(2.1rem, 7vw, 4rem); letter-spacing: -0.045em; margin: 22px 0 8px; line-height: 1.05; }}
    h2 {{ font-size: clamp(1.35rem, 4vw, 2rem); margin-top: 34px; padding-top: 22px; border-top: 1px solid var(--line); letter-spacing: -0.025em; }}
    h3 {{ margin-top: 26px; }}
    p {{ color: #263244; }}
    a {{ color: var(--brand); }}
    ul, ol {{ background: var(--soft); border: 1px solid var(--line); border-radius: 16px; padding: 16px 22px 16px 34px; }}
    li {{ margin: 8px 0; }}
    code {{ background: #eef2f7; padding: 2px 5px; border-radius: 6px; }}
    pre {{ background: #111827; color: #f8fafc; padding: 16px; overflow-x: auto; white-space: pre-wrap; overflow-wrap: anywhere; border-radius: 16px; border: 1px solid #0f172a; }}
    pre code {{ background: transparent; color: inherit; padding: 0; }}
    table {{ border-collapse: collapse; width: 100%; display: block; overflow-x: auto; }}
    td, th {{ border: 1px solid var(--line); padding: 10px; }}
    tr:first-child td {{ font-weight: 700; background: var(--soft); }}
    h1 + p {{ font-size: 1.18rem; color: var(--muted); }}
    @media (max-width: 640px) {{
      body {{ padding: 16px 14px 44px; }}
      nav {{ position: static; gap: 8px; padding: 10px; }}
      nav a {{ flex: 1 1 calc(50% - 8px); text-align: center; padding: 9px 8px; font-size: 0.95rem; }}
      ul, ol {{ padding-left: 28px; }}
    }}
  </style>
</head>
<body>
<nav><a href="/engineering-systems-foundation/">Home</a><a href="/engineering-systems-foundation/unlocked/README.html">Start / Unlocked</a><a href="/engineering-systems-foundation/COURSE_STATUS.html">Status</a><a href="/engineering-systems-foundation/ROADMAP.html">Roadmap</a></nav>
<main>
{body}
</main>
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

nav = ['# Start Here: Unlocked Checkpoints', '', 'Only the checkpoints released by the instructor are listed here.', '']
for number, name in all_checkpoints:
    if number <= UNLOCKED_UNTIL:
        clean = name.replace('-', ' ').title()
        nav.append(f'- [Checkpoint {number:02d}: {clean}](./{name}/README.md)')
nav.append('')
nav.append('After finishing the latest unlocked checkpoint, submit your evidence for mentor review before moving forward.')
(unlocked_dir / 'README.md').write_text('\n'.join(nav), encoding='utf-8')

convert_all_md(OUT)

print(f'Built public site: {OUT}')
print(f'Unlocked until checkpoint {UNLOCKED_UNTIL:02d}')
