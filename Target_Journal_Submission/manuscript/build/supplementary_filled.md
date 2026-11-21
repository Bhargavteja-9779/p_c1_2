---
title: "Supplementary Material: Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression"
---

# S1. Datasets

**Table S1.** The OpenML-CTR23 datasets used in the main benchmark: size, number of features after one-hot encoding, skewness and number of distinct values of the target, realised number of calibration strata $K$, realised training mass of the lowest and highest stratum (nominal 0.10), relative test RMSE of the point model, and licence as recorded by OpenML.

| Dataset                       | n      | p   | Skewness   | Distinct y   | K   | Lower mass   | Upper mass   | RMSE/sd   | Licence                                         |
|:------------------------------|:-------|:----|:-----------|:-------------|:----|:-------------|:-------------|:----------|:------------------------------------------------|
| forest fires                  | 517    | 31  | 12.81      | 251          | 3   | 0.744        | 0.105        | 0.40      | CC BY 4.0                                       |
| energy efficiency             | 768    | 8   | 0.36       | 587          | 5   | 0.099        | 0.104        | 0.06      | CC BY 4.0                                       |
| cars                          | 804    | 17  | 1.57       | 798          | 5   | 0.100        | 0.104        | 0.27      | Public                                          |
| QSAR fish toxicity            | 908    | 6   | 0.25       | 827          | 5   | 0.099        | 0.103        | 0.62      | CC BY 4.0                                       |
| concrete compressive strength | 1,030  | 8   | 0.42       | 938          | 5   | 0.099        | 0.103        | 0.30      | CC BY 4.0                                       |
| geographical origin of music  | 1,059  | 116 | -0.99      | 31           | 5   | 0.084        | 0.117        | 0.90      | CC BY 4.0                                       |
| socmob                        | 1,156  | 43  | 4.43       | 361          | 4   | 0.240        | 0.102        | 0.49      | Non-commercial scholarly and teaching purposes. |
| Moneyball                     | 1,232  | 78  | 0.17       | 374          | 5   | 0.099        | 0.103        | 0.27      | Public                                          |
| airfoil self noise            | 1,503  | 5   | -0.42      | 1,456        | 5   | 0.100        | 0.102        | 0.28      | CC BY 4.0                                       |
| auction verification          | 2,043  | 18  | 1.50       | 2,039        | 5   | 0.100        | 0.102        | 0.17      | CC BY 4.0                                       |
| space ga                      | 3,107  | 6   | -1.02      | 3,105        | 5   | 0.100        | 0.101        | 0.56      | Public                                          |
| abalone                       | 4,177  | 11  | 1.11       | 28           | 5   | 0.045        | 0.114        | 0.65      | CC BY 4.0                                       |
| cpu activity                  | 8,192  | 21  | -3.42      | 56           | 5   | 0.096        | 0.104        | 0.13      | Public                                          |
| pumadyn32nh                   | 8,192  | 32  | -0.05      | 8,191        | 5   | 0.100        | 0.100        | 0.61      | Public                                          |
| kin8nm                        | 8,192  | 8   | 0.09       | 8,191        | 5   | 0.100        | 0.100        | 0.47      | Public                                          |
| grid stability                | 10,000 | 12  | 0.02       | 10,000       | 5   | 0.100        | 0.100        | 0.22      | CC BY 4.0                                       |
| brazilian houses              | 10,692 | 53  | 58.95      | 5,751        | 5   | 0.100        | 0.100        | 1.26      | CC 0: Public Domain                             |
| naval propulsion plant        | 11,934 | 14  | -0.00      | 51           | 5   | 0.096        | 0.117        | 0.06      | CC BY 4.0                                       |
| miami housing                 | 13,932 | 15  | 3.22       | 2,111        | 5   | 0.099        | 0.100        | 0.28      | CC0: Public Domain                              |
| fifa                          | 19,178 | 191 | 6.47       | 133          | 4   | 0.207        | 0.103        | 0.48      | CC0: Public Domain                              |
| california housing            | 20,640 | 8   | 0.98       | 3,842        | 5   | 0.100        | 0.100        | 0.41      | Public                                          |
| superconductivity             | 21,263 | 81  | 0.86       | 3,007        | 5   | 0.100        | 0.101        | 0.29      | CC BY 4.0                                       |
| kings county                  | 21,613 | 136 | 4.02       | 4,028        | 5   | 0.098        | 0.100        | 0.33      | CC 0: Public Domain                             |
| health insurance              | 22,272 | 32  | -0.34      | 75           | 2   | 0.555        | 0.442        | 0.78      | GPL (>= 2)                                      |
| fps benchmark                 | 24,624 | 971 | 1.05       | 2,675        | 5   | 0.100        | 0.100        | 0.02      | CC BY                                           |
| cps88wages                    | 28,155 | 16  | 6.50       | 5,970        | 5   | 0.100        | 0.107        | 0.82      | Public                                          |
| physiochemical protein        | 45,730 | 9   | 0.57       | 15,903       | 5   | 0.100        | 0.100        | 0.61      | CC BY 4.0                                       |
| sarcos                        | 48,933 | 21  | 0.15       | 11,414       | 5   | 0.100        | 0.100        | 0.13      | Public                                          |
| diamonds                      | 53,940 | 29  | 1.62       | 11,602       | 5   | 0.099        | 0.100        | 0.14      | Public                                          |
| video transcoding             | 68,784 | 26  | 4.25       | 10,960       | 5   | 0.100        | 0.100        | 0.07      | CC BY 4.0                                       |
| wave energy                   | 72,000 | 36  | 0.14       | 71,993       | 5   | 0.100        | 0.100        | 0.40      | CC BY 4.0                                       |

**Table S2.** Held-out datasets of the confirmatory replication (regression datasets of OpenML suites 335/336 without source overlap with CTR23; datasets above 50,000 rows subsampled once with seed 2026). Excluded by content overlap: cpu_act (cpu_activity); houses (california_housing); house_sales (kings_county); MiamiHousing2016 (miami_housing); superconduct (superconductivity); diamonds; Brazilian_houses; abalone; wine_quality (wine). Excluded by the distinct-value rule: 44055 analcatdata_supreme; 44133 pol.

| OpenML ID   | Dataset                             | n (used)   | p    | Distinct y   | Licence                       |
|:------------|:------------------------------------|:-----------|:-----|:-------------|:------------------------------|
| 44056       | visualizing_soil                    | 8,641      | 6    | 40           | Public                        |
| 44061       | Mercedes_Benz_Greener_Manufacturing | 4,209      | 1094 | 2,545        | Public                        |
| 44068       | particulate-matter-ukair-2017       | 394,299    | 29   | 21,599       | Open Government Licence (OGL) |
| 44069       | SGEMM_GPU_kernel_performance        | 241,600    | 21   | 58,161       | CC BY 4.0                     |
| 44134       | elevators                           | 16,599     | 16   | 61           | Public                        |
| 44137       | Ailerons                            | 13,750     | 33   | 35           | Public                        |
| 44139       | house_16H                           | 22,784     | 16   | 2,045        | Public                        |
| 44142       | Bike_Sharing_Demand                 | 17,379     | 6    | 869          | Public                        |
| 44143       | nyc-taxi-green-dec-2016             | 581,835    | 9    | 1,811        | Public                        |
| 44145       | sulfur                              | 10,081     | 6    | 9,368        | Public                        |
| 44146       | medical_charges                     | 163,065    | 3    | 154,891      | Public Domain (CC0)           |
| 45032       | yprop_4_1                           | 8,885      | 42   | 1,336        | Public                        |
| 45034       | delays_zurich_transport             | 5,465,575  | 8    | 4,082        | CCZero                        |
| 45041       | topo_2_1                            | 8,885      | 261  | 1,336        | Public                        |
| 45043       | seattlecrime6                       | 52,031     | 26   | 29           | CC0                           |
| 45046       | Allstate_Claims_Severity            | 188,318    | 587  | 158,223      | Public                        |
| 45047       | Airlines_DepDelay_1M                | 1,000,000  | 5    | 629          | CC0                           |

# S2. Leakage audit

Exact duplicate rows (features and target), duplicate feature vectors, the share of test feature vectors that also occur in the training split (seed 0), and the share of missing values, recomputed on the final data files (scripts/leakage_audit.py). Random splitting keeps rows exchangeable, so the coverage guarantees hold for new rows from the same pool; repeated units (duplicates, repeated videos, repeat sales) mean that they do not transfer to new units.

