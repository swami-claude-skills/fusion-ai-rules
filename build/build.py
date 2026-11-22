#!/usr/bin/env python3
"""Fusion AI Rules: validate the rule files and build every export.

Usage:
  python3 build/build.py check            # validate only (used on pull requests)
  python3 build/build.py build [OUTDIR]   # validate, then write exports (default: dist/)

Exports match the formats of the Rule Set dashboard's Export Builder:
  md, skill (SKILL.md), txt (full plain text), compact, titles, json
plus one file per target in targets.yaml (each with its own format and options),
and dist/data.json for dashboards, the Fusion add-in and the MCP server.
Requires: PyYAML; jsonschema (optional but used when installed).
"""
import json, re, sys, unicodedata, pathlib, datetime

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRI_ORDER = ['Must', 'Should', 'Nice to have']
ERR, WARN = [], []


def load_yaml(p):
    try:
        return yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as e:
        ERR.append(f'{p.relative_to(ROOT)}: not valid YAML ({e})')
        return None


# ------------------------------------------------------------------ load
meta = load_yaml(ROOT / 'ruleset.yaml')
cats = [c['name'] for c in load_yaml(ROOT / 'categories.yaml')['categories']]
cat_colour = {c['name']: c['colour'] for c in load_yaml(ROOT / 'categories.yaml')['categories']}
tgt = load_yaml(ROOT / 'targets.yaml')
schema = json.loads((ROOT / 'schema/rule.schema.json').read_text())
try:
    import jsonschema
    validator = jsonschema.Draft202012Validator(schema)
except ImportError:
    validator = None
    WARN.append('jsonschema not installed: schema check skipped (pip install jsonschema)')


def load_dir(d):
    out = []
    for p in sorted((ROOT / d).rglob('*.yaml')):
        r = load_yaml(p)
        if r is None:
            continue
        r['_file'] = str(p.relative_to(ROOT))
        out.append(r)
    return out


rules = load_dir('rules')
cands = load_dir('candidates')

# ------------------------------------------------------------------ validate
def check(r, kind):
    f = r['_file']
    if validator:
        for e in validator.iter_errors({k: v for k, v in r.items() if k != '_file'}):
            where = '/'.join(str(x) for x in e.path) or '(top)'
            ERR.append(f'{f}: {where}: {e.message}')
    rid = r.get('id', '')
    if kind == 'rule':
        if not re.fullmatch(r'R\d{2,3}', rid):
            ERR.append(f'{f}: accepted rules need an R## id, got {rid!r}')
        if not pathlib.Path(f).name.startswith(rid + '-'):
            ERR.append(f'{f}: file name must start with its id ({rid}-...)')
        if r.get('category') not in cats:
            ERR.append(f'{f}: category {r.get("category")!r} is not in categories.yaml')
        if r.get('status') == 'Candidate':
            ERR.append(f'{f}: status Candidate belongs in candidates/, not rules/')
    else:
        if not rid.startswith('C-'):
            ERR.append(f'{f}: candidates need a C-YYYY-MM-NN id, got {rid!r}')


for r in rules:
    check(r, 'rule')
for r in cands:
    check(r, 'cand')

ids = [r.get('id') for r in rules]
for dup in {i for i in ids if ids.count(i) > 1}:
    ERR.append(f'duplicate rule id {dup}')
cids = [r.get('id') for r in cands]
for dup in {i for i in cids if cids.count(i) > 1}:
    ERR.append(f'duplicate candidate id {dup}')
known = set(ids)
for r in rules + cands:
    for fld in ('conflicts_with', 'supersedes', 'related'):
        for x in r.get(fld) or []:
            if x not in known:
                ERR.append(f'{r["_file"]}: {fld} names {x}, which is not an accepted rule')
    pid = r.get('proposed_id')
    if pid and pid in known:
        ERR.append(f'{r["_file"]}: proposed_id {pid} is already taken by an accepted rule')
# unresolved conflicts between two ACTIVE accepted rules block the build
active = {r['id']: r for r in rules if r.get('status') != 'Deprecated'}
for r in active.values():
    for x in r.get('conflicts_with') or []:
        if x in active:
            ERR.append(f'{r["_file"]}: unresolved conflict with active rule {x}; reword one, or deprecate/supersede it')
