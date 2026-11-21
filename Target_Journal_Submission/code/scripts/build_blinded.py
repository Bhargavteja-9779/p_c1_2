"""Anonymised manuscript (no author names, affiliations, CRediT, funding or competing-interest statement) and a
separate title page, for double-anonymised review. Uses manuscript/build/manuscript_filled.md from
render_manuscript.py and the same pandoc/citeproc/styling route. Writes SUBMISSION/1_Manuscript_anonymised.docx/.pdf
and SUBMISSION/0_Title_Page.docx."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from scripts.build_pdf import build  # noqa: E402
from scripts.docx_style import postprocess  # noqa: E402

BUILD, OUT = TOP / "manuscript" / "build", TOP / "SUBMISSION"
TITLE = ("Covering the rare outcomes: stratified conformal prediction with size-optimal density scores "
         "for imbalanced regression")
A1, A2 = "Bhargav Teja P. N.", "Rajay Vedaraj I.S."
AFF = "Vellore Institute of Technology (VIT), India"
EMAIL = "rajay@vit.ac.in"
ORCID = {A1: "https://orcid.org/0009-0004-5378-6278", A2: "https://orcid.org/0000-0001-8445-7195"}


def anonymise(text):
    text = re.sub(r"author:\n(  - .*\n)+", "", text, count=1)
    for h in ("Declaration of competing interest", "CRediT authorship contribution statement", "Funding"):
        text = re.sub(r"\n# " + re.escape(h) + r"(?: \{-\})?\n.*?(?=\n# )", "\n", text, flags=re.S)
    return text


def title_page():
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    d = Document()
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Times New Roman", Pt(12)

    def para(txt="", bold=False, center=False, size=None, italic=False):
        p = d.add_paragraph()
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.bold, r.italic = bold, italic
        if size:
            r.font.size = Pt(size)
        return p

    para("Title page", bold=True, center=True, size=14)
    para(TITLE, bold=True, center=True, size=16)
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for txt, sup in ((A1, "a"), (", " + A2, "a,*")):
        p.add_run(txt).bold = True
        s = p.add_run(sup)
        s.font.superscript = True
    p = para(center=True)
    s = p.add_run("a")
    s.font.superscript = True
    p.add_run(" " + AFF)
    p = para(center=True)
    s = p.add_run("*")
    s.font.superscript = True
    p.add_run(f" Corresponding author: {A2}, {AFF}. E-mail: {EMAIL}")
    para("ORCID iDs", bold=True)
    for a, o in ORCID.items():
        para(f"{a}: {o}")
    para("Declaration of competing interest", bold=True)
    para("The authors declare that they have no known competing financial interests or personal relationships that "
         "could have appeared to influence the work reported in this paper.")
    para("Funding", bold=True)
    para("This research did not receive any specific grant from funding agencies in the public, commercial, or "
         "not-for-profit sectors.")
    para("CRediT authorship contribution statement", bold=True)
    p = d.add_paragraph()
    p.add_run(f"{A1}: ").bold = True
    p.add_run("Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, "
              "Visualization, Writing – original draft, Writing – review & editing.")
    p = d.add_paragraph()
    p.add_run(f"{A2}: ").bold = True
    p.add_run("Supervision, Writing – review & editing.")
    para("Data and code availability", bold=True)
    para("All datasets are publicly available on OpenML (study 353 and suites 335 and 336). The code will be made "
         "available on request.")
    cp = d.core_properties
    cp.author = cp.last_modified_by = A1
    cp.title, cp.comments = "Title page", ""
    d.save(OUT / "0_Title_Page.docx")


def main():
    OUT.mkdir(exist_ok=True)
    md = BUILD / "manuscript_anonymised.md"
    md.write_text(anonymise((BUILD / "manuscript_filled.md").read_text()))
    out = OUT / "1_Manuscript_anonymised.docx"
    subprocess.run(["pandoc", str(md), "-o", str(out), "--citeproc",
                    f"--bibliography={TOP / 'supplementary' / 'references_verified.bib'}",
                    f"--csl={BUILD / 'elsevier-harvard.csl'}", f"--reference-doc={BUILD / 'reference.docx'}",
                    "--resource-path", str(TOP), "-M", "link-citations=true"], check=True)
    postprocess(out)
    from docx import Document
    d = Document(out)
    cp = d.core_properties
    cp.author = cp.last_modified_by = ""
    cp.title, cp.comments = TITLE, ""
    d.save(out)
    build(md, OUT / "1_Manuscript_anonymised.pdf", BUILD / "manuscript_anonymised.html")
    title_page()
    print("written anonymised manuscript and title page")


if __name__ == "__main__":
    main()
