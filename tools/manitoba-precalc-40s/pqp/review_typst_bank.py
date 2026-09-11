"""Compile exam review PDFs and flag text extending beyond the page margin."""
import json, subprocess, sys, re
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import fitz

bank, stage = map(Path, sys.argv[1:3])
review=stage/'review';review.mkdir(exist_ok=True)
groups=defaultdict(list)
for p in sorted((bank/'questions').glob('*.json')):
    if p.name=='index.json':continue
    q=json.loads(p.read_text())['question']
    groups[q['id'].rsplit('-q',1)[0]].append(q)
def build(item):
    session,questions=item
    parts=['#set page(paper: "a4", margin: 15mm)','#set text(size: 10pt)',
      f'= {session}', 'Typst conversion review. OCR content and mathematical accuracy require editorial review.']
    missing=[]
    for q in questions:
        number=int(q['id'].rsplit('-q',1)[1]);parts+=['#pagebreak()',f'= Question {number}',q['body']]
        for label,choice in q.get('choices',{}).items():parts.append(f'*{label}.*\n\n{choice}')
        parts+=['== Solution',q['solution'] or '_No solution was extracted from the marking guide._']
        if not q['solution']:missing.append(q['id'])
    typ=review/(session+'.typ');typ.write_text('\n\n'.join(parts))
    r=subprocess.run(['typst','compile','--root',str(stage),str(typ),str(typ.with_suffix('.pdf'))],capture_output=True,text=True,timeout=90)
    if r.returncode:return {'session':session,'error':r.stderr}
    flags=[];qnum=None
    with fitz.open(typ.with_suffix('.pdf')) as doc:
        pages=len(doc)
        for i,page in enumerate(doc):
            m=re.search(r'Question (\d+)',page.get_text())
            if m:qnum=int(m[1])
            blocks=page.get_text('blocks')
            if any(b[0]<35 or b[2]>page.rect.width-35 for b in blocks):
                flags.append({'page':i+1,'question':qnum,'reason':'text-near-or-outside-horizontal-margin'})
    return {'session':session,'questions':len(questions),'pages':pages,'layoutReview':flags,'missingSolutions':missing}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(build,groups.items()))
(review/'report.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'exams':len(results),'questions':sum(r.get('questions',0) for r in results),'compileFailures':[r for r in results if 'error'in r], 'layoutFlags':sum(len(r.get('layoutReview',[])) for r in results),'missingSolutions':[q for r in results for q in r.get('missingSolutions',[])]},indent=2))
if any('error'in r for r in results):raise SystemExit(1)