**Table S3.** Leakage audit (sorted by the share of test feature vectors seen in training).

| Dataset                       | n     | Duplicate rows   | Duplicate feature vectors   | Test feature vectors seen in training (seed 0)   | Missing values   |
|:------------------------------|:------|:-----------------|:----------------------------|:-------------------------------------------------|:-----------------|
| cps88wages                    | 28155 | 0.0756           | 0.7740                      | 0.8245                                           | 0.0000           |
| superconductivity             | 21263 | 0.0031           | 0.2866                      | 0.3138                                           | 0.0000           |
| QSAR_fish_toxicity            | 908   | 0.0011           | 0.1465                      | 0.1542                                           | 0.0000           |
| sarcos                        | 48933 | 0.0909           | 0.0909                      | 0.0908                                           | 0.0000           |
| health_insurance              | 22272 | 0.0436           | 0.0798                      | 0.0875                                           | 0.0000           |
| brazilian_houses              | 10692 | 0.0337           | 0.0677                      | 0.0849                                           | 0.0000           |
| physiochemical_protein        | 45730 | 0.0374           | 0.0384                      | 0.0396                                           | 0.0000           |
| concrete_compressive_strength | 1030  | 0.0243           | 0.0330                      | 0.0233                                           | 0.0000           |
| forest_fires                  | 517   | 0.0077           | 0.0251                      | 0.0231                                           | 0.0000           |
| diamonds                      | 53940 | 0.0027           | 0.0064                      | 0.0065                                           | 0.0000           |
| cars                          | 804   | 0.0000           | 0.0012                      | 0.0050                                           | 0.0000           |
| video_transcoding             | 68784 | 0.0000           | 0.0012                      | 0.0010                                           | 0.0000           |
| miami_housing                 | 13932 | 0.0000           | 0.0007                      | 0.0003                                           | 0.0000           |
| energy_efficiency             | 768   | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| Moneyball                     | 1232  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0169           |
| wave_energy                   | 72000 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| grid_stability                | 10000 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| geographical_origin_of_music  | 1059  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| naval_propulsion_plant        | 11934 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| airfoil_self_noise            | 1503  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| abalone                       | 4177  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| auction_verification          | 2043  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| cpu_activity                  | 8192  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| kin8nm                        | 8192  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| pumadyn32nh                   | 8192  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| california_housing            | 20640 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| socmob                        | 1156  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| fps_benchmark                 | 24624 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0029           |
| kings_county                  | 21613 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| fifa                          | 19178 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |
| space_ga                      | 3107  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           |

# S3. Implementation checks

*Exactness of scores.* Calibration and test scores are evaluated exactly at the observed target, so the coverage reported for every location–scale method is that of the exact rule (4) of the main text.

*Set geometry.* Sizes, piece counts, hulls and alerts are those of the stratum-exact set for the piecewise-linear interpolant of $\hat g$ on a standardised grid (1,536 core and 2×256 tail points by default). The production algorithm decomposes the interpolant into monotone runs, on each of which a super-level set is an interval. It reproduces a cell-by-cell reference implementation to a relative size difference below $10^{-14}$, with identical piece counts, hulls, alerts and coverage (unit test `tests/test_ls_exact3.py`). Table S4 compares three grid resolutions with the finest one.

**Table S4.** Grid convergence of SDLC sets (seed 0, $\alpha=0.1$).

| OpenML ID   | Core points   | Tail points   | Mean size    | Rel. diff. of mean size   | Max rel. diff. per point   | 99% quantile rel. diff.   | Share with different piece count   | Empty-set mismatches   |
|:------------|:--------------|:--------------|:-------------|:--------------------------|:---------------------------|:--------------------------|:-----------------------------------|:-----------------------|
| 44963       | 512           | 64            | 10.16319     | 0.00006                   | 0.00390                    | 0.00034                   | 0.00289                            | 0                      |
| 44963       | 1536          | 256           | 10.16262     | 0.00001                   | 0.00224                    | 0.00008                   | 0.00000                            | 0                      |
| 44963       | 6144          | 1024          | 10.16255     | 0.00000                   | 0.00000                    | 0.00000                   | 0.00000                            | 0                      |
| 45012       | 512           | 64            | 17323.23123  | 0.00002                   | 0.00313                    | 0.00073                   | 0.00063                            | 0                      |
| 45012       | 1536          | 256           | 17322.86174  | 0.00000                   | 0.00085                    | 0.00015                   | 0.00021                            | 0                      |
| 45012       | 6144          | 1024          | 17322.82412  | 0.00000                   | 0.00000                    | 0.00000                   | 0.00000                            | 0                      |
| 44987       | 512           | 64            | 43.11462     | 0.00017                   | 0.15946                    | 0.09813                   | 0.01384                            | 0                      |
| 44987       | 1536          | 256           | 43.12198     | 0.00000                   | 0.01346                    | 0.00794                   | 0.00000                            | 0                      |
| 44987       | 6144          | 1024          | 43.12183     | 0.00000                   | 0.00000                    | 0.00000                   | 0.00000                            | 0                      |
| 44958       | 512           | 64            | 3570.19296   | 0.00020                   | 0.09365                    | 0.05916                   | 0.03333                            | 0                      |
| 44958       | 1536          | 256           | 3569.53013   | 0.00001                   | 0.01477                    | 0.00818                   | 0.00980                            | 0                      |
| 44958       | 6144          | 1024          | 3569.49619   | 0.00000                   | 0.00000                    | 0.00000                   | 0.00000                            | 0                      |
| 44990       | 512           | 64            | 9167.39704   | 0.00139                   | 0.08523                    | 0.03564                   | 0.04003                            | 0                      |
| 44990       | 1536          | 256           | 9164.94776   | 0.00166                   | 0.01054                    | 0.00753                   | 0.00374                            | 0                      |
| 44990       | 6144          | 1024          | 9180.17517   | 0.00000                   | 0.00000                    | 0.00000                   | 0.00000                            | 0                      |
| 44975       | 512           | 64            | 146450.74457 | 0.00001                   | 0.00023                    | 0.00009                   | 0.00000                            | 0                      |
| 44975       | 1536          | 256           | 146449.76909 | 0.00000                   | 0.00005                    | 0.00002                   | 0.00006                            | 0                      |
| 44975       | 6144          | 1024          | 146449.66930 | 0.00000                   | 0.00000                    | 0.00000                   | 0.00000                            | 0                      |

*Finite-sample validity.* A Monte Carlo test with known exchangeable data (`tests/test_ls_exact3.py`) confirms that the empirical stratum-wise coverage matches the theoretical value $\lceil (n_k+1)(1-\alpha)\rceil/(n_k+1)$.

# S4. Additional results

**Table S5.** Sensitivity of the set-size comparisons among stratified methods (geometric-mean ratio of SDLC to each comparator with 95% bootstrap CI, wins/losses of SDLC, Holm-adjusted two-sided Wilcoxon $p$ within each analysis). Development datasets: airfoil, concrete, QSAR fish; diagnostic datasets: cpu activity, naval propulsion, cars, energy efficiency, forest fires, fifa, Miami housing.

