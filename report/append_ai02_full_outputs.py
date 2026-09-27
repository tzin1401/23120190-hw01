#!/usr/bin/env python3
"""Attach the verbatim AI outputs to the filled AI-02 form.

The audit table remains compact and points to each numbered transcript entry.
This annex carries the complete output text for all 25 audited artifacts.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from xml.etree import ElementTree as ET
import os

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "23120190_HW01_AI_100"
DOCX = PACKAGE / "[AI-02] - FIT@HCMUS - AI Audit Report.docx"
LOG = PACKAGE / "Appendix_A_Prompt_Log.md"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
MARKER = "Phụ lục B — Toàn văn AI Output cho 25 artifact"


def add_paragraph(body: ET.Element, text: str, *, title: bool = False, new_page: bool = False) -> None:
    paragraph = ET.Element(W + "p")
    props = ET.SubElement(paragraph, W + "pPr")
    spacing = ET.SubElement(props, W + "spacing")
    spacing.set(W + "after", "40" if title else "0")
    if new_page:
        ET.SubElement(props, W + "pageBreakBefore")
    run = ET.SubElement(paragraph, W + "r")
    rpr = ET.SubElement(run, W + "rPr")
    size = ET.SubElement(rpr, W + "sz")
    size.set(W + "val", "22" if title else "18")
    if title:
        ET.SubElement(rpr, W + "b")
    node = ET.SubElement(run, W + "t")
    node.set(XML_SPACE, "preserve")
    node.text = text
    section = body.find(W + "sectPr")
    body.insert(list(body).index(section) if section is not None else len(body), paragraph)


source = LOG.read_text()
entries = [part for part in re.split(r"(?=^### Thời gian:)", source, flags=re.M) if part.startswith("### Thời gian:")]
assert len(entries) == 28
numbers = [2, 5, *range(6, 29)]
assert len(numbers) == 25

with zipfile.ZipFile(DOCX) as original:
    root = ET.fromstring(original.read("word/document.xml"))
    body = root.find(".//" + W + "body")
    existing = "".join(node.text or "" for node in root.iter(W + "t"))
    if MARKER in existing:
        raise SystemExit("The full-output annex is already present")

    add_paragraph(body, MARKER, title=True, new_page=True)
    add_paragraph(body, "Các đoạn dưới đây sao chép nguyên văn phần AI OUTPUT trong Appendix_A_Prompt_Log.md; mỗi mục khớp với một hàng của Audit Table.")
    for artifact_no, log_no in enumerate(numbers, start=1):
        entry = entries[log_no - 1]
        header = entry.splitlines()[0]
        match = re.search(r"^\*\*AI OUTPUT:\*\*\s*\n", entry, re.M)
        assert match, log_no
        output = entry[match.end():].rsplit("\n---", 1)[0].strip("\n")
        assert output.strip(), log_no
        add_paragraph(body, f"Artifact {artifact_no:02d} — Prompt log lượt #{log_no} — {header.removeprefix('### ')}", title=True, new_page=True)
        for line in output.splitlines():
            add_paragraph(body, line)

    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with NamedTemporaryFile(dir=DOCX.parent, suffix=".docx", delete=False) as handle:
        temp = Path(handle.name)
    try:
        with zipfile.ZipFile(temp, "w") as target:
            for info in original.infolist():
                target.writestr(info, xml if info.filename == "word/document.xml" else original.read(info.filename))
        os.replace(temp, DOCX)
    finally:
        temp.unlink(missing_ok=True)

print(DOCX, "full AI outputs:", len(numbers))
