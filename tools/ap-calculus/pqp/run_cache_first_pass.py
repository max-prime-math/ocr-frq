#!/usr/bin/env python3
"""Resumable cache-first BC staging runner. Never emits TestGen questions."""
from __future__ import annotations
import argparse, subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BATCHES=[
 ("05","BC-1998","BC-2002-FORM-B"),("06","BC-2005","BC-2005-FORM-B"),("07","BC-2006","BC-2006-FORM-B"),
 ("08","BC-2007","BC-2007-FORM-B"),("09","BC-2008","BC-2008-FORM-B"),("10","BC-2009","BC-2009-FORM-B"),
 ("11","BC-2010","BC-2010-FORM-B"),("12","BC-2011","BC-2011-FORM-B"),("13","BC-2012","BC-2013"),
 ("14","BC-2014","BC-2015"),("15","BC-2016","BC-2017"),("16","BC-2018","BC-2019")]
LOG=HERE/"AP_CALCULUS_FIRST_PASS_RUN.md"
def run(*args:str)->None: subprocess.run(args,cwd=ROOT,check=True)
def note(line:str)->None:
 if not LOG.exists(): LOG.write_text("# AP Calculus first-pass runner log\n\n")
 with LOG.open("a") as f: f.write(line+"\n")
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--from-tranche",default="05");p.add_argument("--through-tranche",default="16");a=p.parse_args()
 for n,r1,r2 in BATCHES:
  if not a.from_tranche<=n<=a.through_tranche: continue
  catalog=f"data/ap-calculus/tranches/tranche-{n}/catalog.json"; stage=f"data/ap-calculus/tranches/tranche-{n}/staging/intermediate"; cand=f"data/ap-calculus/tranches/tranche-{n}/staging/typst-candidates"; inp=f"data/ap-calculus/tranches/tranche-{n}/mathpix-recovery-inputs"; cache=f"data/ap-calculus/tranches/tranche-{n}/mathpix-recovery-cache/manifest.json"
  note(f"- {datetime.now(timezone.utc).isoformat()}: tranche {n} started ({r1}, {r2}).")
  run("python3","tools/ap-calculus/pqp/generate_cache_tranche_manifest.py","--tranche",n,"--release",r1,"--release",r2)
  run("python3","tools/ap-calculus/pqp/build_tranche_catalog.py","--manifest",f"tools/ap-calculus/pqp/tranche_{n}_manifest.json","--output",catalog)
  run("python3","tools/ap-calculus/pqp/build_tranche_legacy_intermediate.py","--catalog",catalog,"--stage",stage)
  run("python3","tools/ap-calculus/pqp/build_tranche_typst_candidates.py","--intermediate",stage,"--output",cand)
  run("python3","tools/ap-calculus/pqp/prepare_tranche_scoring_recovery_inputs.py","--catalog",catalog,"--output-dir",inp,"--write")
  run("python3","tools/ap-calculus/pqp/submit_tranche_scoring_recovery.py","--queue",inp+"/submission-queue.json","--cache",cache)
  run("python3","tools/ap-calculus/pqp/fetch_tranche_scoring_recovery.py","--cache",cache,"--poll","--sleep","10","--timeout","300")
  run("python3","tools/ap-calculus/pqp/attach_tranche_scoring_recovery.py","--cache",cache,"--stage",stage)
  run("python3","tools/ap-calculus/pqp/build_tranche_typst_candidates.py","--intermediate",stage,"--output",cand,"--replace")
  note(f"- {datetime.now(timezone.utc).isoformat()}: tranche {n} recovered and left blocked for audit.")
 return 0
if __name__=="__main__": raise SystemExit(main())
