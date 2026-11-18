"""Build manuscript/Final_Manuscript.pdf from the filled manuscript source.

Route: pandoc (citeproc, Elsevier Harvard CSL, MathML) -> standalone HTML with embedded figures ->
headless Chromium (Playwright) print to A4 PDF. MathML is rendered natively by Chromium, which avoids
the equation-glyph limitations of converting the DOCX with LibreOffice. The DOCX remains the
submission file; the PDF is a convenience copy with identical content.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
MS = TOP / "manuscript"
BUILD = MS / "build"

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm; }
body { font-family: 'Times New Roman', 'Liberation Serif', serif; font-size: 11pt; line-height: 1.45;
       color: #000; max-width: none; margin: 0; }
h1.title { font-size: 17pt; text-align: center; margin: 0 0 8pt 0; line-height: 1.25; }
p.author { text-align: center; margin: 2pt 0; font-size: 10.5pt; }
div.abstract { margin: 12pt 6% 8pt 6%; font-size: 10.5pt; text-align: justify; }
div.abstract-title { font-weight: bold; text-align: center; margin-bottom: 4pt; }
h1 { font-size: 13pt; margin: 16pt 0 6pt 0; } h2 { font-size: 11.5pt; margin: 12pt 0 4pt 0; }
h3 { font-size: 11pt; font-style: italic; }
p { text-align: justify; margin: 0 0 6pt 0; }
table { border-collapse: collapse; margin: 6pt auto 12pt auto; font-size: 8.3pt; border-top: 1.2px solid #000;
        border-bottom: 1.2px solid #000; page-break-inside: avoid; }
th { border-bottom: 0.8px solid #000; padding: 2pt 5pt; text-align: right; }
td { padding: 1.5pt 5pt; text-align: right; }
th:first-child, td:first-child { text-align: left; }
figure { margin: 10pt 0; page-break-inside: avoid; text-align: center; }
figure img { max-width: 100%; }
figcaption { font-size: 9.5pt; text-align: justify; margin-top: 4pt; }
blockquote { margin: 8pt 4%; padding: 4pt 8pt; border-left: 2px solid #888; font-size: 10pt; }
div.csl-entry { font-size: 9.5pt; margin-bottom: 3pt; padding-left: 1.5em; text-indent: -1.5em; }
math { font-size: 1.02em; }
"""


def main():
    md = BUILD / "manuscript_filled.md"
    if not md.exists():
        sys.exit("run scripts/render_manuscript.py first")
    build(md, MS / "Final_Manuscript.pdf", BUILD / "manuscript.html")


def build(md, out_pdf, html):
    css = BUILD / "pdf.css"
    css.write_text(CSS)
    subprocess.run(["pandoc", str(md), "-s", "--citeproc", "--mathml", "--embed-resources",
                    f"--bibliography={TOP / 'supplementary' / 'references_verified.bib'}",
                    f"--csl={BUILD / 'elsevier-harvard.csl'}", f"--css={css}", "--resource-path", str(TOP),
                    "-M", "link-citations=true", "-o", str(html)], check=True)
    js = BUILD / "print_pdf.js"
    js.write_text("""
const { chromium } = require('playwright');
(async () => {
  const [html, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: "<div style='font-size:8pt;width:100%;text-align:center'><span class='pageNumber'></span></div>",
    margin: { top: '20mm', bottom: '20mm', left: '18mm', right: '18mm' } });
  await browser.close();
})();
""")
    subprocess.run(["node", str(js), str(html), str(out_pdf)], check=True,
                   env={**__import__("os").environ, "NODE_PATH": "/opt/node22/lib/node_modules"})
    print("written", out_pdf)


if __name__ == "__main__":
    main()