| Analysis                                    | Comparison    | n   | Ratio [95% CI]       | Wins/losses   | Holm p   |
|:--------------------------------------------|:--------------|:----|:---------------------|:--------------|:---------|
| primary (alpha=0.1, S5, all datasets)       | SDLC vs BCCP  | 31  | 0.902 [0.841, 0.956] | 24/7          | < 0.001  |
| primary (alpha=0.1, S5, all datasets)       | SDLC vs S-NCP | 31  | 0.975 [0.941, 1.020] | 27/4          | < 0.001  |
| primary (alpha=0.1, S5, all datasets)       | SDLC vs S-CQR | 31  | 0.795 [0.702, 0.878] | 27/4          | < 0.001  |
| primary (alpha=0.1, S5, all datasets)       | SDLC vs S-HPD | 31  | 0.947 [0.929, 0.963] | 28/3          | < 0.001  |
| excluding development datasets              | SDLC vs BCCP  | 28  | 0.893 [0.828, 0.954] | 23/5          | < 0.001  |
| excluding development datasets              | SDLC vs S-NCP | 28  | 0.977 [0.940, 1.027] | 25/3          | < 0.001  |
| excluding development datasets              | SDLC vs S-CQR | 28  | 0.791 [0.690, 0.884] | 24/4          | < 0.001  |
| excluding development datasets              | SDLC vs S-HPD | 28  | 0.949 [0.929, 0.966] | 25/3          | < 0.001  |
| excluding development + diagnostic datasets | SDLC vs BCCP  | 21  | 0.899 [0.843, 0.945] | 18/3          | < 0.001  |
| excluding development + diagnostic datasets | SDLC vs S-NCP | 21  | 0.974 [0.930, 1.037] | 20/1          | < 0.001  |
| excluding development + diagnostic datasets | SDLC vs S-CQR | 21  | 0.757 [0.643, 0.861] | 19/2          | < 0.001  |
| excluding development + diagnostic datasets | SDLC vs S-HPD | 21  | 0.953 [0.927, 0.973] | 19/2          | < 0.001  |
| datasets with nominal tail strata           | SDLC vs BCCP  | 26  | 0.940 [0.904, 0.980] | 20/6          | < 0.001  |
| datasets with nominal tail strata           | SDLC vs S-NCP | 26  | 0.956 [0.931, 0.983] | 24/2          | < 0.001  |
| datasets with nominal tail strata           | SDLC vs S-CQR | 26  | 0.762 [0.664, 0.853] | 24/2          | < 0.001  |
| datasets with nominal tail strata           | SDLC vs S-HPD | 26  | 0.943 [0.922, 0.961] | 25/1          | < 0.001  |
| |skewness| > 1                              | SDLC vs BCCP  | 15  | 0.857 [0.748, 0.965] | 12/3          | 0.025    |
| |skewness| > 1                              | SDLC vs S-NCP | 15  | 0.988 [0.920, 1.082] | 12/3          | 0.127    |
| |skewness| > 1                              | SDLC vs S-CQR | 15  | 0.821 [0.642, 0.988] | 11/4          | 0.127    |
| |skewness| > 1                              | SDLC vs S-HPD | 15  | 0.938 [0.905, 0.964] | 12/3          | 0.003    |
| |skewness| <= 1                             | SDLC vs BCCP  | 16  | 0.947 [0.918, 0.975] | 12/4          | 0.005    |
| |skewness| <= 1                             | SDLC vs S-NCP | 16  | 0.963 [0.947, 0.977] | 15/1          | < 0.001  |
| |skewness| <= 1                             | SDLC vs S-CQR | 16  | 0.771 [0.723, 0.821] | 16/0          | < 0.001  |
| |skewness| <= 1                             | SDLC vs S-HPD | 16  | 0.957 [0.941, 0.972] | 16/0          | < 0.001  |
| n >= 1600                                   | SDLC vs BCCP  | 22  | 0.884 [0.817, 0.935] | 20/2          | < 0.001  |
| n >= 1600                                   | SDLC vs S-NCP | 22  | 0.946 [0.922, 0.964] | 22/0          | < 0.001  |
| n >= 1600                                   | SDLC vs S-CQR | 22  | 0.743 [0.635, 0.839] | 21/1          | < 0.001  |
| n >= 1600                                   | SDLC vs S-HPD | 22  | 0.946 [0.923, 0.964] | 21/1          | < 0.001  |
| n < 1600                                    | SDLC vs BCCP  | 9   | 0.948 [0.801, 1.076] | 4/5           | 1.000    |
| n < 1600                                    | SDLC vs S-NCP | 9   | 1.050 [0.956, 1.190] | 5/4           | 1.000    |
| n < 1600                                    | SDLC vs S-CQR | 9   | 0.938 [0.847, 1.064] | 6/3           | 0.750    |
| n < 1600                                    | SDLC vs S-HPD | 9   | 0.951 [0.924, 0.979] | 7/2           | 0.078    |
| alpha = 0.05                                | SDLC vs BCCP  | 31  | 0.876 [0.801, 0.943] | 25/6          | < 0.001  |
| alpha = 0.05                                | SDLC vs S-NCP | 31  | 0.990 [0.951, 1.047] | 25/6          | 0.002    |
| alpha = 0.05                                | SDLC vs S-CQR | 31  | 0.713 [0.605, 0.820] | 29/2          | < 0.001  |
| alpha = 0.05                                | SDLC vs S-HPD | 31  | 0.948 [0.926, 0.965] | 29/2          | < 0.001  |
| alpha = 0.2                                 | SDLC vs BCCP  | 31  | 0.935 [0.880, 0.978] | 22/9          | < 0.001  |
| alpha = 0.2                                 | SDLC vs S-NCP | 31  | 0.938 [0.912, 0.963] | 28/3          | < 0.001  |
| alpha = 0.2                                 | SDLC vs S-CQR | 31  | 0.823 [0.754, 0.883] | 28/3          | < 0.001  |
| alpha = 0.2                                 | SDLC vs S-HPD | 31  | 0.932 [0.907, 0.954] | 29/2          | < 0.001  |
| strata S3                                   | SDLC vs BCCP  | 31  | 0.900 [0.845, 0.951] | 26/5          | < 0.001  |
| strata S3                                   | SDLC vs S-NCP | 31  | 0.962 [0.922, 1.008] | 28/3          | < 0.001  |
| strata S3                                   | SDLC vs S-CQR | 31  | 0.781 [0.690, 0.862] | 28/3          | < 0.001  |
| strata S3                                   | SDLC vs S-HPD | 31  | 0.936 [0.907, 0.958] | 29/2          | < 0.001  |
| strata S10                                  | SDLC vs BCCP  | 31  | 0.900 [0.837, 0.957] | 26/5          | < 0.001  |
| strata S10                                  | SDLC vs S-NCP | 31  | 0.980 [0.950, 1.023] | 26/5          | < 0.001  |
| strata S10                                  | SDLC vs S-CQR | 31  | 0.809 [0.713, 0.894] | 26/5          | < 0.001  |
| strata S10                                  | SDLC vs S-HPD | 31  | 0.951 [0.936, 0.964] | 28/3          | < 0.001  |

**Table S6.** Miscoverage level: marginal coverage, worst-stratum coverage, upper-tail coverage and geometric-mean size (means over datasets).

| alpha   | method     | coverage   | worst_stratum   | upper_tail   | size_geo   |
|:--------|:-----------|:-----------|:----------------|:-------------|:-----------|
| 0.050   | SCP        | 0.952      | 0.772           | 0.814        | 1.053      |
| 0.050   | NCP        | 0.952      | 0.858           | 0.893        | 1.005      |
| 0.050   | CQR        | 0.951      | 0.808           | 0.845        | 1.374      |
| 0.050   | Mondrian-ŷ | 0.954      | 0.866           | 0.893        | 1.070      |
| 0.050   | DCP        | 0.952      | 0.878           | 0.903        | 1.017      |
| 0.050   | HPD-split  | 0.953      | 0.863           | 0.895        | 1.030      |
| 0.050   | DLS        | 0.952      | 0.819           | 0.854        | 0.937      |
| 0.050   | BCCP       | 0.954      | 0.947           | 0.955        | 1.424      |
| 0.050   | S-NCP      | 0.954      | 0.947           | 0.955        | 1.260      |
| 0.050   | S-CQR      | 0.955      | 0.945           | 0.956        | 1.748      |
| 0.050   | S-HPD      | 0.954      | 0.948           | 0.956        | 1.315      |
| 0.050   | SDLC-N     | 0.954      | 0.946           | 0.955        | 1.240      |
| 0.050   | SDLC       | 0.954      | 0.947           | 0.955        | 1.247      |
| 0.050   | SDLC-floor | 0.962      | 0.912           | 0.928        | 1.083      |
| 0.100   | SCP        | 0.903      | 0.630           | 0.690        | 0.763      |
| 0.100   | NCP        | 0.903      | 0.765           | 0.812        | 0.769      |
| 0.100   | CQR        | 0.903      | 0.720           | 0.759        | 0.927      |
| 0.100   | Mondrian-ŷ | 0.905      | 0.770           | 0.811        | 0.787      |
| 0.100   | DCP        | 0.902      | 0.783           | 0.820        | 0.781      |
| 0.100   | HPD-split  | 0.903      | 0.759           | 0.809        | 0.779      |
| 0.100   | DLS        | 0.902      | 0.660           | 0.723        | 0.703      |
| 0.100   | BCCP       | 0.904      | 0.890           | 0.908        | 0.969      |
| 0.100   | S-NCP      | 0.904      | 0.891           | 0.907        | 0.897      |
| 0.100   | S-CQR      | 0.905      | 0.892           | 0.907        | 1.100      |
| 0.100   | S-HPD      | 0.904      | 0.893           | 0.907        | 0.923      |
| 0.100   | SDLC-N     | 0.905      | 0.893           | 0.909        | 0.881      |
| 0.100   | SDLC       | 0.903      | 0.891           | 0.906        | 0.874      |
| 0.100   | SDLC-floor | 0.919      | 0.821           | 0.852        | 0.806      |
| 0.200   | SCP        | 0.802      | 0.470           | 0.544        | 0.514      |
| 0.200   | NCP        | 0.803      | 0.641           | 0.699        | 0.567      |
| 0.200   | CQR        | 0.804      | 0.593           | 0.644        | 0.633      |
| 0.200   | Mondrian-ŷ | 0.806      | 0.626           | 0.669        | 0.549      |
| 0.200   | DCP        | 0.802      | 0.642           | 0.697        | 0.565      |
| 0.200   | HPD-split  | 0.802      | 0.615           | 0.687        | 0.550      |
| 0.200   | DLS        | 0.801      | 0.433           | 0.522        | 0.481      |
| 0.200   | BCCP       | 0.803      | 0.786           | 0.816        | 0.643      |
| 0.200   | S-NCP      | 0.804      | 0.789           | 0.812        | 0.641      |
| 0.200   | S-CQR      | 0.807      | 0.789           | 0.815        | 0.731      |
| 0.200   | S-HPD      | 0.804      | 0.791           | 0.811        | 0.645      |
| 0.200   | SDLC-N     | 0.804      | 0.790           | 0.814        | 0.602      |
| 0.200   | SDLC       | 0.803      | 0.789           | 0.813        | 0.601      |
| 0.200   | SDLC-floor | 0.823      | 0.638           | 0.696        | 0.560      |

