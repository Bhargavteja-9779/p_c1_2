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

import matplotlib.patheffects as pe
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from scripts.analyze import BLUE, ORANGE, AQUA, GRAY, DARK, save, FIG, TAB, table  # noqa: E402,F401


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
    """Fig. 1: (a) illustration of an SDLC set for one input (synthetic density, not data); (b) workflow of SDLC
    and RW-DLC with the training / calibration / test split."""
    from scipy import stats as st
    fig = plt.figure(figsize=(7.4, 6.9))
    # ---------------------------------------------------------------- (a) stratified density level set
    ax = fig.add_axes([0.07, 0.645, 0.90, 0.31])
    y = np.linspace(0, 10, 2001)
    f = st.gamma(a=3.0, scale=1.0).pdf(y)
    e = [0.9, 1.6, 3.8, 5.6]                                  # cut points e_1..e_4 (illustrative)
    thr = [0.060, 0.090, 0.150, 0.110, 0.012]               # -q_k per stratum (illustrative)
    lo_, hi_ = [0.0] + e, e + [10.0]
    ax.plot(y, f, color="#0b0b0b", lw=1.3)
    ax.text(2.2, f.max() * 1.02, r"$\hat f(y\mid x)$", fontsize=8, ha="left", va="bottom")
    for k in range(5):
        m = (y >= lo_[k]) & (y <= hi_[k])
        ax.hlines(thr[k], lo_[k], hi_[k], color="#d62728", lw=1.2)
        inside = m & (f >= thr[k])
        ax.fill_between(y, 0, f, where=inside, color=BLUE, alpha=0.22, lw=0)
        ax.text((lo_[k] + hi_[k]) / 2, f.max() * 1.18, f"$B_{k + 1}$", ha="center", fontsize=8)
        ax.text(lo_[k] + 0.05 if k < 4 else 9.9, thr[k] + 0.006, rf"$-\hat q_{k + 1}$",
                ha="left" if k < 4 else "right", va="bottom", fontsize=7, color="#d62728")
    for c_ in e:
        ax.axvline(c_, color="#8a8984", lw=0.7, ls="--")
    # the resulting set: union of pieces, drawn below the axis
    ins = np.zeros_like(y, bool)
    for k in range(5):
        ins |= (y >= lo_[k]) & (y < hi_[k]) & (f >= thr[k])
    d = np.diff(ins.astype(int))
    starts, ends = list(y[1:][d == 1]), list(y[1:][d == -1])
    if ins[0]:
        starts = [y[0]] + starts
    if ins[-1]:
        ends = ends + [y[-1]]
    for s_, e_ in zip(starts, ends):
        ax.plot([s_, e_], [-0.035, -0.035], color=BLUE, lw=4, solid_capstyle="butt")
    ax.text(10.0, -0.035, r"$\hat C(x)$", color=BLUE, fontsize=8, va="center", ha="right")
    ax.set_ylim(-0.06, f.max() * 1.32)
    ax.set_xlim(0, 10)
    ax.set_xlabel("Candidate target value y")
    ax.set_ylabel("Estimated density")
    ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(False)
    ax.set_title("(a) SDLC set for one input x: one threshold per target stratum gives a union of pieces",
                 fontsize=8.5, loc="left")
    # ---------------------------------------------------------------- (b) workflow
    bx = fig.add_axes([0.0, 0.075, 1.0, 0.52])
    bx.set_axis_off()
    bx.set_xlim(0, 100)
    bx.set_ylim(0, 62)
    bx.text(1, 60, "(b) Workflow", fontsize=8.5, va="top")
    TR, CA, TE, OUT = "#dce9f8", "#fde3d8", "#ececec", "#d9f2e9"

    def box(x, y_, w, h, txt, c, fs=6.8):
        bx.add_patch(FancyBboxPatch((x, y_), w, h, boxstyle="round,pad=0.3,rounding_size=1.0", fc=c, ec="#8a8984",
                                    lw=0.6))
        lines = txt.split("\n")                 # one text object per line: mathtext accents (hats) stay in place
        lh = 0.47 * fs
        for i, ln in enumerate(lines):
            bx.text(x + w / 2, y_ + h / 2 + ((len(lines) - 1) / 2 - i) * lh, ln, ha="center", va="center", fontsize=fs)

    def arrow(x1, y1, x2, y2, over=False):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7, color=DARK, lw=0.8, zorder=3)
        if over:                                  # drawn over a crossing arrow with a white outline (bridge)
            a.set_path_effects([pe.Stroke(linewidth=3.2, foreground="white"), pe.Normal()])
            a.set_zorder(4)
        bx.add_patch(a)
    # training row
    box(1, 44, 15, 10, "Proper training\nset (50%)", TR)
    box(20, 44, 25, 10, "Density model: mean $\\hat\\mu(x)$, scale $\\hat\\sigma(x)$,\nnoise density $\\hat g$"
        " $\\rightarrow$ $\\hat f(y\\mid x)$ (Eq. 7)", TR)
    box(49, 44, 21, 10, "Target strata $B_1,\\ldots,B_K$\nfrom training quantiles", TR)
    box(74, 44, 25, 10, "Relevance $\\phi(y)$ from the\ntraining targets (RW-DLC only)", TR)
    arrow(16.5, 49, 19.5, 49)
    # calibration rows
    box(1, 22, 15, 10, "Calibration\nset (25%)", CA)
    box(20, 22, 25, 10, "Scores at the observed targets\nSDLC: $S_i=-\\hat f(Y_i\\mid X_i)$\n"
        "RW-DLC: $S_i=-\\phi(Y_i)\\hat f(Y_i\\mid X_i)$", CA)
    box(49, 28, 21, 9, "SDLC: group by stratum of $Y_i$;\nthreshold $\\hat q_k$ per stratum", CA)
    box(49, 16, 21, 9, "RW-DLC: weight by $\\phi(Y_i)$;\nweighted threshold $q(y)$", CA)
    box(74, 28, 25, 9, "$\\hat C(x)=\\cup_k\\{y\\in B_k:\\ \\hat f(y\\mid x)\\geq{-\\hat q_k}\\}$\n"
        "coverage $\\geq 1-\\alpha_k$ in every stratum", OUT, 6.6)
    box(74, 16, 25, 9, "$\\hat C_\\phi(x)=\\{y:\\ \\phi(y)\\hat f(y\\mid x)\\geq{-q(y)}\\}$\n"
        "relevance-weighted coverage $\\geq 1-\\alpha$", OUT, 6.6)
    arrow(16.5, 27, 19.5, 27)
    arrow(45.5, 28.5, 48.5, 32)
    arrow(45.5, 25.5, 48.5, 20.5)
    arrow(70.5, 32.5, 73.5, 32.5, over=True)
    arrow(70.5, 20.5, 73.5, 20.5)
    arrow(32.5, 43.5, 32.5, 32.5)        # density model -> scores
    arrow(59.5, 43.5, 59.5, 37.5)        # strata -> SDLC
    arrow(75.5, 43.5, 70.5, 24.0)        # relevance -> RW-DLC
    # test row
    box(1, 3, 15, 9, "Test set (25%)", TE)
    box(20, 3, 79, 9, "Evaluation only: coverage (marginal, per stratum, relevance-weighted, top 1%), "
        "set size and tail alerts of both sets", TE)
    arrow(16.5, 7.5, 19.5, 7.5)
    fig.text(0.01, 0.008, "Abbreviations: SDLC, stratified density-level conformal prediction; RW-DLC, relevance-weighted "
             "density-level conformal prediction;\n$\\hat q_k$, conformal threshold of stratum $k$ (Eq. 3); $q(y)$, "
             "relevance-weighted threshold (Eq. 10). The scale model $\\hat\\sigma$ is fitted to three-fold out-of-fold "
             "residuals of $\\hat\\mu$,\nand $\\hat g$ is a kernel density estimate of the cross-fitted standardised "
             "residuals. Panel (a) is an illustration, not data.",
             fontsize=6.4, va="bottom", linespacing=1.5)
    fig.savefig(FIG / "F0_method_schematic.png", dpi=300)
    fig.savefig(FIG / "F0_method_schematic.pdf")
    plt.close(fig)


