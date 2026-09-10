import collections
import copy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools/manitoba-precalc-40s/pqp'))
import export_manitoba_pqp_mathpix as e

source = e.OUT_DIR / 'manitoba-pc40s-2014-jan'
output = ROOT / 'data/manitoba-precalc-40s/workspace/derived/pilot-2014-jan'
output.mkdir(exist_ok=True)
shutil.copytree(source / 'assets', output / 'assets', dirs_exist_ok=True)
package = json.loads((source / 'manitoba-pc40s-2014-jan.pqp.json').read_text())
original = copy.deepcopy(package)
e.extract_images(['pc_2014_jan_mg'], output / 'assets')
rows = {int(row['question']): row for row in e.load_catalog(2014, 'jan', None)}
pages = e.doc_page_map('pc_2014_jan_mg')
assets = {a['id']: a for a in package['assets']}
report = []
for question in package['questions']:
    if question['kind'] == 'mcq':
        continue
    number = int(question['provenance']['sourceQuestionNumber'])
    row = rows[number]
    items = []
    continuing = False
    for page_number in row['mgSourcePages']:
        segment, _, continuing = e.guide_solution_items_for_question(pages[page_number], number, continuing)
        items.extend(segment)
    latex, filenames = e.items_to_text_and_images(items)
    rejection = e.solution_rejection_reason(latex, question['content']['stem'].get('extensions', {}).get('latexSource', ''))
    if rejection:
        raise RuntimeError(f'{number}: {rejection}')
    pieces = []
    for item in items:
        if item['kind'] == 'image':
            pieces.append(f'#image("assets/{item["text"]}", width: {float(item.get("width") or 1) * 100:.1f}%)')
        else:
            converted = subprocess.run(['node', str(Path(__file__).with_name('convert.mjs'))], input=json.dumps([item['text']]), text=True, capture_output=True)
            if converted.returncode:
                report.append({'question': number, 'field': 'conversion', 'errors': str(item['text'])[:800]})
                pieces.append(e.latex_to_typst_fallback(str(item['text'])))
            else:
                pieces.append(e.clean_typst_output(json.loads(converted.stdout)[0]))
    text = '\n\n'.join(pieces)
    question['content']['solution'] = {
        'format': 'typst', 'text': text,
        'extensions': {'latexSource': latex, 'source': 'mathpix', 'mathpixPdfId': 'cc9001ad-6312-43bc-93f7-8b12c5460552'}
    }
    for filename in filenames:
        if not (output / 'assets' / filename).is_file():
            raise RuntimeError(f'Missing image {filename}')
        aid = f'asset_{Path(filename).stem}'
        assets[aid] = {'id': aid, 'kind': 'image', 'filename': filename, 'mimeType': 'image/jpeg',
                       'storage': {'mode': 'external', 'path': f'assets/{filename}'}}
        question['assets'].append(aid)
    question.setdefault('extensions', {})['reviewStatus'] = 'unreviewed'
    for field in ['stem', 'solution']:
        document = output / f'q{number:02d}-{field}.typ'
        document.write_text(question['content'][field]['text'])
        result = subprocess.run(['typst', 'compile', str(document), str(document.with_suffix('.pdf'))], capture_output=True, text=True)
        if result.returncode:
            report.append({'question': number, 'field': field, 'errors': result.stderr[:1600]})
for before, after in zip(original['questions'], package['questions']):
    assert before['content']['stem'] == after['content']['stem']
    assert before.get('answer') == after.get('answer')
    assert before['content'].get('choices') == after['content'].get('choices')
package['assets'] = list(assets.values())
package['diagnostics'] = [d for d in package.get('diagnostics', []) if d.get('code') != 'solution-mathpix-rejected-source-pdf-fallback']
package['producer']['exportedAt'] = e.utc_now()
(output / 'manitoba-pc40s-2014-jan.pqp.json').write_text(json.dumps(package, indent=2, ensure_ascii=False))
(output / 'compile-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps({'output': str(output), 'compileFailures': len(report), 'errors': report}, indent=2))