**Table S7.** Strata: three (S3), five (S5) and ten (S10, deciles) strata from training quantiles; worst-stratum and worst-decile coverage, geometric-mean size and number of runs with an infinite stratum threshold.

| scheme   | K_median   | method   | worst_stratum   | worst_decile   | size_geo   | runs_with_inf   |
|:---------|:-----------|:---------|:----------------|:---------------|:-----------|:----------------|
| S3       | 3.000      | BCCP     | 0.895           | 0.781          | 0.950      | 1               |
| S3       | 3.000      | S-NCP    | 0.895           | 0.839          | 0.889      | 1               |
| S3       | 3.000      | S-CQR    | 0.894           | 0.809          | 1.095      | 1               |
| S3       | 3.000      | S-HPD    | 0.895           | 0.813          | 0.914      | 1               |
| S3       | 3.000      | SDLC-N   | 0.895           | 0.819          | 0.865      | 1               |
| S3       | 3.000      | SDLC     | 0.893           | 0.769          | 0.855      | 1               |
| S3       | 3.000      | DLS      | 0.657           | 0.656          | 0.703      | 1               |
| S5       | 5.000      | BCCP     | 0.890           | 0.860          | 0.969      | 2               |
| S5       | 5.000      | S-NCP    | 0.891           | 0.872          | 0.897      | 2               |
| S5       | 5.000      | S-CQR    | 0.892           | 0.846          | 1.100      | 2               |
| S5       | 5.000      | S-HPD    | 0.893           | 0.870          | 0.923      | 2               |
| S5       | 5.000      | SDLC-N   | 0.893           | 0.872          | 0.881      | 2               |
| S5       | 5.000      | SDLC     | 0.891           | 0.863          | 0.874      | 2               |
| S5       | 5.000      | DLS      | 0.660           | 0.656          | 0.703      | 2               |
| S10      | 10.000     | BCCP     | 0.886           | 0.888          | 0.998      | 10              |
| S10      | 10.000     | S-NCP    | 0.889           | 0.890          | 0.916      | 10              |
| S10      | 10.000     | S-CQR    | 0.889           | 0.889          | 1.111      | 10              |
| S10      | 10.000     | S-HPD    | 0.891           | 0.892          | 0.944      | 10              |
| S10      | 10.000     | SDLC-N   | 0.890           | 0.891          | 0.899      | 10              |
| S10      | 10.000     | SDLC     | 0.887           | 0.888          | 0.898      | 10              |
| S10      | 10.000     | DLS      | 0.657           | 0.656          | 0.703      | 10              |

**Table S8.** Calibration-set size (fraction of the calibration split used; runs with an infinite threshold refer to the stratified methods).

| cal_frac   | mean_n_cal   | method   | coverage   | worst_stratum   | size_geo   | runs_with_inf   |
|:-----------|:-------------|:---------|:-----------|:----------------|:-----------|:----------------|
| 0.250      | 1081.798     | SCP      | 0.905      | 0.647           | 0.792      | 87              |
| 0.250      | 1081.798     | NCP      | 0.907      | 0.778           | 0.800      | 87              |
| 0.250      | 1081.798     | CQR      | 0.905      | 0.729           | 0.946      | 87              |
| 0.250      | 1081.798     | BCCP     | 0.914      | 0.899           | 1.372      | 87              |
| 0.250      | 1081.798     | S-NCP    | 0.915      | 0.901           | 1.281      | 87              |
| 0.250      | 1081.798     | S-CQR    | 0.914      | 0.899           | 1.527      | 87              |
| 0.250      | 1081.798     | SDLC-N   | 0.915      | 0.897           | 1.252      | 87              |
| 0.250      | 1081.798     | SDLC     | 0.915      | 0.899           | 1.243      | 87              |
| 0.500      | 2163.597     | SCP      | 0.903      | 0.633           | 0.767      | 32              |
| 0.500      | 2163.597     | NCP      | 0.903      | 0.767           | 0.778      | 32              |
| 0.500      | 2163.597     | CQR      | 0.904      | 0.722           | 0.932      | 32              |
| 0.500      | 2163.597     | BCCP     | 0.906      | 0.895           | 1.091      | 32              |
| 0.500      | 2163.597     | S-NCP    | 0.907      | 0.896           | 1.019      | 32              |
| 0.500      | 2163.597     | S-CQR    | 0.908      | 0.894           | 1.236      | 32              |
| 0.500      | 2163.597     | SDLC-N   | 0.907      | 0.896           | 1.002      | 32              |
| 0.500      | 2163.597     | SDLC     | 0.906      | 0.893           | 0.996      | 32              |
| 1.000      | 4327.194     | SCP      | 0.903      | 0.630           | 0.763      | 2               |
| 1.000      | 4327.194     | NCP      | 0.903      | 0.765           | 0.769      | 2               |
| 1.000      | 4327.194     | CQR      | 0.903      | 0.720           | 0.927      | 2               |
| 1.000      | 4327.194     | BCCP     | 0.904      | 0.890           | 0.969      | 2               |
| 1.000      | 4327.194     | S-NCP    | 0.904      | 0.891           | 0.897      | 2               |
| 1.000      | 4327.194     | S-CQR    | 0.905      | 0.892           | 1.100      | 2               |
| 1.000      | 4327.194     | SDLC-N   | 0.905      | 0.893           | 0.881      | 2               |
| 1.000      | 4327.194     | SDLC     | 0.903      | 0.891           | 0.874      | 2               |

**Table S9.** Density estimators and variants ($\alpha=0.1$).

