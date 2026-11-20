"""All 2026 JKSU-CIS articles (cursor paging): received->accepted, received->first published."""
import json, urllib.request, urllib.parse, statistics, datetime, csv
from crossref_times import parse
cur, rows = "*", []
while True:
    u = ("https://api.crossref.org/journals/1319-1578/works?rows=500&cursor=%s&filter=from-pub-date:2026-01-01,type:journal-article"
         "&select=DOI,title,assertion,published" % urllib.parse.quote(cur))
    m = json.load(urllib.request.urlopen(u, timeout=90))["message"]
    if not m["items"]: break
    for it in m["items"]:
        a = {x.get("name"): x.get("value") for x in it.get("assertion", [])}
        r, c = parse(a.get("received","") or "x"), parse(a.get("accepted","") or "x")
        rv = a.get("revised")
        rows.append(dict(doi=it["DOI"], title=(it.get("title") or [""])[0][:120], received=r, accepted=c,
                         days=(c-r).days if r and c else None))
    cur = m["next-cursor"]
import urllib.parse
d = sorted(x["days"] for x in rows if x["days"] is not None and x["days"] >= 0)
q = statistics.quantiles(d, n=4)
print(dict(n=len(rows), n_dated=len(d), median=statistics.median(d), q1=q[0], q3=q[2], mean=round(statistics.mean(d),1),
           pct_le_60=round(100*sum(x<=60 for x in d)/len(d),1), pct_le_72=round(100*sum(x<=72 for x in d)/len(d),1)))
with open("jksu_cis_2026.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
