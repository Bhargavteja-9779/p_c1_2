"""Remove local file-system paths from the DOCX deliverables (review round 9, issue 5): image descriptions and
custom document properties written by pandoc contain absolute paths of the build machine. Every directory prefix
of an absolute path is removed, leaving the file name only. Run after every build; idempotent."""
import re
import sys
import zipfile
from pathlib import Path

MS = Path(__file__).resolve().parents[2] / "manuscript"
PAT = re.compile(rb"(?:[A-Za-z]:)?/(?:home|Users|root|tmp|mnt)/[^\"<>\s]*/")


def clean(path: Path) -> int:
    tmp = path.with_suffix(".tmp.docx")
    n = 0
    with zipfile.ZipFile(path) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            data = zi.read(item.filename)
            if item.filename.endswith((".xml", ".rels")):
                data, k = PAT.subn(b"", data)
                n += k
            zo.writestr(item, data)
    tmp.replace(path)
    return n


if __name__ == "__main__":
    files = [Path(a) for a in sys.argv[1:]] or sorted(MS.glob("*.docx"))
    for f in files:
        print(f.name, "paths removed:", clean(f))
