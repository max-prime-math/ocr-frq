"""Convert Manitoba PQPs, compile every field, and build a validated staging bank.

Does not overwrite the source bank. Original LaTeX remains in jobs.json and PQPs.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from manitoba_typst_conversion import convert_many

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bank',type=Path,required=True)
    parser.add_argument('--pqp-root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--testgen',type=Path,required=True)
    args=parser.parse_args()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    if (out/'bank').exists():raise SystemExit('Staging bank already exists; choose a new output directory')
    shutil.copytree(args.bank/'images',out/'imgs',dirs_exist_ok=True)
    sources={}
    for p in sorted(args.pqp_root.glob('*/*.pqp.json')):
        for q in json.loads(p.read_text())['questions']:sources[q['id']]=q
    jobs=[]
    index=json.loads((args.bank/'questions/index.json').read_text())
    for entry in index['questions']:
        q=sources[entry['id']]
        docs=[('body',q['content']['stem']),('solution',q['content']['solution'])]
        docs.extend(('choice:'+c['id'],c['body']) for c in q['content'].get('choices',[]))
        for field,doc in docs:
            jobs.append({'id':q['id'],'field':field,'latex':doc.get('extensions',{}).get('latexSource',doc['text'])})
    for j,text in zip(jobs,convert_many([j['latex'] for j in jobs])):
        j['typst']=text.replace('assets/','/imgs/')
    for override in json.loads(Path(__file__).with_name('typst_overrides.json').read_text()):
        matches=[j for j in jobs if (j['id'],j['field'])==(override['id'],override['field'])]
        for j in matches:j.update(typst=override['text'],repairNote=override['reason'])
    fields=out/'fields';fields.mkdir(exist_ok=True)
    def compile_field(j):
        name=j['id']+'-'+j['field'].replace(':','-')
        p=fields/(name+'.typ')
        p.write_text('#set page(paper: "a4", margin: 15mm)\n#set text(size: 10pt)\n'+j['typst'])
        try:
            r=subprocess.run(['typst','compile','--root',str(out),str(p),str(p.with_suffix('.pdf'))],text=True,capture_output=True,timeout=30)
            if r.returncode:return {'id':j['id'],'field':j['field'],'error':r.stderr}
        except subprocess.TimeoutExpired:return {'id':j['id'],'field':j['field'],'error':'compile timeout'}
    with ThreadPoolExecutor(max_workers=6) as pool:errors=[r for r in pool.map(compile_field,jobs) if r]
    (out/'jobs.json').write_text(json.dumps(jobs,indent=2))
    (out/'compile-errors.json').write_text(json.dumps(errors,indent=2))
    if errors:raise SystemExit(f'{len(errors)} fields failed: see compile-errors.json')
    subprocess.run(['node',str(Path(__file__).with_name('build_typst_bank.mjs')),str(args.bank.resolve()),str(out/'jobs.json'),str(out/'bank'),str(args.testgen.resolve())],check=True)
    subprocess.run(['python3',str(Path(__file__).with_name('review_typst_bank.py')),str(out/'bank'),str(out)],check=True)

if __name__=='__main__':main()
