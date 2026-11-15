"""Figures that are not aggregates of the benchmark files:
F1  Proposition 1 curves (from results/prop1_gaussian.json)
F0  Method schematic (workflow diagram, no data)
F9  Example prediction sets on a real dataset (fresh run, seed 0, same pipeline)
F10 Synthetic oracle study (from results/synthetic.jsonl)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from scripts.analyze import BLUE, ORANGE, AQUA, GRAY, DARK, save, FIG, TAB, table  # noqa: E402


def f1():
    r = json.loads((TOP / "results" / "prop1_gaussian.json").read_text())
    c = r["curve"]
    y = np.array(c["y"])
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    cols = {"0.3": ORANGE, "0.5": "#e87ba4", "0.7": AQUA, "0.9": BLUE}
    for k, col in cols.items():
        ax.plot(y, c[k], color=col, label=f"$R^2$ = {k}")
    ax.axhline(0.9, color="#0b0b0b", lw=0.8)
    ax.text(-3.55, 0.925, "1−α = X-conditional\ncoverage of $C^*$", fontsize=6.5, va="bottom")
    ax.set_xlabel("Standardised target value y")
    ax.set_ylabel(r"$P(Y \in C^*(X) \mid Y=y)$")
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=7, loc="lower center")
    save(fig, "F1_prop1_oracle_target_conditional")
    rows = [{"R2": x["R2"], "upper10_analytic": x["analytic_upper10"], "upper10_MC": x["mc"]["upper10"],
             "upper1_analytic": x["analytic_upper1"], "central80_analytic": x["analytic_central80"],
             "marginal_MC": x["mc"]["marginal"]} for x in r["rows"]]
    table(pd.DataFrame(rows), "T0_prop1_gaussian", 4)


def f0():
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    ax.set_axis_off()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 36)
    boxes = [
        (1, 20, 17, 12, "Proper training set\n(50%)", "#dce9f8"),
        (22, 20, 19, 12, "Fit $\\hat\\mu(x)$, $\\hat\\sigma(x)$ (OOF),\nKDE $\\hat g$ of standardised\nresiduals $\\rightarrow \\hat f(y\\mid x)$", "#dce9f8"),
        (45, 20, 17, 12, "Target strata $B_1,\\ldots,B_K$\nfrom training\nquantiles of $Y$", "#dce9f8"),
        (1, 3, 17, 12, "Calibration set\n(25%)", "#fde3d8"),
        (22, 3, 19, 12, "Scores $s_i=-\\hat f(y_i\\mid x_i)$\ngrouped by stratum\nof $y_i$", "#fde3d8"),
        (45, 3, 17, 12, "Per-stratum conformal\nquantile $\\hat q_k$\n(level $1-\\alpha_k$)", "#fde3d8"),
        (67, 11, 31, 14, "Prediction set for a new $x$:\n$C(x)=\\bigcup_k\\{y\\in B_k:\\hat f(y\\mid x)\\geq -\\hat q_k\\}$\n"
                         "$P(Y\\in C(X)\\mid Y\\in B_k)\\geq 1-\\alpha_k$ (finite sample)", "#d9f2e9"),
    ]
    for x, y, w, h, t, c in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    fc=c, ec="#8a8984", lw=0.6))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=6.6)
    for (x1, y1, x2, y2) in [(18.5, 26, 21.5, 26), (41.5, 26, 44.5, 26), (18.5, 9, 21.5, 9),
                             (41.5, 9, 44.5, 9), (31.5, 19.5, 31.5, 15.5), (53.5, 19.5, 53.5, 15.5),
                             (62.5, 9, 66.5, 15), (62.5, 26, 66.5, 21)]:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7,
                                     color=DARK, lw=0.8))
    save(fig, "F0_method_schematic")


def f9(did=44977, seed=0, n_show=70):
    from experiments.run_benchmark import fit_context, run_methods
    from src.data.openml_ctr23 import load
    X, y, meta = load(did)
    ctx, part, _ = fit_context(X, y, seed, [0.1], 200, 4, 40)
    sets = run_methods(ctx, 0.1, part, which="all")
    yt = ctx["yt"]
    rng = np.random.default_rng(1)
    st = part.stratum(yt)
    # show a stratified random sample with over-representation of the two tail strata
    idx = np.concatenate([rng.choice(np.where(st == k)[0], n_show // part.K, replace=False)
                          for k in range(part.K)])
    idx = idx[np.argsort(yt[idx])]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True)
    scale = 1e3
    for ax, m, col in zip(axs, ["CQR", "HPD-split-LS", "SDLC-LS"], [ORANGE, DARK, BLUE]):
        S = sets[m]
        for j, i in enumerate(idx):
            if S[0] == "int":
                for lo, hi in zip(S[1][i], S[2][i]):
                    if hi > lo:
                        ax.plot([j, j], [lo / scale, hi / scale], color=col, lw=1.2, alpha=0.8)
            else:
                m_ = S[1][i]
                e = part.fine_edges
                runs = np.flatnonzero(np.diff(np.r_[0, m_.astype(int), 0]))
                for a, b in zip(runs[::2], runs[1::2]):
                    ax.plot([j, j], [e[a] / scale, e[b] / scale], color=col, lw=1.2, alpha=0.8)
        cov = [None] * len(idx)
        from src.evaluation.metrics import covered
        c = covered(S, yt, part)[idx]
        ax.scatter(np.arange(len(idx))[c], yt[idx][c] / scale, s=5, color="#0b0b0b", zorder=3)
        ax.scatter(np.arange(len(idx))[~c], yt[idx][~c] / scale, s=12, marker="x", color="#e34948", zorder=4)
        for e_ in part.strata_inner:
            ax.axhline(e_ / scale, color="#c3c2b7", lw=0.6, ls="--")
        nm = {"CQR": "CQR", "HPD-split-LS": "HPD-split", "SDLC-LS": "SDLC (proposed)"}[m]
        ax.set_title(f"{nm}: {int((~c).sum())} misses", fontsize=8)
        ax.set_xlabel("Test points sorted by true target")
        ax.set_xticks([])
    axs[0].set_ylabel(f"{meta['target']} (×1000)")
    save(fig, "F9_example_sets_california")


def f10():
    p = TOP / "results" / "synthetic.jsonl"
    if not p.exists():
        return
    d = pd.read_json(p, lines=True)
    cc = [c for c in d.columns if c.startswith("cal_cov_")]
    g = d.groupby(["scores", "method"])
    t = g[["coverage", "size", "components"]].mean()
    prof = g[cc].mean()
    t["worst_stratum"] = prof.min(axis=1)
    t["lower_tail"] = prof["cal_cov_0"]
    t["upper_tail"] = prof[f"cal_cov_{len(cc) - 1}"]
    t["size_sd"] = g["size"].std()
    t = t.reset_index().sort_values(["scores", "size"])
    table(t, "T11_synthetic_oracle", 4)


if __name__ == "__main__":
    which = sys.argv[1:] or ["f0", "f1", "f9", "f10"]
    for w in which:
        globals()[w]()
        print(w, "done")