if not re.fullmatch(r'\d+\.\d+\.\d+', str(meta.get('version', ''))):
    ERR.append('ruleset.yaml: version must look like 1.2.3')
for t in tgt['targets']:
    if t['format'] not in ('md', 'skill', 'txt', 'compact', 'titles', 'json'):
        ERR.append(f'targets.yaml: {t["id"]} has unknown format {t["format"]!r}')


def report():
    for w in WARN:
        print('warning:', w)
    for e in ERR:
        print('ERROR:', e)
    print(f'{len(rules)} rules, {len(cands)} candidates, {len(tgt["targets"])} targets, '
          f'version {meta.get("version")}: {"FAILED" if ERR else "OK"} ({len(ERR)} errors, {len(WARN)} warnings)')


# ------------------------------------------------------------------ exports
ASCII = [('[‘’]', "'"), ('[“”]', '"'), ('[–—]', '-'), ('…', '...'), ('·', '-'), ('→', '->'), ('×', 'x'),
         ('³', '3'), ('²', '2'), ('°', ' deg'), ('≥', '>='), ('≤', '<='), (' ', ' ')]


def to_ascii(s):
    for a, b in ASCII:
        s = re.sub(a, b, s)
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', s)


def select(sel_id):
    sel = next(s for s in tgt['selections'] if s['id'] == sel_id)
    out = [r for r in rules if r.get('status') != 'Deprecated']
    if 'priority' in sel:
        out = [r for r in out if r['priority'] in sel['priority']]
    if 'status' in sel:
        out = [r for r in out if r['status'] in sel['status']]
    return out


def render(fmt, rs, label, why=True, ex=True, today=None):
    today = today or datetime.date.today().isoformat()
    total = len([r for r in rules if r.get('status') != 'Deprecated'])
    name, ver = meta['name'], meta['version']
    stamp = f'Version {ver} - exported {today} - {len(rs)} of {total} rules - for {label}'
    PRI = lambda r: r['priority'].upper()
    groups = [(c, [r for r in rs if r['category'] == c]) for c in cats]
    groups = [g for g in groups if g[1]]
    if fmt == 'json':
        return json.dumps({
            'meta': {'name': name, 'version': ver, 'edited': False, 'exported': today, 'preset': label,
                     'count': len(rs), 'of': total, 'intro': meta['intro']},
            'categories': [{'name': c, 'colour': cat_colour[c]} for c, _ in groups],
            'rules': [{'id': r['id'], 'category': r['category'], 'title': r['title'], 'rule': r['rule'],
                       'why': r.get('why', ''), 'good': r.get('good', ''), 'avoid': r.get('avoid', ''),
                       'priority': r['priority'], 'status': r['status'], 'works': r['works']} for r in rs],
        }, indent=2, ensure_ascii=False) + '\n'
    if fmt == 'titles':
        s = f'{name.upper()} (v{ver}, {today}, {len(rs)}/{total})\n{meta["intro_short"]}\n'
        for c, lst in groups:
            s += c.upper() + ': ' + '; '.join(
                f'{r["id"]} {"NICE" if r["priority"] == "Nice to have" else PRI(r)} {r["title"]}' for r in lst) + '\n'
        return to_ascii(s.strip()) + '\n'
    if fmt == 'compact':
        s = f'{name.upper()} ({stamp})\n{meta["intro_short"]}\n'
        for c, lst in groups:
            s += '\n' + c.upper() + '\n'
            for r in lst:
                s += f'{r["id"]} {PRI(r)}: {r["rule"]}' + (f' Why: {r["why"]}' if why and r.get('why') else '') + '\n'
        return to_ascii(s.strip()) + '\n'
    if fmt == 'txt':
        s = f'{name.upper()}\n{stamp}\n\n{meta["intro"]}\n'
        for c, lst in groups:
            s += '\n' + c.upper() + '\n' + '-' * len(c) + '\n'
            for r in lst:
                s += f'{r["id"]} [{PRI(r)}] {r["title"]}. {r["rule"]}\n'
                if why and r.get('why'):
                    s += f'    Why: {r["why"]}\n'
                if ex and r.get('good'):
                    s += f'    Good: {r["good"]}\n'
                if ex and r.get('avoid'):
                    s += f'    Avoid: {r["avoid"]}\n'
        return to_ascii(s)
    s = ''
    if fmt == 'skill':
        s += f'---\nname: fusion-modeling-rules\ndescription: {meta["skill_description"]}\n---\n\n'
    s += f'# {name}\n\n_{stamp}_\n\n{meta["intro"]}\n'
    for c, lst in groups:
        s += f'\n## {c}\n\n'
        for r in lst:
            s += f'- **{r["id"]} [{PRI(r)}] {r["title"]}.** {r["rule"]}\n'
            if why and r.get('why'):
                s += f'  - Why: {r["why"]}\n'
            if ex and r.get('good'):
                s += f'  - Good: {r["good"]}\n'
            if ex and r.get('avoid'):
                s += f'  - Avoid: {r["avoid"]}\n'
    return s