def f9(did=44977, seed=0, n_show=70):
    """Example prediction sets for test points of one dataset, built from the cached model outputs with
    exactly the v3 code used for the benchmark evaluation (stratum-exact location-scale sets)."""
    from experiments.evaluate_from_cache3 import CACHE, CACHE3, all_sets, build_context
    from experiments.run_benchmark import CFG
    from src.data.openml_ctr23 import load
    from src.evaluation.metrics import covered
    from src.methods import ls_exact3 as L3
    from src.methods.conformal import conformal_quantile
    from src.methods.strata import make_partition
    c, c3 = dict(np.load(CACHE / f"{did}_{seed}.npz")), dict(np.load(CACHE3 / f"{did}_{seed}.npz"))
    meta = load(did)[2]
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    ctx, tables, scales = build_context(c, c3, part, CFG["alphas"])
    sets = all_sets(ctx, tables, scales, 0.1, part, which="all", only={"CQR", "S-Res", "S-NCP"})
    yt, yc = ctx["yt"], ctx["yc"]
    T = tables["LS"]
    sc_c = L3.scores("density", T, yc, ctx["mu_c"], ctx["sg_c"], ctx["sg_c"], part)
    sc_t = L3.scores("density", T, yt, ctx["mu_t"], ctx["sg_t"], ctx["sg_t"], part)
    st_c = part.stratum(yc)
    q = np.array([conformal_quantile(sc_c[st_c == k], 0.1) for k in range(part.K)])
    S_sdlc, iv = L3.build_sets("density", T, ctx["mu_t"], ctx["sg_t"], ctx["sg_t"], q, part, yt, sc_t,
                               return_intervals=True)
    rng = np.random.default_rng(1)
    st = part.stratum(yt)
    idx = np.concatenate([rng.choice(np.where(st == k)[0], n_show // part.K, replace=False)
                          for k in range(part.K)])
    idx = idx[np.argsort(yt[idx])]
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 3.0), sharey=True)
    scale = 1e3
    from scripts.analyze3 import mcolor
    names = {"CQR": "CQR", "S-Res": "BCCP", "S-NCP": "S-NCP", "SDLC-LS": "SDLC"}
    for ax, m in zip(axs, ["CQR", "S-Res", "S-NCP", "SDLC-LS"]):
        col = mcolor(names[m])
        if m == "SDLC-LS":
            pieces = [iv[i] for i in idx]
            cv = S_sdlc[6][idx]
        else:
            S = sets[m]
            pieces = [list(zip(S[1][i], S[2][i])) for i in idx]
            cv = covered(S, yt, part)[idx]
        for j, pc in enumerate(pieces):
            for lo, hi in pc:
                if np.isfinite(lo) and np.isfinite(hi) and hi > lo:
                    ax.plot([j, j], [lo / scale, hi / scale], color=col, lw=1.0, alpha=0.85)
        ax.scatter(np.arange(len(idx))[cv], yt[idx][cv] / scale, s=4, color="#0b0b0b", zorder=3)
        ax.scatter(np.arange(len(idx))[~cv], yt[idx][~cv] / scale, s=12, marker="x", color="#e34948", zorder=4)
        for e_ in part.strata_inner:
            ax.axhline(e_ / scale, color="#c3c2b7", lw=0.6, ls="--")
        ax.set_title(f"{names[m]}: {int((~cv).sum())} of {len(idx)} missed", fontsize=7.5)
        ax.set_xlabel("Test points (sorted by y)", fontsize=7)
        ax.set_xticks([])
    label = {"medianHouseValue": "Median house value (thousand USD)"}
    axs[0].set_ylabel(label.get(meta["target"], f"{meta['target']} (thousands)"))
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


