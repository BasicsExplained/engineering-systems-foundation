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


def checkpoint_label(folder_name: str) -> str:
    return folder_name.replace('-', ' ').title()


def checkpoint_number_from_path(md: Path):
    parts = md.parts
    for part in parts:
        match = re.match(r'checkpoint-(\d{2})-', part)
        if match:
            return int(match.group(1))
    return None


def checkpoint_navigation_html(md: Path, checkpoints: list[tuple[int, str]]) -> str:
    number = checkpoint_number_from_path(md)
    if number is None:
        return ''

    checkpoint_map = {n: name for n, name in checkpoints}
    prev_number = number - 1
    next_number = number + 1

    items = ['<div class="checkpoint-nav" aria-label="Checkpoint navigation">']

    if prev_number in checkpoint_map and prev_number <= UNLOCKED_UNTIL:
        prev_name = checkpoint_map[prev_number]
        items.append(f'<a class="checkpoint-link" href="../{prev_name}/README.html">← Previous: Checkpoint {prev_number:02d}</a>')
    else:
        items.append('<span class="checkpoint-link disabled">← Previous checkpoint</span>')

    items.append('<a class="checkpoint-link" href="../README.html">Unlocked list</a>')

    if next_number in checkpoint_map and next_number <= UNLOCKED_UNTIL:
        next_name = checkpoint_map[next_number]
        items.append(f'<a class="checkpoint-link" href="../{next_name}/README.html">Next: Checkpoint {next_number:02d} →</a>')
    elif next_number in checkpoint_map:
        items.append(f'<span class="checkpoint-link disabled" title="This checkpoint is locked until mentor approval">Next locked: Checkpoint {next_number:02d} →</span>')
    else:
        items.append('<span class="checkpoint-link disabled">No next checkpoint</span>')

    items.append('</div>')
    return '\n'.join(items)


def page(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ --ink:#172033; --muted:#5f6b7a; --line:#dfe5ee; --soft:#f7f9fc; --brand:#1f4fd8; --brand-soft:#eaf0ff; --task:#fff8e7; --example:#eef7ff; --submit:#ecfdf3; --review:#f5efff; }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 980px; margin: 0 auto; padding: 22px 18px 56px; line-height: 1.65; color: var(--ink); background: #ffffff; }}
    nav {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 0 0 24px; padding: 10px; border: 1px solid var(--line); border-radius: 16px; background: var(--soft); position: sticky; top: 8px; z-index: 5; }}
    nav a {{ display: inline-block; text-decoration: none; color: var(--brand); background: #fff; border: 1px solid var(--line); border-radius: 999px; padding: 8px 12px; font-weight: 700; }}
    nav a:hover {{ background: var(--brand-soft); }}
    .checkpoint-nav {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin: 20px 0 24px; padding: 12px; border: 1px solid var(--line); border-radius: 16px; background: var(--soft); }}
    .checkpoint-link {{ display: block; text-align: center; text-decoration: none; font-weight: 800; border: 1px solid var(--line); border-radius: 12px; padding: 11px 12px; background: #fff; color: var(--brand); }}
    .checkpoint-link:hover {{ background: var(--brand-soft); }}
    .checkpoint-link.disabled {{ color: #8a94a6; background: #eef1f5; cursor: not-allowed; pointer-events: none; }}
    h1 {{ font-size: clamp(2rem, 6vw, 3.4rem); letter-spacing: -0.04em; margin: 18px 0 8px; line-height: 1.08; }}
    h2 {{ font-size: clamp(1.25rem, 3.4vw, 1.8rem); margin: 24px 0 10px; padding: 14px 16px; border-radius: 16px; border: 1px solid var(--line); background: var(--soft); letter-spacing: -0.02em; }}
    h2:nth-of-type(1) {{ background: var(--task); }}
    h2:has(+ ol), h2:has(+ ul) {{ background: var(--task); }}
    h3 {{ margin-top: 22px; }}
    p {{ color: #263244; }}
    a {{ color: var(--brand); }}
    ul, ol {{ background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 14px 22px 14px 34px; margin: 10px 0 18px; }}
    li {{ margin: 7px 0; }}
    code {{ background: #eef2f7; padding: 2px 5px; border-radius: 6px; }}
    pre {{ background: #111827; color: #f8fafc; padding: 15px; overflow-x: auto; white-space: pre-wrap; overflow-wrap: anywhere; border-radius: 14px; border: 1px solid #0f172a; }}
    pre code {{ background: transparent; color: inherit; padding: 0; }}
    table {{ border-collapse: collapse; width: 100%; display: block; overflow-x: auto; margin: 12px 0 20px; }}
    td, th {{ border: 1px solid var(--line); padding: 10px; vertical-align: top; }}
    tr:first-child td {{ font-weight: 800; background: var(--soft); }}
    strong {{ font-weight: 800; }}
    @media (max-width: 640px) {{
      body {{ padding: 14px 12px 44px; }}
      nav {{ position: static; gap: 8px; padding: 9px; }}
      nav a {{ flex: 1 1 calc(50% - 8px); text-align: center; padding: 9px 8px; font-size: 0.92rem; }}
      .checkpoint-nav {{ grid-template-columns: 1fr; }}
      ul, ol {{ padding-left: 28px; }}
      h2 {{ padding: 12px 14px; }}
    }}
  </style>
</head>
<body>
<nav><a href="/engineering-systems-foundation/">Home</a><a href="/engineering-systems-foundation/unlocked/README.html">Start</a><a href="/engineering-systems-foundation/COURSE_STATUS.html">Status</a><a href="/engineering-systems-foundation/ROADMAP.html">Roadmap</a></nav>
<main>
{body}
</main>
</body>
</html>'''


def convert_all_md(root: Path, checkpoints: list[tuple[int, str]]):
    for md in list(root.rglob('*.md')):
        rel_title = md.stem.replace('-', ' ').title()
        body = markdown_to_html(md.read_text(encoding='utf-8'))
        checkpoint_nav = checkpoint_navigation_html(md, checkpoints)
        if checkpoint_nav:
            body = checkpoint_nav + '\n' + body + '\n' + checkpoint_nav
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

nav = [
    '# Start Here',
    '',
    'Do not browse randomly. Open the checkpoints below in order.',
    '',
    '## Instruction',
    '',
    '1. Open the first checkpoint listed below.',
    '2. Finish its **Instruction** section.',
    '3. Use **Example** only for understanding. Do not copy it.',
    '4. Complete **Submit** and send evidence to the mentor.',
    '5. Stop until the mentor unlocks the next checkpoint.',
    '',
    '## Unlocked checkpoints',
    '',
]
for number, name in all_checkpoints:
    if number <= UNLOCKED_UNTIL:
        clean = checkpoint_label(name)
        nav.append(f'- [Checkpoint {number:02d}: {clean}](./{name}/README.md)')
nav.append('')
nav.append('## Stop rule')
nav.append('')
nav.append('If a checkpoint is not listed here, it is not part of your current work.')
(unlocked_dir / 'README.md').write_text('\n'.join(nav), encoding='utf-8')

convert_all_md(OUT, all_checkpoints)

print(f'Built public site: {OUT}')
print(f'Unlocked until checkpoint {UNLOCKED_UNTIL:02d}')
