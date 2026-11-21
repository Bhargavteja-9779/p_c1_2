"""Build the anonymised code package for double-blind review (review round 9, issue 5).

The package contains code/, the configurations, both analysis plans, the final-version per-run results, tables and
figures, but no version-control metadata (remote, branch names, commit messages). Because the plans' commit
identifiers are cited in the manuscript, PLAN_TIMESTAMPS.md lists, for each plan, the commit identifier, its commit
time and the SHA-256 of the plan file at that commit, so that the full history can be checked against them when it is
made public after review. In packaged text files, "PREREGISTRATION_" is renamed "ANALYSIS_PLAN_" (consistently, so
the scripts still run), internal review labels are neutralised and absolute local paths are removed; the build then
scans the package for identifying strings and fails if any remain.
Output: ../submission_package/anonymous_code_package.zip (not version-controlled).
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

TOP = Path(__file__).resolve().parents[2]
OUT = TOP.parent / "submission_package" / "anonymous_code_package.zip"
PLANS = {"PREREGISTRATION_confirmatory.md": "ccba99b", "PREREGISTRATION_relevance_weighted.md": "a9f31d2"}
RESULTS = ["raw_eval_v3", "raw_mlp_v3", "raw_denseweight", "raw_grouped", "raw_temporal", "raw_tail1", "rw",
           "confirmatory/raw_eval_v3", "confirmatory/statistics_confirmatory.json", "confirmatory/tables",
           "synthetic_v3.jsonl", "tail_alerts.jsonl", "raw_results_v3.csv.gz"]
SKIP_CODE = {"review_cycle_workflow.js", "build_anonymous_package.py"}
TEXT = {".py", ".md", ".json", ".txt", ".yml", ".yaml", ".sh", ".csv", ".jsonl", ".js", ".cfg", ".toml"}
FORBIDDEN = [r"/home/", r"claude", r"anthropic", r"github\.com", r"bhargav", r"Expert Systems with Applications",
             r"\bESWA\b"]


def sanitise(name: str, data: bytes) -> bytes:
    if Path(name).suffix not in TEXT:
        return data
    t = data.decode("utf-8", errors="replace")
    t = t.replace("PREREGISTRATION_", "ANALYSIS_PLAN_")
    t = re.sub(r"\(branch `[^`]*`\)", "[branch name redacted for double-blind review]", t)
    t = re.sub(r"[Rr]eview (?:round|cycle) ?\d+[a-z]?", "internal check", t)
    t = re.sub(r"\bC1-\d+(?:\([a-z0-9]+\))?", "internal check", t)
    t = re.sub(r"(?:[A-Za-z]:)?/(?:home|Users|root|tmp|mnt)/[^\s\"'<>]*/", "", t)
    return t.encode("utf-8")


def arcname(p: Path) -> str:
    return str(p.relative_to(TOP)).replace("PREREGISTRATION_", "ANALYSIS_PLAN_")


def files():
    for p in sorted((TOP / "code").rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.name not in SKIP_CODE and not p.name.endswith(".pyc"):
            yield p
    for name in PLANS:
        yield TOP / name
    for r in RESULTS:
        q = TOP / "results" / r
        if q.is_file():
            yield q
        elif q.is_dir():
            yield from (x for x in sorted(q.rglob("*")) if x.is_file())
    for p in sorted((TOP / "results").glob("*.json")):
        yield p
    for d in ("tables", "figures"):
        yield from (x for x in sorted((TOP / d).rglob("*")) if x.is_file())


def timestamps() -> str:
    rows = ["# Commit time stamps of the analysis plans", "",
            "The manuscript cites the commits that added the two analysis plans. The version history itself is "
            "withheld during double-blind review and will be made public upon acceptance. For each plan the table "
            "gives the commit identifier, the commit time (UTC) and the SHA-256 of the plan file as committed; the "
            "packaged plan files (renamed ANALYSIS_PLAN_*) are byte-identical to the committed versions apart from "
            "the renaming of file references and the redaction of one branch name.", "", "| Plan | Commit | Commit time | SHA-256 at commit |", "|---|---|---|---|"]
    for name, commit in PLANS.items():
        when = subprocess.run(["git", "log", "-1", "--format=%cd", "--date=iso-strict", commit], cwd=TOP,
                              capture_output=True, text=True, check=True).stdout.strip()
        blob = subprocess.run(["git", "show", f"{commit}:Target_Journal_Submission/{name}"], cwd=TOP,
                              capture_output=True, check=True).stdout
        rows.append(f"| {name.replace('PREREGISTRATION_', 'ANALYSIS_PLAN_')} | {commit} | {when} | "
                    f"{hashlib.sha256(blob).hexdigest()} |")
    return "\n".join(rows) + "\n"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    bad, n = [], 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("PLAN_TIMESTAMPS.md", timestamps())
        for p in files():
            data = sanitise(p.name, p.read_bytes())
            name = arcname(p)
            if Path(name).suffix in TEXT:
                low = data.decode("utf-8", errors="replace")
                for pat in FORBIDDEN:
                    if re.search(pat, low, re.I) or re.search(pat, name, re.I):
                        bad.append((name, pat))
            z.writestr(name, data)
            n += 1
    print(f"{n} files -> {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")
    if bad:
        for b in bad[:40]:
            print("IDENTIFYING STRING:", b)
        sys.exit(f"{len(bad)} identifying strings found")


if __name__ == "__main__":
    main()