def light(with_raw=True):
    """Redraw the benchmark figures from the saved per-dataset files (no re-analysis): F2, F4, F6, F7, F11, F13 and,
    if with_raw, F3 and F12 (which need decile coverages from the raw evaluation files; read column-wise)."""
    from scripts import analyze3 as A
    root = TOP / "results"
    pdm = pd.read_csv(root / "per_dataset_main_v3.csv")
    A.fig_tradeoff(pdm)
    A.fig_upper(pdm)
    A.fig_shift(pdm)
    A.fig_decomp(pdm)
    A.fig_calsize(pd.read_csv(TOP / "tables" / "T7_calibration_size.csv"))
    A.fig_costs(pd.read_csv(root / "tail_alerts_per_dataset.csv"))
    if with_raw:
        import glob
        keep = [f"dec_cov_{k}" for k in range(10)] + [f"sig_cov_{k}" for k in range(10)]
        rows = []
        for fn in sorted(glob.glob(str(root / "raw_eval_v3" / "*.jsonl"))):
            with open(fn) as fh:
                for line in fh:
                    r = json.loads(line)
                    if r.get("alpha") == 0.1 and r.get("scheme") == "S5" and r.get("cal_frac") == 1.0:
                        rows.append({"did": r["did"], "method": r["method"], **{k: r.get(k) for k in keep}})
        a10 = pd.DataFrame(rows)
        A.fig_deciles(a10.groupby(["did", "method"])[keep[:10]].mean().reset_index())
        A.fig_sigma(a10.groupby(["did", "method"])[keep[10:]].mean().reset_index())


if __name__ == "__main__":
    which = sys.argv[1:] or ["f0", "f1", "f9", "f10"]
    for w in which:
        globals()[w]()
        print(w, "done")
