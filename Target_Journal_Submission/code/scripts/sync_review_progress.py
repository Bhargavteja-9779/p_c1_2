"""Copy the progress of a running review-cycle workflow into the repository so that a later session
(possibly another account) can continue: journal (which reviewers started/finished, with their results)
and, per reviewer, the final structured review or the last partial assistant text.
Usage: python3 sync_review_progress.py <workflow_transcript_dir> <cycle>"""
import json, sys
from pathlib import Path

src, cycle = Path(sys.argv[1]), int(sys.argv[2])
out = Path(__file__).resolve().parents[2] / "REVIEW" / f"cycle{cycle:02d}_progress"
out.mkdir(parents=True, exist_ok=True)
jr = src / "journal.jsonl"
if jr.exists():
    (out / "journal.jsonl").write_text(jr.read_text())
status = {}
for line in (jr.read_text().splitlines() if jr.exists() else []):
    try:
        e = json.loads(line)
    except Exception:
        continue
    if e.get("label"):
        status[e["agentId"]] = {"label": e["label"], "state": e["type"]}
    elif e.get("agentId") in status:
        status[e["agentId"]]["state"] = e["type"]
for f in src.glob("agent-*.jsonl"):
    aid = f.stem.replace("agent-", "")
    meta = json.loads((src / f"agent-{aid}.meta.json").read_text()) if (src / f"agent-{aid}.meta.json").exists() else {}
    label = meta.get("description", aid).replace(":", "_")
    last_text, structured = None, None
    for line in f.read_text().splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        msg = e.get("message") or {}
        if msg.get("role") != "assistant":
            continue
        for c in msg.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "text" and c.get("text", "").strip():
                last_text = c["text"]
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in ("StructuredOutput", "structured_output", "return_result"):
                structured = c.get("input")
    if structured is not None:
        (out / f"{label}.json").write_text(json.dumps(structured, indent=1))
    elif last_text:
        (out / f"{label}.partial.md").write_text(last_text)
(out / "STATUS.md").write_text(
    f"# Review cycle {cycle} progress (auto-synced)\n\nFinished reviews are `<label>.json`; `.partial.md` = reviewer "
    "still running or interrupted (re-run that reviewer). To continue in a new session: run "
    f"code/scripts/review_cycle_workflow.js with args {{cycle: {cycle}}} for the reviewers WITHOUT a .json file only "
    "(edit REVIEWERS), then consolidate all JSON reviews into REVIEW/review_%02d.md.\n\n" % cycle
    + "\n".join(f"* {v['label']}: {v['state']}" for v in status.values()) + "\n")
