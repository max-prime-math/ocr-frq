#!/usr/bin/env python3
"""Preserving, compile-checked Mathpix -> editable Typst AP draft conversion.

No full-question raster fallback, algebraic simplification, or diagram deletion.
The original OCR stays in canonical records; all repairs are reproducible here.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools/manitoba-precalc-40s/pqp"))
from manitoba_typst_conversion import convert_many, replace_call


def unwrap_command(text, command):
    """Retain a formatting command's balanced argument, including nested math."""
    pattern = re.compile(r'\\' + command + r'(?:\[[^]]*\])?\s*\{')
    while match := pattern.search(text):
        at = match.end()
        depth = 1
        end = at
        while end < len(text) and depth:
            if text[end] == '\\':
                end += 2
                continue
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        if depth:
            raise ValueError('Unbalanced formatting command: ' + command)
        text = text[:match.start()] + text[at:end-1] + text[end:]
    return text


# Exam-booklet logistics and page headers are not part of the mathematical
# prompt. Every variant seen in the 408 source records is listed explicitly.
EXAM_LOGISTICS = re.compile(
    r'\s*Write\s+your\s+responses\s+to\s+this\s+question\s+only\s+on\s+the\s+designated\s+pages\s+in\s+the\s+separate\s+Free\s+Response\s+booklet\.'
    r'(?:\s*Write\s+your\s+solution\s+to\s+each\s+part\s+in\s+the\s+space\s+provided\s+for\s+that\s+part\.)?'
    r'|\s*\(Note:\s+(?:Use\s+the|The)\s+(?:axes|slope\s+field)\s+(?:are\s+)?provided\s+in\s+the\s+(?:pink\s+)?(?:test|exam)\s+booklet(?:\s+only)?\.\)'
    r'|^The\s+College\s+Board\s+Advanced\s+Placement\s+Examination\s*')


def flatten_header_tabulars(raw):
    """A one-column tabular inside a table cell is a wrapped header label."""
    def join(match):
        lines = [line.strip() for line in re.split(r'\\\\', match.group(1))]
        return ' '.join(line for line in lines if line)
    return re.sub(r'\\begin\{tabular\}\{c\}((?:(?!\\begin\{tabular\}).)*?)\\end\{tabular\}', join, raw, flags=re.S)