| method         | code          | coverage   | lower_tail_cov   | upper_tail_cov   | worst_stratum   | n_ds_below_null   | top5_cov   | top1_cov   | size_geo   | size_median_ds   | pieces   | empty_rate   | empty_ds   | sigma_decile_worst   | wsc   | wsc_n   |
|:---------------|:--------------|:-----------|:-----------------|:-----------------|:----------------|:------------------|:-----------|:-----------|:-----------|:-----------------|:---------|:-------------|:-----------|:---------------------|:------|:--------|
| BCCP-hull      | S-Res-hull    | 0.916      | 0.907            | 0.908            | 0.895           | 1                 | 0.863      | 0.687      | 1.051      | 1.099            | 1.000    | 0.000        | 1          | 0.758                | 0.838 | 27      |
| S-NCP-hull     | S-NCP-hull    | 0.913      | 0.906            | 0.909            | 0.895           | 1                 | 0.880      | 0.789      | 0.936      | 1.077            | 0.999    | 0.001        | 2          | 0.805                | 0.893 | 27      |
| SDLC-hull      | SDLC-LS-hull  | 0.918      | 0.908            | 0.910            | 0.898           | 0                 | 0.872      | 0.743      | 0.949      | 0.986            | 0.996    | 0.004        | 8          | 0.790                | 0.861 | 27      |
| BCCP-floor     | S-Res-floor   | 0.923      | 0.903            | 0.847            | 0.817           | 28                | 0.774      | 0.564      | 0.903      | 0.993            | 1.164    | 0.000        | 1          | 0.723                | 0.835 | 27      |
| S-NCP-floor    | S-NCP-floor   | 0.911      | 0.880            | 0.874            | 0.842           | 23                | 0.830      | 0.715      | 0.843      | 0.943            | 1.062    | 0.001        | 3          | 0.807                | 0.885 | 27      |
| SDLC-floor     | SDLC-LS-floor | 0.919      | 0.893            | 0.852            | 0.821           | 29                | 0.787      | 0.594      | 0.806      | 0.925            | 1.261    | 0.005        | 9          | 0.760                | 0.856 | 27      |
| SDLC-2p        | SDLC-LS2      | 0.903      | 0.904            | 0.909            | 0.891           | 0                 | 0.868      | 0.733      | 0.881      | 0.954            | 1.499    | 0.001        | 6          | 0.780                | 0.852 | 27      |
| SDLC-2p-hull   | SDLC-LS2-hull | 0.918      | 0.908            | 0.911            | 0.898           | 0                 | 0.869      | 0.740      | 0.958      | 0.963            | 0.999    | 0.001        | 6          | 0.799                | 0.865 | 27      |
| DLS-2p         | DLS-M-LS2     | 0.903      | 0.863            | 0.714            | 0.656           | 31                | 0.615      | 0.459      | 0.701      | 0.711            | 1.067    | 0.003        | 11         | 0.693                | 0.803 | 27      |
| SDLC-hist      | SDLC-H        | 0.905      | 0.908            | 0.909            | 0.893           | 3                 | 0.859      | 0.862      | 1.745      | 1.818            | 3.671    | 0.000        | 1          | 0.821                | 0.872 | 27      |
| DLS-hist       | DLS-M-H       | 0.903      | 0.846            | 0.672            | 0.628           | 30                | 0.578      | 0.556      | 1.111      | 1.299            | 2.770    | 0.002        | 5          | 0.731                | 0.809 | 27      |
| HPD-split-hist | HPD-split-H   | 0.902      | 0.857            | 0.743            | 0.719           | 30                | 0.676      | 0.773      | 1.411      | 1.535            | 3.307    | 0.000        | 0          | 0.810                | 0.869 | 27      |
| S-HPD-hist     | S-HPD-H       | 0.904      | 0.907            | 0.911            | 0.893           | 2                 | 0.863      | 0.919      | 2.253      | 2.125            | 4.324    | 0.000        | 0          | 0.834                | 0.882 | 27      |
| DLS-N          | DLS-M-N       | 0.903      | 0.859            | 0.760            | 0.707           | 30                | 0.676      | 0.514      | 0.708      | 0.888            | 0.995    | 0.005        | 12         | 0.736                | 0.835 | 27      |

**Table S10.** Synthetic study: coverage of the upper stratum under a genuine label shift (test points drawn with acceptance probability proportional to $\exp\{\gamma\Phi^{-1}(F_Y(y))\}$, so that $X\mid Y$ is unchanged); designs A and B, 10 seeds.

| Method    | A, γ=0   | A, γ=0.5   | A, γ=1   | A, γ=2   | B, γ=0   | B, γ=0.5   | B, γ=1   | B, γ=2   |
|:----------|:---------|:-----------|:---------|:---------|:---------|:-----------|:---------|:---------|
| SCP       | 0.709    | 0.662      | 0.607    | 0.419    | 0.806    | 0.776      | 0.730    | 0.569    |
| CQR       | 0.694    | 0.648      | 0.593    | 0.410    | 0.752    | 0.721      | 0.672    | 0.512    |
| HPD-split | 0.675    | 0.633      | 0.581    | 0.405    | 0.814    | 0.788      | 0.746    | 0.598    |
| O-HDR-X   | 0.693    | 0.650      | 0.600    | 0.423    | 0.841    | 0.820      | 0.786    | 0.655    |
| BCCP      | 0.893    | 0.860      | 0.811    | 0.630    | 0.899    | 0.877      | 0.842    | 0.698    |
| S-NCP     | 0.895    | 0.868      | 0.824    | 0.660    | 0.894    | 0.875      | 0.843    | 0.714    |
| S-CQR     | 0.891    | 0.854      | 0.803    | 0.617    | 0.896    | 0.874      | 0.835    | 0.688    |
| SDLC      | 0.894    | 0.865      | 0.818    | 0.645    | 0.898    | 0.875      | 0.841    | 0.705    |
| O-SDLC    | 0.897    | 0.869      | 0.825    | 0.654    | 0.903    | 0.883      | 0.852    | 0.725    |

**Table S11.** Per-dataset error analysis for SDLC ($\alpha=0.1$): calibration size, target skewness, share of zero targets, relative RMSE, worst-stratum coverage, size, and size ratios to DLS (price), S-NCP and BCCP.

| dataset                       | n_cal     | skew_y   | zero_frac   | rmse_over_sd   | worst_stratum   | nsize   | price   | vs_sncp   | vs_bccp   | empty_rate   |
|:------------------------------|:----------|:---------|:------------|:---------------|:----------------|:--------|:--------|:----------|:----------|:-------------|
| grid_stability                | 2500.000  | 0.019    | 0.000       | 0.218          | 0.897           | 0.645   | 0.983   | 0.966     | 0.970     | 0.001        |
| naval_propulsion_plant        | 2984.000  | -0.000   | 0.000       | 0.060          | 0.891           | 0.168   | 1.002   | 0.954     | 0.995     | 0.018        |
| kin8nm                        | 2048.000  | 0.090    | 0.000       | 0.472          | 0.883           | 1.491   | 1.012   | 0.990     | 0.953     | 0.000        |
| sarcos                        | 12233.000 | 0.152    | 0.002       | 0.130          | 0.896           | 0.356   | 1.013   | 0.942     | 0.898     | 0.001        |
| fps_benchmark                 | 6156.000  | 1.053    | 0.000       | 0.022          | 0.892           | 0.059   | 1.024   | 0.911     | 0.988     | 0.021        |
| physiochemical_protein        | 11432.000 | 0.567    | 0.006       | 0.607          | 0.898           | 1.673   | 1.026   | 0.970     | 0.903     | 0.000        |
| Moneyball                     | 308.000   | 0.174    | 0.000       | 0.268          | 0.881           | 0.963   | 1.042   | 0.984     | 1.017     | 0.000        |
| cpu_activity                  | 2048.000  | -3.416   | 0.035       | 0.127          | 0.895           | 0.362   | 1.042   | 0.966     | 0.952     | 0.000        |
| wave_energy                   | 18000.000 | 0.144    | 0.000       | 0.399          | 0.896           | 1.300   | 1.043   | 0.991     | 0.984     | 0.000        |
| california_housing            | 5160.000  | 0.978    | 0.000       | 0.406          | 0.897           | 1.122   | 1.046   | 0.972     | 0.917     | 0.000        |
| auction_verification          | 511.000   | 1.502    | 0.000       | 0.170          | 0.905           | 0.342   | 1.050   | 0.770     | 0.967     | 0.019        |
| pumadyn32nh                   | 2048.000  | -0.050   | 0.000       | 0.611          | 0.888           | 2.148   | 1.065   | 0.997     | 1.000     | 0.000        |
| superconductivity             | 5316.000  | 0.860    | 0.000       | 0.293          | 0.890           | 0.674   | 1.065   | 0.915     | 0.810     | 0.001        |
| brazilian_houses              | 2673.000  | 58.953   | 0.000       | 1.261          | 0.899           | 0.550   | 1.094   | 0.912     | 0.812     | 0.000        |
| airfoil_self_noise            | 376.000   | -0.419   | 0.000       | 0.278          | 0.876           | 0.951   | 1.110   | 0.912     | 0.936     | 0.001        |
| health_insurance              | 5568.000  | -0.342   | 0.299       | 0.778          | 0.893           | 2.176   | 1.113   | 0.964     | 0.876     | 0.000        |
| kings_county                  | 5403.000  | 4.024    | 0.000       | 0.333          | 0.896           | 0.774   | 1.139   | 0.951     | 0.834     | 0.000        |
| diamonds                      | 13485.000 | 1.618    | 0.000       | 0.142          | 0.896           | 0.301   | 1.171   | 0.969     | 0.887     | 0.000        |
| concrete_compressive_strength | 258.000   | 0.416    | 0.000       | 0.297          | 0.886           | 1.137   | 1.184   | 0.950     | 1.037     | 0.000        |
| space_ga                      | 777.000   | -1.020   | 0.000       | 0.557          | 0.896           | 2.015   | 1.194   | 0.972     | 1.002     | 0.000        |
| video_transcoding             | 17196.000 | 4.245    | 0.000       | 0.068          | 0.895           | 0.112   | 1.194   | 0.886     | 0.919     | 0.006        |
| miami_housing                 | 3483.000  | 3.215    | 0.000       | 0.280          | 0.900           | 0.594   | 1.196   | 0.944     | 0.755     | 0.000        |
| abalone                       | 1044.000  | 1.114    | 0.000       | 0.649          | 0.903           | 2.418   | 1.254   | 0.960     | 0.969     | 0.000        |
| energy_efficiency             | 192.000   | 0.360    | 0.000       | 0.061          | 0.855           | 0.322   | 1.291   | 0.902     | 0.917     | 0.030        |
| QSAR_fish_toxicity            | 227.000   | 0.252    | 0.000       | 0.622          | 0.881           | 2.750   | 1.334   | 1.008     | 1.002     | 0.000        |
| geographical_origin_of_music  | 265.000   | -0.990   | 0.000       | 0.901          | 0.886           | 3.779   | 1.350   | 0.991     | 0.968     | 0.000        |
| fifa                          | 4794.000  | 6.472    | 0.000       | 0.481          | 0.896           | 0.853   | 1.381   | 0.931     | 0.455     | 0.000        |
| cps88wages                    | 7039.000  | 6.504    | 0.000       | 0.820          | 0.895           | 2.670   | 1.466   | 0.999     | 0.838     | 0.000        |
| cars                          | 201.000   | 1.573    | 0.000       | 0.272          | 0.887           | 1.362   | 1.503   | 1.199     | 1.313     | 0.000        |
| socmob                        | 289.000   | 4.429    | 0.201       | 0.491          | 0.899           | 1.812   | 2.022   | 1.637     | 0.531     | 0.012        |
| forest_fires                  | 129.000   | 12.810   | 0.478       | 0.403          | 0.860           | 5.937   | 8.752   | 1.029     | 1.012     | 0.000        |

