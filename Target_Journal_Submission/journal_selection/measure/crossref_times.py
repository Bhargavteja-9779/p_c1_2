"""Median received->accepted interval from Crossref assertion dates (2026 publications).
Usage: python crossref_times.py ISSN [ISSN ...]; prints JSON lines."""
import json, sys, statistics, urllib.request, urllib.parse, datetime, re, time

def parse(s):
    for fmt in ("%d %B %Y", "%d %b %Y", "%Y-%m-%d", "%B %d, %Y", "%d/%m/%Y"):
        try: return datetime.datetime.strptime(s.strip(), fmt).date()
        except Exception: pass
    return None

def measure(issn, n=400):
    url = ("https://api.crossref.org/journals/%s/works?rows=%d&filter=from-pub-date:2026-01-01,type:journal-article"
           "&select=DOI,assertion,container-title&mailto=" % (issn, n))
    url = url.replace("&mailto=", "")
    with urllib.request.urlopen(url, timeout=60) as r:
        items = json.load(r)["message"]["items"]
    d, name = [], None
    for it in items:
        name = name or (it.get("container-title") or [None])[0]
        a = {x.get("name"): x.get("value") for x in it.get("assertion", []) if isinstance(x, dict)}
        rec = a.get("received"); acc = a.get("accepted")
        if rec and acc:
            r_, c_ = parse(rec), parse(acc)
            if r_ and c_ and c_ >= r_: d.append((c_ - r_).days)
    out = {"issn": issn, "journal": name, "n_items": len(items), "n_dated": len(d)}
    if d:
        d.sort()
        out.update(median=statistics.median(d), q25=d[len(d)//4], q75=d[3*len(d)//4],
                   pct_le_72=round(100*sum(x<=72 for x in d)/len(d),1))
    return out

for issn in sys.argv[1:]:
    for k in range(4):
        try: print(json.dumps(measure(issn)), flush=True); break
        except Exception as e:
            if "429" in str(e) and k<3: time.sleep(10*(k+1)); continue
            print(json.dumps({"issn": issn, "error": str(e)}), flush=True); break
    time.sleep(1)
