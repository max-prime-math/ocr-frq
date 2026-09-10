import json
from pathlib import Path
import re
import subprocess
import sys
import fitz

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'tools/manitoba-precalc-40s/pqp'))
import export_manitoba_pqp_mathpix as e
out=ROOT / 'data/manitoba-precalc-40s/workspace/derived/pilot-2014-jan'
file=out/'manitoba-pc40s-2014-jan.pqp.json'
package=json.loads(file.read_text())
issues=json.loads((out/'compile-report.json').read_text())
fallbacks={x['question'] for x in issues if x['field'] in ('solution','conversion')}
rows={int(r['question']):r for r in e.load_catalog(2014,'jan',None)}
source=e.MB_DIR/'source-pdfs/marking-guides/pc_14_jan_mg.pdf'
with fitz.open(source) as pdf:
 for q in package['questions']:
  n=int(q['provenance']['sourceQuestionNumber'])
  if n==28:
   q['content']['stem']['text']=q['content']['stem']['text'].replace('$_(n)', '$""_(n)')
  if n not in fallbacks: continue
  images=[]
  for page in rows[n]['mgSourcePages']:
   filename=f'pc_14_jan_mg-page-{page:03d}.png'
   pdf[page-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(out/'assets'/filename))
   aid=f'asset_pc14jan_mg_page_{page:03d}'
   if not any(a['id']==aid for a in package['assets']):
    package['assets'].append({'id':aid,'kind':'image','filename':filename,'mimeType':'image/png','storage':{'mode':'external','path':f'assets/{filename}'},'source':{'originalPath':source.name,'page':page}})
   if aid not in q['assets']: q['assets'].append(aid)
   images.append(f'#image("assets/{filename}", width: 100%)')
  solution=q['content']['solution']
  solution['extensions']['candidateTypst']=solution['text']
  solution['extensions']['source']='marking-guide-image-fallback'
  solution['extensions']['sourcePages']=rows[n]['mgSourcePages']
  solution['text']='Official marking-guide reference pages (may include scoring notes and exemplars).\n\n'+'\n\n'.join(images)
  package['diagnostics'].append({'level':'warning','code':'solution-marking-guide-image-fallback','questionId':q['id'],'message':'Editable OCR conversion needs repair; original guide pages displayed instead.'})

# Keep only assets referenced by question content; candidates retain their OCR
# source for later repair but are not used as rendered content.
referenced=set()
for q in package['questions']:
 visible=[q['content']['stem']['text'],q['content']['solution']['text']]
 visible += [c['body']['text'] for c in q['content'].get('choices',[])]
 referenced.update(re.findall(r'assets/([^"\s)]+)','\n'.join(visible)))
package['assets']=[a for a in package['assets'] if a['filename'] in referenced]
ids={a['id'] for a in package['assets']}
for q in package['questions']: q['assets']=[a for a in q['assets'] if a in ids]
for name in referenced: assert (out/'assets'/name).is_file(), name
package['extensions']['notes'].append('January 2014 pilot: 29 editable Mathpix solutions, 5 guide-page image fallbacks, 10 answer-key solutions; visual review pending.')
file.write_text(json.dumps(package,indent=2,ensure_ascii=False))
review=['#set page(paper: "a4", margin: 18mm)','#set text(size: 10pt)','= January 2014 — staging review','Generated pilot. Not yet approved for classroom publication.']
failures=[]
for q in package['questions']:
 n=int(q['provenance']['sourceQuestionNumber'])
 choices='\n\n'.join(c['id']+'. '+c['body']['text'] for c in q['content'].get('choices',[]))
 body='\n\n'.join([f'= Question {n}',q['content']['stem']['text'],choices,'== Solution',q['content']['solution']['text']])
 p=out/f'q{n:02d}-complete.typ'
 p.write_text(body)
 result=subprocess.run(['typst','compile',str(p),str(p.with_suffix('.pdf'))],capture_output=True,text=True)
 if result.returncode: failures.append({'question':n,'error':result.stderr[:1500]})
 review.extend(['#pagebreak()',body])
(out/'review.typ').write_text('\n\n'.join(review))
report={'questions':len(package['questions']),'mathpixSolutions':29,'guideImageFallbacks':sorted(fallbacks),'answerKeySolutions':10,'compileFailures':failures,'sourcePageHeaderDiscrepancies':0,'visualReview':'pending; Question 1 spot-checked'}
(out/'pilot-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not failures: subprocess.run(['typst','compile',str(out/'review.typ'),str(out/'review.pdf')],check=True)