def landing(index, sizes):
    """Interim GitHub Pages page (Phase 1): every export as a direct download.
    Phase 2 replaces it with the full Rule Set dashboard built from data.json."""
    from html import escape as e
    ai_name = {a['key']: a['name'] for a in tgt['ais']}
    main = ''.join(f'<tr><td><a href="{e(rel)}" download>{e(rel)}</a></td><td>{n:,}</td></tr>' for rel, n in sizes[:9])
    rows = ''
    for x in index:
        t = next(t for t in tgt['targets'] if t['id'] == x['target'])
        sel = next(s['label'] for s in tgt['selections'] if s['id'] == x['selection'])
        rows += (f'<tr><td>{e(ai_name.get(t["ai"], "Any AI"))}</td><td>{e(t["label"].split(" · ", 1)[-1])}</td>'
                 f'<td>{e(t.get("where") or "")}</td><td>{e(sel)} ({x["rules"]})</td><td>{x["characters"]:,}'
                 f'{" / " + format(x["limit"], ",") if x["limit"] else ""}</td>'
                 f'<td><a href="{e(x["file"])}" download>{e(t["file"])}</a></td></tr>')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(meta["system"])} v{e(meta["version"])}</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0d0d0f;--panel:#141418;--panel-2:#1a1a20;--cyan:#00e5ff;--text:#e8e8ec;--dim:#9aa0aa;--mute:#6a6f78;--border:#26262e}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 'DM Sans',sans-serif;padding:0 16px 60px}}
