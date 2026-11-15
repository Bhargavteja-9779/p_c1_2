"""DOCX styling for the Elsevier free-format submission: Times New Roman 12 pt, 1.5 line
spacing, continuous line numbers, page numbers, compact three-rule tables, centred figures."""
from __future__ import annotations

import subprocess
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONT = "Times New Roman"


def make_reference(path: Path):
    with open(path, "wb") as fh:
        subprocess.run(["pandoc", "-o", "-", "--print-default-data-file", "reference.docx"], stdout=fh, check=True)
    d = Document(path)
    for st in d.styles:
        try:
            if st.font is not None:
                st.font.name = FONT
                st.font.color.rgb = RGBColor(0, 0, 0)
                rpr = st.element.get_or_add_rPr()
                rf = rpr.find(qn("w:rFonts"))
                if rf is None:
                    rf = OxmlElement("w:rFonts")
                    rpr.append(rf)
                for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                    rf.set(qn(a), FONT)
        except (AttributeError, ValueError):
            pass
    sizes = {"Normal": 12, "Body Text": 12, "First Paragraph": 12, "Compact": 10, "Title": 16, "Subtitle": 12,
             "Heading 1": 13, "Heading 2": 12, "Heading 3": 12, "Abstract": 11, "Bibliography": 10,
             "Image Caption": 10, "Table Caption": 10, "Block Text": 11, "Author": 12, "Date": 12}
    for name, sz in sizes.items():
        try:
            st = d.styles[name]
        except KeyError:
            continue
        st.font.size = Pt(sz)
        pf = st.paragraph_format
        if name.startswith("Heading") or name in ("Title",):
            st.font.bold = True
            st.font.italic = name == "Heading 3"
            pf.space_before, pf.space_after = Pt(12), Pt(6)
        elif name in ("Body Text", "First Paragraph", "Normal", "Abstract", "Block Text"):
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
            pf.space_after = Pt(6)
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for sec in d.sections:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(2.5)
        sec.top_margin = sec.bottom_margin = Cm(2.5)
    d.save(path)


def _page_number_footer(section):
    p = section.footer.paragraphs[0] if section.footer.paragraphs else section.footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)


def _line_numbers(section):
    sp = section._sectPr
    ln = OxmlElement("w:lnNumType")
    ln.set(qn("w:countBy"), "1")
    ln.set(qn("w:restart"), "continuous")
    ln.set(qn("w:distance"), "283")
    sp.append(ln)


def _borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge, val in (("top", "single"), ("bottom", "single"), ("insideH", "nil"), ("insideV", "nil"),
                      ("left", "nil"), ("right", "nil")):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), val)
        e.set(qn("w:sz"), "8")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)
    # rule under header row
    for cell in table.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tb = OxmlElement("w:tcBorders")
        bt = OxmlElement("w:bottom")
        for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "0"), ("w:color", "000000")):
            bt.set(qn(k), v)
        tb.append(bt)
        tcPr.append(tb)


def postprocess(path: Path):
    d = Document(path)
    for sec in d.sections:
        _page_number_footer(sec)
        _line_numbers(sec)
    for t in d.tables:
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        _borders(t)
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        r.font.size = Pt(8)
                        r.font.name = FONT
        for cell in t.rows[0].cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.bold = True
    for p in d.paragraphs:
        if p.style.name in ("Captioned Figure", "Figure"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.style.name == "Image Caption":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    d.save(path)
