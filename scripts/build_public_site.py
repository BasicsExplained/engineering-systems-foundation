#!/usr/bin/env python3
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

print(f'Built public site: {OUT}')
print(f'Unlocked until checkpoint {UNLOCKED_UNTIL:02d}')
