"""Assemble the submission package in SUBMISSION/ (manuscript, supplement, highlights, cover letter, figures)
and set the document metadata (author) of every DOCX file."""
import shutil
from pathlib import Path

from docx import Document

TOP = Path(__file__).resolve().parents[2]
MS, FIG, OUT = TOP / "manuscript", TOP / "figures", TOP / "SUBMISSION"
AUTHOR = "P N Bhargav Teja"
TITLE = ("Covering the rare outcomes: stratified conformal prediction with size-optimal density scores "
         "for imbalanced regression")
FILES = {"Final_Manuscript.docx": "1_Manuscript.docx", "Final_Manuscript.pdf": "1_Manuscript.pdf",
         "highlights.docx": "2_Highlights.docx", "cover_letter.docx": "3_Cover_Letter.docx",
         "Supplementary_Material.docx": "4_Supplementary_Material.docx",
         "Supplementary_Material.pdf": "4_Supplementary_Material.pdf"}


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "figures").mkdir(parents=True)
    for src, dst in FILES.items():
        shutil.copy2(MS / src, OUT / dst)
        if dst.endswith(".docx"):
            d = Document(OUT / dst)
            cp = d.core_properties
            cp.author, cp.last_modified_by = AUTHOR, AUTHOR
            cp.title = TITLE if "Manuscript" in dst or "Supplementary" in dst else dst[2:-5].replace("_", " ")
            cp.comments, cp.keywords, cp.subject = "", "", ""
            d.save(OUT / dst)
    text = (MS / "build" / "manuscript_filled.md").read_text()
    for f in sorted(FIG.glob("F*.p*")):
        if f.with_suffix(".png").name in text or f.stem in text:
            shutil.copy2(f, OUT / "figures" / f.name)
    print("written", sorted(p.name for p in OUT.rglob("*") if p.is_file()))


if __name__ == "__main__":
    main()
