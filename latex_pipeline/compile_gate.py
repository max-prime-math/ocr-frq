from __future__ import annotations

import subprocess
from pathlib import Path


def compile_latex(tex_path: str, pdf_path: str) -> tuple[bool, str]:
    tex = Path(tex_path).resolve()
    pdf = Path(pdf_path).resolve()
    out_dir = pdf.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={out_dir}",
        f"-jobname={pdf.stem}",
        str(tex),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = ((proc.stdout or "") + (proc.stderr or "")).strip()
    return proc.returncode == 0 and pdf.exists(), output