**Table S12.** Lower-tail alerts (means over datasets).

| rule       | recall   | rate   | precision   | cost_r1   | cost_r5   | cost_r10   | cost_r20   | n_ds_recall_ge_0.9   |
|:-----------|:---------|:-------|:------------|:----------|:----------|:-----------|:-----------|:---------------------|
| BCCP       | 0.974    | 0.401  | 0.399       | 0.266     | 0.280     | 0.298      | 0.333      | 31                   |
| CQR        | 0.960    | 0.328  | 0.459       | 0.194     | 0.211     | 0.232      | 0.274      | 29                   |
| CS-BH-0.1  | 0.341    | 0.039  | 0.829       | 0.112     | 0.543     | 1.082      | 2.159      | 5                    |
| CS-BH-0.2  | 0.476    | 0.063  | 0.777       | 0.103     | 0.466     | 0.920      | 1.828      | 6                    |
| HPD-split  | 0.962    | 0.366  | 0.420       | 0.232     | 0.248     | 0.268      | 0.308      | 30                   |
| Point      | 0.573    | 0.102  | 0.779       | 0.098     | 0.374     | 0.720      | 1.410      | 6                    |
| S-CQR      | 0.984    | 0.428  | 0.412       | 0.289     | 0.297     | 0.307      | 0.327      | 31                   |
| S-NCP      | 0.979    | 0.411  | 0.389       | 0.275     | 0.286     | 0.299      | 0.327      | 31                   |
| SCP        | 0.961    | 0.395  | 0.386       | 0.260     | 0.276     | 0.296      | 0.335      | 28                   |
| SDLC       | 0.975    | 0.403  | 0.399       | 0.267     | 0.280     | 0.295      | 0.326      | 31                   |
| SDLC-floor | 0.973    | 0.397  | 0.399       | 0.261     | 0.273     | 0.289      | 0.319      | 30                   |
| TC-H       | 0.905    | 0.272  | 0.537       | 0.156     | 0.210     | 0.277      | 0.410      | 21                   |
| TC-LS      | 0.906    | 0.284  | 0.538       | 0.169     | 0.224     | 0.292      | 0.427      | 16                   |

**Table S13.** Calibration and prediction time per test point (median over datasets of the per-dataset median of three repetitions after a discarded warm-up; one thread).

| Method          | Median µs per test point   | Maximum over datasets   |
|:----------------|:---------------------------|:------------------------|
| CQR             | 0.0                        | 0.1                     |
| DCP-hist        | 3.9                        | 9.4                     |
| DCP             | 0.3                        | 2.4                     |
| DCP-2p          | 0.3                        | 2.1                     |
| DCP-N           | 0.3                        | 2.0                     |
| DLS-hist        | 0.4                        | 0.7                     |
| DLS             | 13.4                       | 75.0                    |
| DLS-2p          | 16.5                       | 55.4                    |
| DLS-N           | 4.7                        | 34.8                    |
| HPD-split-hist  | 12.4                       | 28.4                    |
| HPD-split       | 12.3                       | 79.7                    |
| HPD-split-LS2   | 17.6                       | 50.7                    |
| HPD-split-N     | 4.3                        | 37.2                    |
| Mondrian-ŷ      | 0.2                        | 0.9                     |
| NCP             | 0.0                        | 0.1                     |
| S-CQR           | 0.1                        | 0.3                     |
| S-HPD-hist      | 14.3                       | 30.7                    |
| S-HPD           | 13.4                       | 78.5                    |
| S-HPD-LS2       | 17.7                       | 51.2                    |
| S-HPD-N         | 4.6                        | 33.5                    |
| S-NCP           | 0.1                        | 0.4                     |
| BCCP            | 0.1                        | 0.3                     |
| BCCP-hull       | 0.1                        | 0.2                     |
| SCP             | 0.0                        | 0.1                     |
| SDLC-hist       | 0.4                        | 0.5                     |
| SDLC-hist-floor | 0.3                        | 0.7                     |
| SDLC-hist-hull  | 0.3                        | 0.7                     |
| SDLC            | 12.8                       | 77.3                    |
| SDLC-2p         | 16.7                       | 54.7                    |
| SDLC-N          | 5.1                        | 35.1                    |

**Table S13c.** Fit and prediction time in seconds per model component (seed 0, one thread; n_pred = calibration plus test points).

