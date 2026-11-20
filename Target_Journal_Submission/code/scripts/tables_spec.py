"""Which generated table (tables/*.csv) each manuscript table shows. Display tables (D*) are written,
already formatted, by scripts/analyze3.py; values are never typed by hand."""

P3 = lambda v: f"{float(v):.3f}"
P2 = lambda v: f"{float(v):.2f}"

SPEC = {
    "prop1": dict(name="T0_prop1", cols=["model", "R2", "bottom10", "central80", "top10", "top1"],
                  rename={"model": "Model", "R2": "R²", "bottom10": "Bottom 10%", "central80": "Central 80%",
                          "top10": "Top 10%", "top1": "Top 1%"},
                  fmt={"R2": P2, "bottom10": P3, "central80": P3, "top10": P3, "top1": P3}),
    "positioning": dict(name="L1_positioning"),
    "datasets": dict(name="D1_datasets"),
    "main": dict(name="D2_main"),
    "size": dict(name="D3_size_tests", query="not (Family == 'Density estimator' and Comparison == 'SDLC vs SDLC-N')"),
    "sensitivity": dict(name="D3s_sensitivity"),
    "price": dict(name="D4_price"),
    "matched": dict(name="D4b_matched"),
    "shift": dict(name="D8_shift"),
    "alerts": dict(name="D13_alerts"),
    "alpha": dict(name="D5_alpha"),
    "strata": dict(name="D6_strata"),
    "calsize": dict(name="D7_calsize"),
    "variants": dict(name="D2b_variants"),
    "error": dict(name="D10_error"),
    "synthetic": dict(name="D11_synthetic"),
    "synthshift": dict(name="D12_synthetic_shift"),
    "learners": dict(name="D9_learners"),
    "confirmatory": dict(name="C2_display"),
}