header{{text-align:center;padding:36px 0 24px;border-bottom:1px solid var(--border)}}
.k{{font:11px 'JetBrains Mono',monospace;letter-spacing:3px;color:var(--cyan);text-transform:uppercase}}
h1{{font-size:28px;margin:10px 0 6px}}p{{color:var(--dim)}}a{{color:var(--cyan)}}
h2{{font:700 13px 'JetBrains Mono',monospace;letter-spacing:1px;text-transform:uppercase;color:var(--cyan);margin:28px 0 8px}}
.w{{overflow-x:auto;border:1px solid var(--border);border-radius:8px;background:var(--panel)}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}}th,td{{text-align:left;padding:8px 12px;border-bottom:1px solid var(--border);vertical-align:top}}
th{{font:11px 'JetBrains Mono',monospace;letter-spacing:1px;text-transform:uppercase;color:var(--cyan);background:var(--panel-2)}}
td{{color:var(--dim)}}td a{{font-family:'JetBrains Mono',monospace;font-size:12.5px}}
footer{{text-align:center;font:11.5px 'JetBrains Mono',monospace;color:var(--mute);margin-top:30px}}
</style></head><body>
<header><div class="k">AI RULE SET</div><h1>{e(meta["name"])}</h1>
<p>Version <strong>{e(meta["version"])}</strong> · {len(select("all"))} rules · released {e(str(meta.get("released", "")))}</p></header>
<p>Good-practice rules to give an AI before it models in Autodesk Fusion. Download the file for your AI below, then put it where the table says.
Source, history and proposals: <a href="https://github.com/swami-claude-skills/fusion-ai-rules">github.com/swami-claude-skills/fusion-ai-rules</a>.
Rules licensed CC BY 4.0.</p>
<h2>By AI and place</h2><div class="w"><table><thead><tr><th>AI</th><th>Place</th><th>Where it goes</th><th>Rules</th><th>Chars / limit</th><th>Download</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Whole set</h2><div class="w"><table><thead><tr><th>File</th><th>Characters</th></tr></thead><tbody>{main}<tr><td><a href="data.json" download>data.json</a></td><td>everything, for tools</td></tr></tbody></table></div>
<footer>Vibe Coding: Swami · AI: Claude</footer></body></html>
'''


EXT = {'md': 'md', 'skill': 'md', 'txt': 'txt', 'compact': 'txt', 'titles': 'txt', 'json': 'json'}


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    today = meta.get('released') or datetime.date.today().isoformat()
    full = select('all')
    files = {
        'fusion-modeling-rules.md': render('md', full, 'All rules (Markdown)', today=today),
        'fusion-modeling-rules.txt': render('txt', full, 'All rules (plain text)', today=today),
        'fusion-modeling-rules-compact.txt': render('compact', full, 'All rules (compact)', why=False, ex=False, today=today),
        'fusion-modeling-rules-titles.txt': render('titles', full, 'All rules (titles only)', today=today),
        'fusion-modeling-rules.json': render('json', full, 'All rules (JSON)', today=today),
        'skill/fusion-modeling-rules/SKILL.md': render('skill', full, 'Claude skill (SKILL.md)', today=today),
        'AGENTS.md': render('md', full, 'ChatGPT Codex (AGENTS.md)', today=today),
        'GEMINI.md': render('md', full, 'Gemini CLI (GEMINI.md)', today=today),
        'CLAUDE.md': render('md', full, 'Claude Code (CLAUDE.md)', today=today),
    }
    index = []
    for t in tgt['targets']:
        # largest selection that fits the target's limit (All, then Must + Should, then Must only)
        chosen = None
        for sel in ['all', 'must-should', 'must']:
            rs = select(sel)
            label = t['label'] + ('' if sel == 'all' else ' - ' + next(s['label'] for s in tgt['selections'] if s['id'] == sel))
            txt = render(t['format'], rs, label, t.get('include_why', True), t.get('include_examples', True), today=today)
            lim = (t.get('limit') or [None])[0]
            chosen = (sel, rs, txt)
            if not lim or len(txt) <= lim:
                break
        sel, rs, txt = chosen
        lim = (t.get('limit') or [None])[0]
        if lim and len(txt) > lim:
            WARN.append(f'{t["id"]}: even Must only is {len(txt):,} characters, over the {lim:,} limit')
        files[f'targets/{t["id"]}/{t["file"]}'] = txt
        index.append({'target': t['id'], 'label': t['label'], 'file': f'targets/{t["id"]}/{t["file"]}',
                      'selection': sel, 'rules': len(rs), 'characters': len(txt), 'limit': lim, 'where': t.get('where')})
    files['targets/index.json'] = json.dumps(index, indent=1, ensure_ascii=False) + '\n'
    sizes = []
    for rel, txt in files.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding='utf-8')
        sizes.append((rel, len(txt)))
    # data for dashboards, add-in and MCP server
    data = {'meta': {k: meta[k] for k in ('name', 'system', 'version', 'released', 'intro', 'intro_short')},
            'categories': [{'name': c, 'colour': cat_colour[c]} for c in cats],
            'ais': tgt['ais'], 'selections': tgt['selections'], 'targets': tgt['targets'],
            'rules': [{k: v for k, v in r.items() if k != '_file'} for r in rules],
            'candidates': [{k: v for k, v in r.items() if k != '_file'} for r in cands]}
    (out / 'data.json').write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    (out / 'index.html').write_text(landing(index, sizes), encoding='utf-8')
    print(f'wrote {len(files) + 2} files to {out}')
    for rel, n in sizes[:9]:
        print(f'  {rel}: {n:,} chars')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'build' and not ERR:
        build(pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / 'dist')
    report()
    sys.exit(1 if ERR else 0)
