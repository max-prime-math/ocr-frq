"""Mathpix LaTeX to native Typst, using the installed MiTeX WASM converter.

No silent LaTeX fallback: failures must be repaired before publication.
"""
import json
import re
import subprocess
from pathlib import Path


def compact_spaced_numbers(text):
    text=re.sub(r"(?<=\d)\s+\.\s+(?=\d)", ".", text)
    return re.sub(r"(?<=\d)\s+(?=\d)", "", text)


def split_top_level_once(text):
    # arg0 is the LaTeX array column specification, before the first comma.
    return text.split(",", 1)

def replace_call(text,name,convert):
    # Escaped delimiters are printed symbols, not Typst function delimiters.
    start=0
    while True:
        at=text.find(name+'(',start)
        if at<0:break
        i=at+len(name)+1; begin=i; depth=1; quote=False
        while i<len(text):
            c=text[i]
            if c=='\\':i+=2;continue
            if c=='"':quote=not quote
            if not quote:
                if c=='(':depth+=1
                elif c==')':depth-=1
            if depth==0:break
            i+=1
        if depth:break
        value=convert(text[begin:i]);text=text[:at]+value+text[i+1:];start=at+len(value)
    return text

def clean(text):
    text=re.sub(r'#math\.equation\(block:\s*false,\s*\$(.*?)\$\);',lambda m:'$'+m[1]+'$',text,flags=re.S)
    text=re.sub(r'#image\(width:\s*([0-9.]+)\s*\*\s*100%,\s*"([^"]+)"\)',lambda m:f'#image("{m[2]}", width: {float(m[1])*100:.1f}%)',text)
    text=re.sub(r'#textmath\[([^\]]*)\];?',lambda m:json.dumps(re.sub(r'\\([^A-Za-z])',r'\1',m[1])),text)
    text=text.replace('mitexmathbf(', 'bold(').replace('mitexnot(', 'cancel(').replace('mitexunderbrace(', 'underbrace(')
    text=replace_call(text,'mitexsqrt',lambda s:re.sub(r'^\\\[([^]]+)\\\],',r'root(\1,',s)+')' if s.startswith(r'\[') else 'sqrt('+s+')')
    text=text.replace('zws','""')
    def array(inner):
        if inner.startswith('arg0:'):
            _,inner=split_top_level_once(inner)
        return 'mat(delim: #none, '+inner+')'
    for _ in range(10):
        text=replace_call(text,'mitexarray',array)
        text=replace_call(text,'aligned',lambda s:s)
        text=replace_call(text,'gathered',lambda s:s)
    text=replace_call(text,'operatorname',lambda s:'op('+json.dumps(s.replace(' ',''))+')')
    for helper,which in [('stackrel','^'),('underset','_')]:
        text=replace_call(text,helper,lambda s:'limits('+s.split(',',1)[1]+')'+which+'('+s.split(',',1)[0]+')')
    text=re.sub(r'\b[lr]vert\b','|',text)
    text=text.replace('lr(⌊', 'lr(floor.l ')
    text=re.sub(r'\[PQPspan(\d+)start\s*(.*?)PQPspanend\s*\]',lambda m:f'table.cell(colspan: {m[1]})[{m[2]}]',text,flags=re.S)
    # MiTeX emits escaped delimiters and spaces between decimal digits.
    def math(m):
        s=m[1]
        # LaTeX uses \\circ for both composition and a superscript degree.
        # Only the superscript form denotes degrees; f \\circ g must survive.
        s=re.sub(r'\^\(\s*compose\s*\)', '^(degree)', s)
        s=compact_spaced_numbers(s)
        return '$'+s+'$'
    text=re.sub(r'(?<!\\)\$(.*?)(?<!\\)\$',math,text,flags=re.S)
    return text.strip()
def prepare(raw):
    raw=re.sub(r'(\\begin\{tabular\})\[[^]]*\]',r'\1',raw)
    raw=re.sub(r'(?<!\\)\s*\\end\{tabular\}',r' \\\\ \\end{tabular}',raw)
    raw=re.sub(r'\\multirow(?:\[[^]]*\])?\{[^{}]*\}\{[^{}]*\}', '', raw)
    while (match:=re.search(r'\\multicolumn\{(\d+)\}\{[^{}]*\}\{',raw)):
        start=match.end();i=start;depth=1
        while depth and i<len(raw):
            if raw[i]=='\\':i+=2;continue
            if raw[i]=='{':depth+=1
            if raw[i]=='}':depth-=1
            i+=1
        assert depth==0
        raw=raw[:match.start()]+f'PQPspan{match[1]}start '+raw[start:i-1]+' PQPspanend'+raw[i:]
    raw=raw.replace(r'\longdiv',r'\vert\overline')
    if r'\begin{itemize}' not in raw:raw=raw.replace(r'\end{itemize}','')
    return raw


def convert_many(values):
    result=subprocess.run(["node",str(Path(__file__).with_name("manitoba_mitex.mjs"))],
        input=json.dumps([prepare(v) for v in values]),text=True,capture_output=True,check=True)
    results=json.loads(result.stdout)
    if len(results)!=len(values):raise RuntimeError("MiTeX returned an incomplete batch")
    output=[]
    for value in results:
        if "error" in value:raise RuntimeError("MiTeX conversion failed: "+value["error"])
        converted=clean(value["text"])
        if re.search(r"\\[A-Za-z]{2,}",converted):raise RuntimeError("LaTeX command remains after conversion")
        output.append(converted)
    return output


def apply_reviewed_overrides(package):
    questions={q['id']:q for q in package['questions']}
    for item in json.loads(Path(__file__).with_name('typst_overrides.json').read_text()):
        if item['id'] not in questions:continue
        q=questions[item['id']]
        key='stem' if item['field']=='body' else item['field']
        doc=q['content'][key]
        doc['text']=item['text'].replace('/imgs/','assets/')
        doc['format']='typst'
        doc.setdefault('extensions',{})['editorialRepair']=item['reason']
        doc['extensions']['source']='editorial-repair'
