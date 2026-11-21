<!-- End matter in the form required by the journal ("Statements and Declarations"). Headings carry {-} so that they stay unnumbered. Identifying information is kept on the separate title page for double-blind review. -->

# Statements and Declarations {-}

**Competing interests.** The authors have no relevant financial or non-financial interests to disclose.

**Funding.** Funding information is given on the separate title page to preserve anonymity.

**Author contributions.** The contributions of each author are given on the separate title page to preserve anonymity.

**Data availability.** All datasets analysed in this study are publicly available on OpenML: study 353, the OpenML-CTR23 benchmark suite [@fischer2023openml], and, for the confirmatory replication, suites 335 and 336 [@grinsztajn2022tree]. They are downloaded programmatically through the OpenML API by the provided scripts; the OpenML identifier and the licence recorded by OpenML of each dataset ("not stated" where OpenML records none) are listed in Supplementary Tables S1 and S2. The per-run result files released with the code contain target values of the calibration and test splits; for the two datasets whose licences restrict use (socmob: non-commercial scholarly and teaching use; health_insurance: GPL ≥ 2), these files are released under the same terms.

**Code availability.** All code, configuration files, raw per-run results, both pre-specified analysis plans and the analysis scripts are provided to reviewers as an anonymised code package (supplementary material), together with the commit identifiers, times and hashes of the analysis plans cited in Section [-@sec:protocol]; the code and its full version history will be deposited in a public repository upon acceptance. A single command (`python run_all.py --mode full`) regenerates every table, figure and number of the manuscript from the raw data. All experiments ran single-threaded per task on a four-core cloud machine (Intel Xeon, 2.1 GHz, no GPU). The logged task run times of the final pipeline sum to about 15 CPU-hours (about 4 hours wall-clock on four cores), and to about 26 CPU-hours including the superseded earlier implementations; energy use was not measured.

**Ethics approval and consent.** Not applicable. The study used only publicly available, de-identified benchmark data, including individual-level survey records (cps88wages, health_insurance) and crime reports (seattlecrime6); it involved no human participants or animals and no identifiable personal data.

**Use of large language models.** The use of a large language model in this work is documented in Section [-@sec:llm], as required by the journal's policy.