| dataset                       | n_train   | n_pred   | fit_mean   | fit_scale_with_oof   | fit_scale_crossfit   | fit_kde   | build_table   | fit_quantile_pair   | fit_histogram_classifier   | predict_mean   | predict_scale   | predict_histogram   |
|:------------------------------|:----------|:---------|:-----------|:---------------------|:---------------------|:----------|:--------------|:--------------------|:---------------------------|:---------------|:----------------|:--------------------|
| Moneyball                     | 616       | 616      | 0.065      | 0.131                | 0.037                | 0.074     | 0.001         | 0.070               | 0.339                      | 0.012          | 0.001           | 0.033               |
| abalone                       | 2088      | 2089     | 0.051      | 0.155                | 0.104                | 0.002     | 0.001         | 0.098               | 0.345                      | 0.010          | 0.005           | 0.046               |
| airfoil_self_noise            | 752       | 751      | 0.174      | 0.299                | 0.075                | 0.002     | 0.001         | 0.118               | 0.229                      | 0.043          | 0.008           | 0.025               |
| auction_verification          | 1022      | 1021     | 0.528      | 0.254                | 0.372                | 0.058     | 0.032         | 0.318               | 0.730                      | 0.292          | 0.024           | 0.333               |
| concrete_compressive_strength | 515       | 515      | 0.137      | 0.179                | 0.066                | 0.002     | 0.001         | 0.130               | 0.319                      | 0.028          | 0.002           | 0.050               |
| energy_efficiency             | 384       | 384      | 0.230      | 0.212                | 0.044                | 0.037     | 0.033         | 0.202               | 0.333                      | 0.056          | 0.005           | 0.091               |
| forest_fires                  | 258       | 259      | 0.008      | 0.031                | 0.026                | 0.002     | 0.001         | 0.013               | 0.092                      | 0.001          | 0.000           | 0.004               |
| physiochemical_protein        | 22865     | 22865    | 2.337      | 7.356                | 3.822                | 0.035     | 0.027         | 2.779               | 18.388                     | 4.160          | 3.065           | 25.951              |
| superconductivity             | 10632     | 10631    | 4.731      | 9.082                | 3.019                | 0.034     | 0.024         | 11.828              | 24.693                     | 0.737          | 0.269           | 3.509               |
| geographical_origin_of_music  | 530       | 529      | 0.165      | 0.862                | 0.385                | 0.002     | 0.001         | 0.421               | 5.631                      | 0.002          | 0.007           | 0.221               |
| naval_propulsion_plant        | 5967      | 5967     | 1.609      | 4.901                | 0.321                | 0.002     | 0.001         | 3.302               | 5.417                      | 1.630          | 0.007           | 3.093               |
| QSAR_fish_toxicity            | 454       | 454      | 0.030      | 0.053                | 0.025                | 0.002     | 0.001         | 0.040               | 0.160                      | 0.003          | 0.001           | 0.011               |
| grid_stability                | 5000      | 5000     | 0.963      | 3.298                | 0.335                | 0.002     | 0.001         | 3.298               | 3.441                      | 0.390          | 0.031           | 1.361               |
| video_transcoding             | 34392     | 34392    | 4.436      | 17.316               | 2.284                | 0.039     | 0.030         | 9.715               | 53.635                     | 6.275          | 0.733           | 55.618              |
| wave_energy                   | 36000     | 36000    | 9.896      | 31.339               | 3.146                | 0.004     | 0.001         | 9.147               | 54.971                     | 8.287          | 0.268           | 37.123              |
| sarcos                        | 24466     | 24467    | 5.360      | 20.435               | 2.439                | 0.003     | 0.001         | 9.767               | 37.204                     | 5.647          | 0.601           | 28.898              |
| california_housing            | 10320     | 10320    | 0.298      | 1.245                | 0.518                | 0.003     | 0.001         | 0.820               | 4.897                      | 0.177          | 0.058           | 4.276               |
| cpu_activity                  | 4096      | 4096     | 0.401      | 1.017                | 0.532                | 0.035     | 0.031         | 0.848               | 3.026                      | 0.083          | 0.028           | 1.013               |
| diamonds                      | 26970     | 26970    | 0.568      | 2.121                | 0.686                | 0.004     | 0.001         | 3.277               | 19.043                     | 0.259          | 0.135           | 22.698              |
| kin8nm                        | 4096      | 4096     | 0.646      | 1.986                | 0.328                | 0.002     | 0.001         | 0.313               | 3.107                      | 0.281          | 0.010           | 1.261               |
| pumadyn32nh                   | 4096      | 4096     | 0.340      | 1.116                | 0.444                | 0.002     | 0.001         | 0.833               | 5.994                      | 0.016          | 0.001           | 0.443               |
| miami_housing                 | 6966      | 6966     | 0.509      | 2.835                | 0.372                | 0.002     | 0.001         | 1.317               | 5.758                      | 0.183          | 0.076           | 2.751               |
| cps88wages                    | 14078     | 14077    | 0.143      | 0.507                | 0.276                | 0.003     | 0.001         | 0.305               | 3.830                      | 0.050          | 0.029           | 2.553               |
| socmob                        | 578       | 578      | 0.084      | 0.101                | 0.066                | 0.034     | 0.034         | 0.088               | 0.301                      | 0.019          | 0.005           | 0.040               |
| kings_county                  | 10806     | 10807    | 0.949      | 1.938                | 0.514                | 0.003     | 0.001         | 1.280               | 8.675                      | 0.497          | 0.047           | 4.707               |
| brazilian_houses              | 5346      | 5346     | 0.056      | 1.860                | 1.703                | 0.033     | 0.032         | 0.182               | 2.455                      | 0.004          | 0.002           | 1.121               |
| fps_benchmark                 | 12312     | 12312    | 2.634      | 9.607                | 2.448                | 0.039     | 0.030         | 7.194               | 15.065                     | 2.805          | 0.449           | 10.476              |
| health_insurance              | 11136     | 11136    | 0.115      | 0.544                | 0.503                | 0.003     | 0.001         | 0.628               | 1.353                      | 0.029          | 0.049           | 0.554               |
| cars                          | 402       | 402      | 0.016      | 0.132                | 0.165                | 0.040     | 0.029         | 0.061               | 0.180                      | 0.002          | 0.001           | 0.017               |
| fifa                          | 9589      | 9589     | 0.361      | 0.854                | 0.379                | 0.002     | 0.001         | 0.845               | 4.290                      | 0.066          | 0.045           | 2.057               |
| space_ga                      | 1554      | 1553     | 0.075      | 0.320                | 0.160                | 0.002     | 0.001         | 0.126               | 0.698                      | 0.014          | 0.003           | 0.062               |

**Table S13b.** Splits that keep repeated units together (sarcos: duplicates removed; video transcoding: grouped by input video; superconductivity: grouped by feature vector) against the random splits of the same seeds (0-4, $\alpha=0.1$). Size in target standard deviations (geometric mean).

| dataset           | split       | method    | coverage_grouped   | coverage_random   | worst_grouped   | worst_random   | size_grouped   | size_random   |
|:------------------|:------------|:----------|:-------------------|:------------------|:----------------|:---------------|:---------------|:--------------|
| superconductivity | by_features | SCP       | 0.901              | 0.897             | 0.819           | 0.803          | 0.785          | 0.754         |
| superconductivity | by_features | CQR       | 0.897              | 0.900             | 0.777           | 0.751          | 1.015          | 1.006         |
| superconductivity | by_features | HPD-split | 0.897              | 0.900             | 0.876           | 0.881          | 0.768          | 0.720         |
| superconductivity | by_features | BCCP      | 0.903              | 0.898             | 0.891           | 0.889          | 0.852          | 0.831         |
| superconductivity | by_features | S-NCP     | 0.897              | 0.903             | 0.879           | 0.889          | 0.767          | 0.730         |
| superconductivity | by_features | S-CQR     | 0.897              | 0.901             | 0.890           | 0.882          | 1.025          | 1.010         |
| superconductivity | by_features | SDLC      | 0.899              | 0.900             | 0.890           | 0.894          | 0.701          | 0.674         |
| video_transcoding | by_video    | SCP       | 0.896              | 0.901             | 0.431           | 0.466          | 0.503          | 0.126         |
| video_transcoding | by_video    | CQR       | 0.892              | 0.900             | 0.700           | 0.857          | 0.466          | 0.253         |
| video_transcoding | by_video    | HPD-split | 0.920              | 0.900             | 0.766           | 0.897          | 0.726          | 0.130         |
| video_transcoding | by_video    | BCCP      | 0.875              | 0.900             | 0.852           | 0.895          | 0.643          | 0.123         |
| video_transcoding | by_video    | S-NCP     | 0.917              | 0.901             | 0.904           | 0.893          | 0.878          | 0.127         |
| video_transcoding | by_video    | S-CQR     | 0.873              | 0.899             | 0.855           | 0.895          | 0.516          | 0.259         |
| video_transcoding | by_video    | SDLC      | 0.900              | 0.900             | 0.873           | 0.897          | 0.775          | 0.113         |
| sarcos            | dedup       | SCP       | 0.898              | 0.900             | 0.787           | 0.796          | 0.414          | 0.395         |
| sarcos            | dedup       | CQR       | 0.902              | 0.901             | 0.821           | 0.834          | 0.582          | 0.556         |
| sarcos            | dedup       | HPD-split | 0.898              | 0.901             | 0.889           | 0.891          | 0.385          | 0.382         |
| sarcos            | dedup       | BCCP      | 0.900              | 0.901             | 0.895           | 0.899          | 0.419          | 0.398         |
| sarcos            | dedup       | S-NCP     | 0.898              | 0.902             | 0.889           | 0.895          | 0.386          | 0.384         |
| sarcos            | dedup       | S-CQR     | 0.904              | 0.900             | 0.900           | 0.898          | 0.586          | 0.559         |
| sarcos            | dedup       | SDLC      | 0.898              | 0.901             | 0.891           | 0.897          | 0.373          | 0.356         |