def prepare(raw, assets):
    """Only normalize notation/layout; preserve math grouping and all objects."""
    raw = EXAM_LOGISTICS.sub('', raw)
    raw = flatten_header_tabulars(raw)
    # A table is its own paragraph; OCR often runs the next sentence into it.
    raw = re.sub(r'\\begin\{tabular\}', r'\n\n\\begin{tabular}', raw)
    raw = re.sub(r'\\end\{tabular\}', r'\\end{tabular}\n\n', raw)
    replacements = {}
    def image(match):
        ref = match.group(1)
        name = Path(ref).name
        found = next((a for a in assets if a['name'] == name or a['path'] == ref), None)
        if not found:
            raise ValueError(f"Unresolved OCR image reference: {ref}")
        token = f"PQPIMAGEPLACEHOLDER{len(replacements)}END"
        replacements[token] = '#image(' + json.dumps('/imgs/' + found['name']) + ', width: 65%)'
        return '\n\n' + token + '\n\n'
    raw = re.sub(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', image, raw)
    raw = re.sub(r'!\[[^]]*\]\(([^)]+)\)', image, raw)
    raw = re.sub(r'\\(?:begin|end)\{(?:center|figure\*?)\}(?:\[[^]]*\])?', '', raw)
    raw = raw.replace(r'\centering', '')
    # Caption configuration controls formatting only; actual captions remain.
    raw = re.sub(r'\\captionsetup\{[^{}]*\}', '', raw)
    raw = unwrap_command(raw, 'caption')
    # Lists from OCR represent printed question and subpart labels. Flattening
    # wrappers leaves all labels/content intact and avoids fragile nested lists.
    raw = re.sub(r'\\(?:begin|end)\{(?:itemize|enumerate)\}(?:\[[^]]*\])?', '\n\n', raw)
    raw = re.sub(r'\\item\[([^]]*)\]', lambda m: '\n\n' + m[1] + ' ', raw)
    raw = re.sub(r'\\item\b', '\n\n', raw)
    # Spatial OCR stores subparts on separate source lines without list markup.
    # Preserve that structure; inline references such as "in part (a)" remain
    # untouched. TestGen's paragraph normalizer otherwise joins every subpart.
    raw = re.sub(r'(?m)^[ \t]*(\([a-f]\))(?=[ \t])', r'\n\n\1', raw)
    # Roman-numeral items ("(i) ... (ii) ...") are printed one per line within
    # their question or part. Some OCR keeps that as \\, some drops it.
    raw = re.sub(r'(?<!\\\\)\n(?=\((?:i|ii|iii|iv)\)[ \t])', r'\\\\\n', raw)
    # A substack is a no-delimiter vertical stack, not concatenated expressions.
    raw = re.sub(r'\\substack\s*\{', r'\\substack{', raw)
    return raw, replacements


def safe_clean(body):
    body = body.replace('angle.l', '⟨').replace('angle.r', '⟩')
    # Shared cleaner visits the outermost call first; repeat for nested roots.
    for _ in range(8):
        previous = body
        body = replace_call(body, 'mitexsqrt', lambda s: 'sqrt(' + s + ')')
        body = replace_call(body, 'substack', lambda s: 'mat(delim: #none, ' + s.replace('\\', ';') + ')')
        if body == previous:
            break
    # TestGen processes a single newline as a hard markup line break, including
    # inside table code. One-line paragraphs keep tables and math valid there.
    body = '\n\n'.join(re.sub(r'\s*\n\s*', ' ', p).strip() for p in re.split(r'\n\s*\n', body) if p.strip())
    # A final OCR line break is valid at standalone EOF, but TestGen inserts
    # the closing content bracket immediately after the body. A trailing lone
    # backslash then escapes that bracket and breaks the surrounding grid.
    # Remove only this terminal layout break, never escaped literal backslashes.
    if body.endswith('\\') and not body.endswith('\\\\'):
        body = body[:-1].rstrip()
    return tidy(body)


def segments(body):
    """Split Typst into ('markup'|'math'|'code', text) runs.

    Code is a `#name(...)` call with balanced parentheses, skipping strings and
    content blocks; its content blocks are tidied recursively by the caller.
    """
    out, i, start = [], 0, 0
    while i < len(body):
        ch = body[i]
        if ch == '\\':
            i += 2
            continue
        if ch == '$':
            end = i + 1
            while end < len(body) and body[end] != '$':
                end += 2 if body[end] == '\\' else 1
            out += [('markup', body[start:i]), ('math', body[i:end + 1])]
            i = start = end + 1
            continue
        call = re.match(r'#[A-Za-z][\w.]*\(', body[i:])
        if call:
            end, depth, quote = i + call.end(), 1, False
            while end < len(body) and depth:
                c = body[end]
                if quote:
                    quote = c != '"' or body[end - 1] == '\\'
                elif c == '"':
                    quote = True
                elif c in '([':
                    depth += 1
                elif c in ')]':
                    depth -= 1
                end += 1
            out += [('markup', body[start:i]), ('code', body[i:end])]
            i = start = end
            continue
        i += 1
    out.append(('markup', body[start:]))
    return [(kind, text) for kind, text in out if text]


def unescape_math_parens(s):
    r"""`f \(x \)` -> `f(x)` for matched pairs; render-identical in Typst.

    After `^` or `_` a bare parenthesis groups (and disappears), so an escaped
    pair there stays escaped.
    """
    chars, stack = list(s), []
    k = 0
    while k < len(s) - 1:
        if s[k] == '\\' and s[k + 1] == '(':
            stack.append((k, s[:k].rstrip()[-1:] in ('^', '_')))
            k += 2
            continue
        if s[k] == '\\' and s[k + 1] == ')':
            if stack:
                opened, keep = stack.pop()
                if not keep:
                    chars[opened] = chars[k] = ''
            k += 2
            continue
        k += 2 if s[k] == '\\' else 1
    return ''.join(chars)


def tidy_math(text):
    # A span that is only a price ("$dollar 0.05$") is prose: `\$0.05`.
    price = re.fullmatch(r'\s*dollar\s*(\d[\d.,]*)\s*', text[1:-1])
    if price:
        return '\\$' + price[1]
    inner = unescape_math_parens(text[1:-1])
    display = inner[:1].isspace() and inner[-1:].isspace()
    parts = re.split(r'("(?:[^"\\]|\\.)*")', inner)
    for n in range(0, len(parts), 2):
        s = re.sub(r'[ \t]{2,}', ' ', parts[n])
        s = re.sub(r'([(\[]) +', r'\1', s)
        s = re.sub(r' +([)\],!;^_])', r'\1', s)
        # `f (x)` -> `f(x)`. Never after other words: `dot(x)`, `hat(x)` and
        # `bar(x)` are accent calls, not the symbol followed by a group.
        s = re.sub(r"((?<![A-Za-z.])[A-Za-z]|\d|'|\b(?:sin|cos|tan|sec|csc|cot|arcsin|arccos|arctan|sinh|cosh|tanh|ln|log|exp|lim|max|min)) +\(", r'\1(', s)
        s = re.sub(r'(?<=[\w)])\^\((prime(?: prime)*)\)', lambda m: "'" * len(m[1].split()), s)
        parts[n] = s
    inner = ''.join(parts)
    return '$ ' + inner.strip() + ' $' if display else '$' + inner.strip() + '$'


def tidy_markup(text):
    # `\(-5` renders a minus sign but `(-5` a hyphen, so that escape stays.
    text = re.sub(r'\\([,;)]|\((?!-))', r'\1', text)
    text = re.sub(r'(?<=\S)\\/', '/', text)
    text = re.sub(r'\bdollar (?=\d)', r'\\$', text)
    # OCR spacing: "is 0 , and" / "is 1 ." (the exams print "0," and "1.").
    text = re.sub(r'(?<=\d) ([,.])(?=\s|$)', r'\1', text)
    # Runs of spaces render as one; keep the source equally tidy.
    return re.sub(r'(?<=\S)[ \t]{2,}(?=\S)', ' ', text)


def tidy_table(call):
    """Drop OCR row-terminator cells and repeated rules; trim cell padding."""
    head, args = call[:call.index('(') + 1], call[call.index('(') + 1:-1]
    items, depth, quote, cur = [], 0, False, ''
    for k, c in enumerate(args):
        if quote:
            quote = c != '"' or args[k - 1] == '\\'
        elif c == '"':
            quote = True
        elif c in '([':
            depth += 1
        elif c in ')]':
            depth -= 1
        if c == ',' and not depth and not quote:
            items.append(cur.strip())
            cur = ''
        else:
            cur += c
    if cur.strip():
        items.append(cur.strip())
    columns = next(int(m[1]) for m in (re.fullmatch(r'columns:\s*(\d+)', it) for it in items) if m)
    cells = lambda: [it for it in items if it.startswith('[')]
    while len(cells()) % columns and items and items[-1] == '[]':
        items.pop()
        while items and items[-1].startswith('table.hline') and len(items) > 1 and items[-2] == items[-1]:
            items.pop()
    deduped = []
    for it in items:
        if not (it.startswith('table.hline') and deduped and deduped[-1] == it):
            deduped.append(it)
    tidied = ['[' + tidy(it[1:-1]).strip() + ']' if it.startswith('[') else it for it in deduped]
    return head + ', '.join(tidied) + ')'


def tidy(body):
    """Readable, render-identical Typst: spacing, escapes, tables and breaks."""
    out = []
    for kind, text in segments(body):
        if kind == 'math':
            out.append(tidy_math(text))
        elif kind == 'markup':
            out.append(tidy_markup(text))
        elif text.startswith('#table('):
            out.append(tidy_table(text))
        else:
            out.append(text)
    body = ''.join(out)
    paragraphs = []
    for p in re.split(r'\n\s*\n', body):
        # A line break directly before a paragraph break renders nothing.
        p = re.sub(r'(?<!\\)\\$', '', p.rstrip()).rstrip()
        # Figure captions printed under a graph are their own paragraph.
        p = re.sub(r'^((?:Graph of \$[^$]*\$)|(?:Note: Figure not drawn to scale\.))\s*(?<!\\)\\?\s+', r'\1\n\n', p)
        if p:
            paragraphs.append(p)
    return '\n\n'.join(paragraphs)


def compile_body(body, assets):
    with tempfile.TemporaryDirectory(prefix='ap-native-compile-') as folder:
        root = Path(folder)
        images = root / 'imgs'
        images.mkdir()
        for asset in assets:
            src = Path(asset['path'])
            if not src.is_absolute():
                src = ROOT / src
            if not src.is_file():
                return f"Missing asset: {src}"
            # Typst cannot follow symlinks outside its root.
            import shutil
            shutil.copyfile(src, images / asset['name'])
        path = root / 'question.typ'
        processed = '\n\n'.join(p.replace('\n', '\\\n') for p in re.split(r'\n{2,}', body.strip()))
        path.write_text('#block(width: 100%)[\n#grid(columns: (auto, 1fr), [1.], [' + processed + '])\n]')
        run = subprocess.run(['typst', 'compile', '--root', str(root), str(path), str(root/'question.pdf')], capture_output=True, text=True, timeout=45)
        return None if run.returncode == 0 else run.stderr[-6000:]


def convert_record(path, out):
    source_bytes = path.read_bytes()
    record = json.loads(source_bytes)
    assets = record.get('assets', [])
    issues = list(record.get('issues', []))
    body, error = '', None
    try:
        raw, replacements = prepare(record['rawPrompt'], assets)
        body = safe_clean(convert_many([raw])[0])
        if re.search(r'\bmitex[A-Za-z]+', body):
            raise ValueError('Unconverted MiTeX construct: ' + ', '.join(set(re.findall(r'\bmitex[A-Za-z]+', body))))
        for token, value in replacements.items():
            if token not in body:
                raise ValueError('Converter lost protected image token: ' + token)
            body = body.replace(token, value)
        # Images are separate paragraphs only after substitution.
        body = tidy(body)
        error = compile_body(body, assets)
    except Exception as exc:
        error = str(exc)
    candidate = {k: record[k] for k in ['id', 'course', 'year', 'form', 'question', 'source'] if k in record}
    candidate.update({'schemaVersion': 1, 'bodyTypst': body, 'assets': assets,
        'compile': {'body': error is None, 'errors': {'body': error}},
        'sourceChecks': record.get('sourceChecks', {}), 'issues': issues,
        'quality': 'native-draft', 'reviewState': 'unreviewed',
        'sourceRecordSha256': hashlib.sha256(source_bytes).hexdigest(),
        'converterSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'ocrEvidence': record.get('ocrEvidence', {})})
    (out / path.name).write_text(json.dumps(candidate, indent=2) + '\n')
    return {'id': record['id'], 'bodyCompiles': error is None, 'assets': len(assets), 'issues': issues, 'error': error}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--records', type=Path, default=ROOT/'data/ap-calculus/native-pass/intermediate/records')
    parser.add_argument('--output', type=Path, default=ROOT/'data/ap-calculus/native-pass/candidates')
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--only', help='Regex matching question IDs')
    args = parser.parse_args()
    # A broken toolchain would otherwise overwrite every good candidate with an
    # empty failed one. Fail before writing anything.
    if compile_body(safe_clean(convert_many(['$x^2$'])[0]), []) is not None:
        raise SystemExit('Toolchain preflight failed: typst could not compile a trivial body')
    args.output.mkdir(parents=True, exist_ok=True)
    sources =[p for p in sorted(args.records.glob('*.json')) if p.stem != 'index']
    paths = [p for p in sources if not args.only or re.search(args.only,p.stem)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        changed_rows = list(pool.map(lambda p: convert_record(p,args.output), paths))
    # A targeted repair must not replace the full inventory with a partial
    # index. Rebuild it from all current source IDs, marking stale artifacts.
    rows = []
    converter_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for source_path in sources:
        candidate_path = args.output / source_path.name
        if not candidate_path.is_file():
            continue
        candidate = json.loads(candidate_path.read_text())
        rows.append({'id': candidate['id'],
                     'bodyCompiles': candidate['compile']['body'],
                     'nativeBodyPresent': bool(candidate['bodyTypst']),
                     'assets': len(candidate['assets']),
                     'issues': candidate['issues'],
                     'error': candidate['compile']['errors']['body'],
                     'sourceFresh': candidate.get('sourceRecordSha256') == hashlib.sha256(source_path.read_bytes()).hexdigest(),
                     'converterFresh': candidate.get('converterSha256') == converter_hash})
    index = {'schemaVersion': 1, 'candidates': rows, 'total': len(rows),
             'sourceTotal': len(sources), 'convertedThisRun': len(changed_rows),
             'bodyCompilePassed': sum(r['bodyCompiles'] for r in rows),
             'nativeBodyCount': sum(r['nativeBodyPresent'] for r in rows),
             'freshCandidateCount': sum(r['sourceFresh'] and r['converterFresh'] for r in rows)}
    (args.output/'index.json').write_text(json.dumps(index,indent=2)+'\n')
    print(json.dumps({k:v for k,v in index.items() if k!='candidates'}))
    for row in rows:
        if row['error']:
            print(row['id'],row['error'][:400])


if __name__ == '__main__':
    main()
