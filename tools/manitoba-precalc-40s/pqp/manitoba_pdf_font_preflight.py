#!/usr/bin/env python3
"""Inventory PDF fonts and optionally normalize reviewed unembedded MT-Extra.

Never edits inputs. This is a narrow June-2014 repair, NOT a general font fixer.
Dependencies: PyMuPDF, fontTools; replacement font must be supplied explicitly.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re

import fitz

# Reviewed against June 2014 mathematical context and correctly embedded MT-Extra
# in adjacent sittings. 0xA1 also documented by transpect's MT_Extra.xml;
# 0x55 and 0x6F by Mozilla's archived MT Extra encoding table.
# MT-Extra versions differ: do not extend this by guessing from ordinary letters.
REVIEWED_MAPPING = {0x55: 0x222A, 0x67: 0x22C5, 0x6F: 0x2218, 0xA1: 0x211D}
MAPPING_SOURCES = [
    "https://www-archive.mozilla.org/projects/mathml/fonts/encoding/mtextra",
    "https://github.com/transpect/fontmaps/blob/master/MT_Extra.xml",
]


def is_mt_extra(name: str) -> bool:
    return name.split("+")[-1].replace("-", "").replace(" ", "").lower() == "mtextra"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_pdf(path: Path) -> dict:
    with fitz.open(path) as doc:
        fonts = {}
        for page in doc:
            for font in page.get_fonts(full=True):
                xref, ext, kind, name, resource, encoding, *_ = font
                if xref not in fonts:
                    fonts[xref] = dict(xref=xref, name=name, type=kind,
                                       embedded=bool(doc.extract_font(xref)[3]),
                                       encoding=encoding, pages=[])
                fonts[xref]["pages"].append(page.number + 1)
        for item in fonts.values():
            item["pages"] = sorted(set(item["pages"]))
        missing = [f for f in fonts.values() if is_mt_extra(f["name"]) and not f["embedded"]]
        chars = Counter()
        occurrences = []
        missing_refs = {f["xref"] for f in missing}
        ambiguous_pages = []
        for page in doc:
            page_fonts = page.get_fonts(full=True)
            if not missing_refs.intersection(f[0] for f in page_fonts):
                continue
            if any(is_mt_extra(f[3]) and fonts[f[0]]["embedded"] for f in page_fonts):
                ambiguous_pages.append(page.number + 1)
            for span in page.get_texttrace():
                # Only exact unembedded face names; subset embedded fonts are untouched.
                if span["font"] not in {f["name"] for f in missing}:
                    continue
                for value, glyph, origin, bbox in span["chars"]:
                    chars[value] += 1
                    occurrences.append(dict(page=page.number + 1, code=f"0x{value:02X}",
                                            origin=list(origin), bbox=list(bbox)))
        unknown = sorted(set(chars) - REVIEWED_MAPPING.keys())
        return dict(path=str(path.resolve()), sha256=digest(path), pages=len(doc),
                    missing_mt_extra=missing,
                    unembedded_fonts=[f for f in fonts.values() if not f["embedded"]],
                    affected_pages=sorted({o["page"] for o in occurrences}),
                    codes={f"0x{k:02X}": v for k, v in sorted(chars.items())},
                    occurrences=occurrences, unknown_codes=[f"0x{k:02X}" for k in unknown],
                    ambiguous_pages=ambiguous_pages,
                    status="blocked-ambiguous-font" if ambiguous_pages else "blocked-unknown-glyph" if unknown else
                    "needs-reviewed-normalization" if missing else "no-missing-mt-extra")


def replacement_font(path: Path) -> bytes:
    from fontTools import subset
    from fontTools.ttLib import TTFont

    font = TTFont(path)
    # Open Font License Noto Sans Math is the tested choice. Require embedding
    # permissions rather than silently copying arbitrary restricted font programs.
    if font["OS/2"].fsType & 0x0302:
        raise ValueError("Replacement font disallows unrestricted outline embedding/subsetting")
    cmap = font.getBestCmap()
    if any(code not in cmap for code in REVIEWED_MAPPING.values()):
        raise ValueError("Replacement font is missing a required mathematical glyph")
    names = {code: cmap[target] for code, target in REVIEWED_MAPPING.items()}
    worker = subset.Subsetter()
    worker.populate(glyphs=list(names.values()))
    worker.subset(font)
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap = dict(names)
    buf = BytesIO()
    font.save(buf)
    return buf.getvalue()


def unicode_cmap() -> bytes:
    pairs = "\n".join(f"<{old:02X}> <{new:04X}>" for old, new in REVIEWED_MAPPING.items())
    return ("/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
            "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
            "/CMapName /ReviewedMTExtra-UCS def\n/CMapType 2 def\n"
            "1 begincodespacerange\n<00> <FF>\nendcodespacerange\n"
            f"{len(REVIEWED_MAPPING)} beginbfchar\n{pairs}\nendbfchar\n"
            "endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend\n").encode()


def normalize_pdf(source: Path, output: Path, font_path: Path) -> dict:
    if output.exists() or output.resolve() == source.resolve():
        raise ValueError("Output must be a new file distinct from the source")
    report = inspect_pdf(source)
    if report.get("ambiguous_pages"):
        raise ValueError("Embedded and unembedded MT-Extra share a page; isolate and review first")
    if report["unknown_codes"]:
        raise ValueError(f"Unreviewed MT-Extra codes: {report['unknown_codes']}")
    if not report["missing_mt_extra"]:
        raise ValueError("No missing MT-Extra: do not rewrite already embedded source")
    with fitz.open(source) as doc:
        original_streams = {xref: doc.xref_stream(xref) for p in doc for xref in p.get_contents()}
        # An unembedded and embedded face with identical texttrace names would
        # make occurrence accounting ambiguous; fail rather than overpromise.
        all_fonts = {f[0]: f for p in doc for f in p.get_fonts(full=True)}
        missing_names = {f["name"] for f in report["missing_mt_extra"]}
        if any(f[3] in missing_names and doc.extract_font(xref)[3] for xref, f in all_fonts.items()):
            raise ValueError("Ambiguous embedded/unembedded face names")
        for item in report["missing_mt_extra"]:
            xref = item["xref"]
            if item["type"] != "TrueType":
                raise ValueError("Only simple TrueType MT-Extra is reviewed")
            encoding = doc.xref_get_key(xref, "Encoding")
            if encoding not in [("null", "null"), ("name", "/WinAnsiEncoding")]:
                raise ValueError(f"Unsupported MT-Extra encoding: {encoding}")
            first = doc.xref_get_key(xref, "FirstChar")
            last = doc.xref_get_key(xref, "LastChar")
            widths = doc.xref_get_key(xref, "Widths")
            if first[0] != "int" or last[0] != "int" or widths[0] != "array":
                raise ValueError("Missing explicit advance widths")
            if (int(first[1]), int(last[1])) != (0, 255):
                raise ValueError("Unexpected character bounds; needs separate review")
        replacement = doc[0].insert_font(fontname="ReviewedMTExtra",
                                         fontbuffer=replacement_font(font_path), set_simple=True)
        cmap_ref = doc.get_new_xref()
        doc.update_object(cmap_ref, "<<>>")
        doc.update_stream(cmap_ref, unicode_cmap())
        for item in report["missing_mt_extra"]:
            xref = item["xref"]
            widths = doc.xref_get_key(xref, "Widths")[1]
            doc.update_object(xref, doc.xref_object(replacement))
            doc.xref_set_key(xref, "Widths", widths)
            doc.xref_set_key(xref, "FirstChar", "0")
            doc.xref_set_key(xref, "LastChar", "255")
            doc.xref_set_key(xref, "ToUnicode", f"{cmap_ref} 0 R")
        if any(doc.xref_stream(xref) != data for xref, data in original_streams.items()):
            raise AssertionError("Page drawing instructions unexpectedly changed")
        output.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output)
    report.update(output=str(output.resolve()), output_sha256=digest(output),
                  replacement_font=str(font_path.resolve()), replacement_font_sha256=digest(font_path),
                  mapping={f"0x{k:02X}": chr(v) for k, v in REVIEWED_MAPPING.items()},
                  mapping_sources=MAPPING_SOURCES, status="normalized-needs-visual-review")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, help="Normalize ONE source into a new PDF")
    parser.add_argument("--font", type=Path, help="Explicit freely embeddable Unicode TTF")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.output:
        if len(args.sources) != 1 or not args.font:
            parser.error("--output requires exactly one source and --font")
        result = [normalize_pdf(args.sources[0], args.output, args.font)]
    else:
        paths = sorted({p for source in args.sources for p in
                        (source.rglob("*.pdf") if source.is_dir() else [source])})
        result = [inspect_pdf(p) for p in paths]
    text = json.dumps(result, indent=2) + "\n"
    if args.report:
        if args.report.exists():
            raise ValueError("Report path already exists")
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