![**Fig. S1.** Coverage of the upper calibration stratum per dataset ($\alpha=0.1$).](/home/user/p_c1_2/Target_Journal_Submission/figures/F4_upper_tail_per_dataset.png){width=100%}

![**Fig. S2.** Error analysis. Left: price of stratum-wise validity (SDLC/DLS size ratio) against relative RMSE. Right: worst-stratum coverage of SDLC minus its null mean against calibration-set size, with the 5% null band.](/home/user/p_c1_2/Target_Journal_Submission/figures/F8_error_analysis.png){width=100%}

![**Fig. S3.** Effect of the calibration-set size on worst-stratum coverage (left) and size (right).](/home/user/p_c1_2/Target_Journal_Submission/figures/F7_calibration_size.png){width=100%}

# S5. Earlier implementations

The first run (v1) evaluated all density-based sets on a fixed grid of 200 equal-mass cells of the marginal training-target distribution. The second (v2) used an exact implementation but standardised residuals with an in-sample scale model and used a density floor. Their complete analyses are archived in `supplementary/v1_preregistered_analysis/` and `supplementary/v2_exact_insample_analysis/`. The coverage results were the same in all versions. Table S14 shows how the size comparisons changed; this dependence on the implementation is why the comparisons on CTR23 are labelled exploratory and were replicated on held-out data (v1 reported medians of log ratios; v2 also geometric means; the final version reports the Hodges–Lehmann estimate).

**Table S14.** Size comparisons of SDLC with the stratified comparators in the three implementations ($\alpha=0.1$, 31 datasets; negative log ratios favour SDLC).

| Version                     | Comparison    | Median log size ratio   | Geometric-mean ratio   | SDLC smaller on   | Holm p   |
|:----------------------------|:--------------|:------------------------|:-----------------------|:------------------|:---------|
| v1 (marginal grid)          | SDLC vs BCCP  | -0.012                  | not computed           | not computed      | 0.809    |
| v1 (marginal grid)          | SDLC vs S-NCP | +0.023                  | not computed           | not computed      | 0.130    |
| v1 (marginal grid)          | SDLC vs S-CQR | -0.121                  | not computed           | not computed      | 0.196    |
| v1 (marginal grid)          | SDLC vs S-HPD | -0.039                  | not computed           | not computed      | < 0.001  |
| v2 (exact, in-sample scale) | SDLC vs BCCP  | -0.042                  | 0.932                  | 22/31             | 0.017    |
| v2 (exact, in-sample scale) | SDLC vs S-NCP | -0.030                  | 1.004                  | 24/31             | 0.035    |
| v2 (exact, in-sample scale) | SDLC vs S-CQR | -0.121                  | 0.833                  | 26/31             | 0.004    |
| v2 (exact, in-sample scale) | SDLC vs S-HPD | -0.047                  | 0.949                  | 30/31             | < 0.001  |
| final                       | SDLC vs BCCP  | -0.069 (HL)             | 0.902                  | 24/31             | < 0.001  |
| final                       | SDLC vs S-NCP | -0.039 (HL)             | 0.975                  | 27/31             | < 0.001  |
| final                       | SDLC vs S-CQR | -0.190 (HL)             | 0.795                  | 27/31             | < 0.001  |
| final                       | SDLC vs S-HPD | -0.048 (HL)             | 0.947                  | 28/31             | < 0.001  |

# S6. Pre-registered analysis plan of the confirmatory replication

Reproduced verbatim from `PREREGISTRATION_confirmatory.md`, committed to the public repository before any confirmatory evaluation.


**Status.** This document and `code/scripts/analyze_confirmatory.py` are committed to the public repository
(branch `claude/amazing-maxwell-i1mihd`) BEFORE any method has been evaluated on the confirmatory datasets. At the time of the
commit, no confirmatory evaluation file (`results/confirmatory/raw_eval_v3/`) exists. Model fitting for these
datasets (`results/confirmatory/raw_contexts*`) may be in progress; fitting produces only base-model outputs
(point, quantile, scale and histogram predictions) and no conformal-method result. The git history provides
the timestamps. Supplementary S6 of the manuscript reproduces this plan.

### 1. Motivation

On the 31 OpenML-CTR23 datasets, the implementation of the density-based methods was changed twice after
results had been seen (EXPERIMENT_LOG.md items 10–13). Every size comparison between SDLC and other stratified
methods on CTR23 is therefore exploratory. This replication tests those comparisons on data that played no role
in any design decision.

### 2. Data (fixed before this plan: `code/config/confirmatory.json`, commit 1762ec0)

* Source: the regression datasets of the tabular benchmark of Grinsztajn, Oyallon & Varoquaux (2022), OpenML
  suites 335/336.
* Removed: datasets that share source data with CTR23 (cpu_act, houses, house_sales, MiamiHousing2016,
  superconduct, diamonds, Brazilian_houses, abalone, wine_quality), duplicate versions, and targets with fewer
  than 20 distinct values (the main-study rule; analcatdata_supreme, pol).
* Remaining: 17 datasets (OpenML IDs 44056, 44061, 44068, 44069, 44134, 44137, 44139, 44142, 44143, 44145,
  44146, 45032, 45034, 45041, 45043, 45046, 45047). Datasets with more than 50,000 rows are subsampled once to
  50,000 rows with seed 2026.
* Seeds 0–4; split 50/25/25; alpha = 0.1; primary strata S5 (training quantiles 0.10, 0.25, 0.75, 0.90).
* Pipeline: exactly the final (v3) implementation of the main study, with no change to any setting:
  `experiments/run_benchmark.py --mode fitonly`, `experiments/refit_scales.py`,
  `experiments/evaluate_from_cache3.py` with `TSCP_CONFIG=confirmatory.json`.
* A dataset is dropped only if fitting or evaluation fails for software reasons. Any drop is reported with its
  reason. No dataset is dropped because of its results.

### 3. Hypotheses, tests and decision rules

Unit of analysis: the dataset (metrics averaged over the 5 seeds). SDLC = `SDLC-LS`. All tests are Wilcoxon
signed-rank tests over datasets, with Holm's correction within each family, at level 0.05.

| ID | Hypothesis | Test | Decision rule |
|---|---|---|---|
| C-H1 | SDLC has higher worst-stratum coverage than each marginal / covariate-adaptive method (SCP, NCP, CQR, Mondrian-ŷ, DCP, HPD-split, DLS) | one-sided, Holm over 7 | supported iff all 7 Holm p < 0.05 |
| C-H2 | SDLC's worst-stratum coverage is consistent with exact validity | count of datasets below the 5% quantile of the Beta–binomial null reference | consistent iff count ≤ 3 (95% quantile of Binomial(17, 0.05)); one-sided binomial test reported |
| C-H3 | SDLC's set size differs from BCCP, S-NCP, S-CQR and S-HPD | two-sided on log size ratios, Holm over 4 | "favours SDLC" iff Holm p < 0.05 and geometric-mean ratio < 1; "favours comparator" iff Holm p < 0.05 and ratio > 1; otherwise "no difference shown" |
| C-H4 | SDLC's worst-stratum coverage is equivalent to S-NCP's and BCCP's | TOST (two one-sided Wilcoxon tests), margin 0.02 | equivalent iff p_TOST < 0.05 |

Effect sizes are reported for every comparison: geometric-mean size ratio with a 95% bootstrap CI (10,000
resamples of datasets), the Hodges–Lehmann ratio with its 95% CI, wins/losses and the sign test.

### 4. Secondary, descriptive analyses (no decision rule)

Price of stratification (SDLC vs DLS); upper-tail, top-5% and top-1% coverage; empty-set rate; worst
sigma-hat-decile coverage; the C-H3 comparisons under decile strata (S10); hull variants.

### 5. Reporting

Results are reported in the manuscript (Section "Confirmatory replication") and in
`results/confirmatory/statistics_confirmatory.json`, whatever their direction. If C-H3 does not favour SDLC
against a comparator, the abstract and conclusions will say so.
