#!/usr/bin/env python3
"""Generate a cache-ready BC tranche manifest; boundaries remain audit-blocked."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import fitz

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def prompt_pages(path: Path) -> dict[int, list[int]]:
    found={q: [] for q in range(1,7)}
    with fitz.open(path) as pdf:
        for page_no,page in enumerate(pdf,1):
            for text in re.findall(r"(?m)^\s*([1-6])\.",page.get_text()):
                found[int(text)].append(page_no)
    if any(not pages for pages in found.values()):
        raise ValueError(f"Could not locate all printed question starts in {path.name}: {found}")
    return {q:[pages[0]] for q,pages in found.items()}

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--tranche",required=True)
    parser.add_argument("--release",action="append",required=True,help="e.g. BC-2004 or BC-2004-FORM-B")
    args=parser.parse_args()
    rows=[]
    for release in args.release:
        match=re.fullmatch(r"BC-(\d{4})(-FORM-B)?",release)
        if not match: raise SystemExit(f"Unsupported release: {release}")
        year=int(match.group(1)); form="B" if match.group(2) else "standard"
        prompt_rel=f"data/ap-calculus-bc/source-pdfs/{release}.pdf"; sg_rel=f"data/ap-calculus-bc/source-pdfs/SG-{release}.pdf"
        prompt=ROOT/prompt_rel; sg=ROOT/sg_rel
        if not prompt.is_file() or not sg.is_file(): raise SystemExit(f"Missing paired sources for {release}")
        pages=prompt_pages(prompt)
        with fitz.open(sg) as pdf:
            if len(pdf)!=7: raise SystemExit(f"Expected seven-page guide: {sg.name}")
        for q in range(1,7):
            suffix="-form-b" if form=="B" else ""
            rows.append({"id":f"ap-calc-bc-{year}{suffix}-frq-{q:02d}","course":"BC","year":year,"form":form,"question":q,"promptPdf":prompt_rel,"scoringGuidePdf":sg_rel,"promptPages":pages[q],"scoringGuidePages":[q+1],"legacyMathpix":{"promptZip":f"data/ap-calculus-bc/mathpix-zips/{release}.zip","scoringGuideZip":f"data/ap-calculus-bc/mathpix-zips/SG-{release}.zip"},"focus":["automapped-source-boundary","audit-required"]})
    if len(rows)!=12: raise SystemExit("A two-release tranche must contain 12 questions")
    target=HERE/f"tranche_{args.tranche}_manifest.json"
    target.write_text(json.dumps({"schemaVersion":1,"tranche":f"ap-calculus-frq-tranche-{args.tranche}","purpose":"Automapped cache-first BC staging; all page boundaries require later manual audit.","questions":rows},indent=2)+"\n")
    print(target)
if __name__=="__main__": main()
