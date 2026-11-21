---
title: "Supplementary Material: Covering rare outcomes in imbalanced regression with conformal prediction: guarantees, size-optimal scores and what tail coverage costs"
---

# S1. Datasets

**Table S1.** The OpenML-CTR23 datasets used in the main benchmark: size, number of features after one-hot encoding, skewness and number of distinct values of the target, realised number of calibration strata $K$, realised training mass of the lowest and highest stratum (nominal 0.10), relative test RMSE of the point model, licence as recorded by OpenML ("not stated" where OpenML records none), and the share of test targets outside the domain $\mathcal{Y}_D$ (automatic misses; mean and maximum over seeds).

| OpenML ID   | Dataset                       | n      | p   | Skewness   | Distinct y   | K   | Lower mass   | Upper mass   | RMSE/sd   | Licence                                         | Out-of-domain test targets, % (mean/max)   |
|:------------|:------------------------------|:-------|:----|:-----------|:-------------|:----|:-------------|:-------------|:----------|:------------------------------------------------|:-------------------------------------------|
| 44962       | forest fires                  | 517    | 31  | 12.81      | 251          | 3   | 0.744        | 0.105        | 0.40      | CC BY 4.0                                       | 0.38/2.31                                  |
| 44960       | energy efficiency             | 768    | 8   | 0.36       | 587          | 5   | 0.099        | 0.104        | 0.06      | CC BY 4.0                                       | 0.00/0.00                                  |
| 44994       | cars                          | 804    | 17  | 1.57       | 798          | 5   | 0.100        | 0.104        | 0.27      | not stated (OpenML: "Public")                   | 0.10/0.50                                  |
| 44970       | QSAR fish toxicity            | 908    | 6   | 0.25       | 827          | 5   | 0.099        | 0.103        | 0.62      | CC BY 4.0                                       | 0.04/0.44                                  |
| 44959       | concrete compressive strength | 1,030  | 8   | 0.42       | 938          | 5   | 0.099        | 0.103        | 0.30      | CC BY 4.0                                       | 0.00/0.00                                  |
| 44965       | geographical origin of music  | 1,059  | 116 | -0.99      | 31           | 5   | 0.084        | 0.117        | 0.90      | CC BY 4.0                                       | 0.00/0.00                                  |
| 44987       | socmob                        | 1,156  | 43  | 4.43       | 361          | 4   | 0.240        | 0.102        | 0.49      | Non-commercial scholarly and teaching purposes. | 0.00/0.00                                  |
| 41021       | Moneyball                     | 1,232  | 78  | 0.17       | 374          | 5   | 0.099        | 0.103        | 0.27      | not stated (OpenML: "Public")                   | 0.03/0.32                                  |
| 44957       | airfoil self noise            | 1,503  | 5   | -0.42      | 1,456        | 5   | 0.100        | 0.102        | 0.28      | CC BY 4.0                                       | 0.00/0.00                                  |
| 44958       | auction verification          | 2,043  | 18  | 1.50       | 2,039        | 5   | 0.100        | 0.102        | 0.17      | CC BY 4.0                                       | 0.00/0.00                                  |
| 45402       | space ga                      | 3,107  | 6   | -1.02      | 3,105        | 5   | 0.100        | 0.101        | 0.56      | not stated (OpenML: "Public")                   | 0.13/0.39                                  |
| 44956       | abalone                       | 4,177  | 11  | 1.11       | 28           | 5   | 0.045        | 0.114        | 0.65      | CC BY 4.0                                       | 0.03/0.10                                  |
| 44978       | cpu activity                  | 8,192  | 21  | -3.42      | 56           | 5   | 0.096        | 0.104        | 0.13      | not stated (OpenML: "Public")                   | 0.00/0.00                                  |
| 44981       | pumadyn32nh                   | 8,192  | 32  | -0.05      | 8,191        | 5   | 0.100        | 0.100        | 0.61      | not stated (OpenML: "Public")                   | 0.01/0.05                                  |
| 44980       | kin8nm                        | 8,192  | 8   | 0.09       | 8,191        | 5   | 0.100        | 0.100        | 0.47      | not stated (OpenML: "Public")                   | 0.00/0.00                                  |
| 44973       | grid stability                | 10,000 | 12  | 0.02       | 10,000       | 5   | 0.100        | 0.100        | 0.22      | CC BY 4.0                                       | 0.01/0.04                                  |
| 44990       | brazilian houses              | 10,692 | 53  | 58.95      | 5,751        | 5   | 0.100        | 0.100        | 1.26      | CC 0: Public Domain                             | 0.01/0.07                                  |
| 44969       | naval propulsion plant        | 11,934 | 14  | -0.00      | 51           | 5   | 0.096        | 0.117        | 0.06      | CC BY 4.0                                       | 0.00/0.00                                  |
| 44983       | miami housing                 | 13,932 | 15  | 3.22       | 2,111        | 5   | 0.099        | 0.100        | 0.28      | CC0: Public Domain                              | 0.00/0.00                                  |
| 45012       | fifa                          | 19,178 | 191 | 6.47       | 133          | 4   | 0.207        | 0.103        | 0.48      | CC0: Public Domain                              | 0.01/0.04                                  |
| 44977       | california housing            | 20,640 | 8   | 0.98       | 3,842        | 5   | 0.100        | 0.100        | 0.41      | not stated (OpenML: "Public")                   | 0.00/0.00                                  |
| 44964       | superconductivity             | 21,263 | 81  | 0.86       | 3,007        | 5   | 0.100        | 0.101        | 0.29      | CC BY 4.0                                       | 0.01/0.02                                  |
| 44989       | kings county                  | 21,613 | 136 | 4.02       | 4,028        | 5   | 0.098        | 0.100        | 0.33      | CC 0: Public Domain                             | 0.00/0.02                                  |
| 44993       | health insurance              | 22,272 | 32  | -0.34      | 75           | 2   | 0.555        | 0.442        | 0.78      | GPL (>= 2)                                      | 0.01/0.04                                  |
| 44992       | fps benchmark                 | 24,624 | 971 | 1.05       | 2,675        | 5   | 0.100        | 0.100        | 0.02      | CC BY                                           | 0.00/0.00                                  |
| 44984       | cps88wages                    | 28,155 | 16  | 6.50       | 5,970        | 5   | 0.100        | 0.107        | 0.82      | not stated (OpenML: "Public")                   | 0.00/0.01                                  |
| 44963       | physiochemical protein        | 45,730 | 9   | 0.57       | 15,903       | 5   | 0.100        | 0.100        | 0.61      | CC BY 4.0                                       | 0.00/0.00                                  |
| 44976       | sarcos                        | 48,933 | 21  | 0.15       | 11,414       | 5   | 0.100        | 0.100        | 0.13      | not stated (OpenML: "Public")                   | 0.00/0.00                                  |
| 44979       | diamonds                      | 53,940 | 29  | 1.62       | 11,602       | 5   | 0.099        | 0.100        | 0.14      | not stated (OpenML: "Public")                   | 0.00/0.00                                  |
| 44974       | video transcoding             | 68,784 | 26  | 4.25       | 10,960       | 5   | 0.100        | 0.100        | 0.07      | CC BY 4.0                                       | 0.00/0.01                                  |
| 44975       | wave energy                   | 72,000 | 36  | 0.14       | 71,993       | 5   | 0.100        | 0.100        | 0.40      | CC BY 4.0                                       | 0.00/0.00                                  |

**Table S2.** Held-out datasets of the confirmatory replication (regression datasets of OpenML suites 335/336 without source overlap with CTR23; datasets above 50,000 rows subsampled once with seed 2026; "Distinct y" on the subsample, "Distinct y (full)" on the full data, the quantity the exclusion rule uses; realised stratum masses as ranges over seeds, nominal 0.10; "Log scale (curated)": the benchmark curators supplied the logarithm of the original quantity). yprop_4_1 and topo_2_1 contain identical observations and targets. visualizing_soil (transect index) and seattlecrime6 (coded time of day) have coded rather than quantitative targets. In house_16H, 52 records with log-price 0 form the whole lowest stratum; in yprop_4_1/topo_2_1 a single record has y = 0 while all others lie in [0.845, 1]. Excluded by content overlap: cpu_act (cpu_activity); houses (california_housing); house_sales (kings_county); MiamiHousing2016 (miami_housing); superconduct (superconductivity); diamonds; Brazilian_houses; abalone; wine_quality (wine). Excluded by the distinct-value rule: 44055 analcatdata_supreme; 44133 pol.

| OpenML ID   | Dataset                             | n (used)   | p    | Distinct y   | Licence                       | n (full)   | Distinct y (full)   | Largest atom   | Skewness (full)   | Log scale (curated)   | K   | Lowest stratum mass   | Highest stratum mass   | Min. calibration points per stratum   | Out-of-domain test targets, % (max)   |
|:------------|:------------------------------------|:-----------|:-----|:-------------|:------------------------------|:-----------|:--------------------|:---------------|:------------------|:----------------------|:----|:----------------------|:-----------------------|:--------------------------------------|:--------------------------------------|
| 44056       | visualizing_soil                    | 8,641      | 6    | 40           | not stated (OpenML: "Public") | 8,641      | 40                  | 0.070          | 0.33              | no                    | 5   | 0.043-0.049           | 0.110-0.112            | 88                                    | 0.00                                  |
| 44061       | Mercedes_Benz_Greener_Manufacturing | 4,209      | 1094 | 2,545        | not stated (OpenML: "Public") | 4,209      | 2,545               | 0.002          | 1.21              | no                    | 5   | 0.100-0.100           | 0.101-0.102            | 97                                    | 0.19                                  |
| 44068       | particulate-matter-ukair-2017       | 50,000     | 29   | 6,195        | Open Government Licence (OGL) | 394,299    | 21,599              | 0.005          | -0.54             | no                    | 5   | 0.096-0.100           | 0.100-0.101            | 1196                                  | 0.01                                  |
| 44069       | SGEMM_GPU_kernel_performance        | 50,000     | 21   | 23,831       | CC BY 4.0                     | 241,600    | 58,161              | 0.000          | 0.79              | yes                   | 5   | 0.100-0.100           | 0.100-0.100            | 1190                                  | 0.00                                  |
| 44134       | elevators                           | 16,599     | 16   | 61           | not stated (OpenML: "Public") | 16,599     | 61                  | 0.151          | 2.42              | no                    | 5   | 0.036-0.100           | 0.104-0.110            | 148                                   | 0.02                                  |
| 44137       | Ailerons                            | 13,750     | 33   | 35           | not stated (OpenML: "Public") | 13,750     | 35                  | 0.135          | -1.35             | no                    | 5   | 0.091-0.098           | 0.211-0.222            | 287                                   | 0.12                                  |
| 44139       | house_16H                           | 22,784     | 16   | 2,045        | not stated (OpenML: "Public") | 22,784     | 2,045               | 0.137          | -3.43             | yes                   | 5   | 0.002-0.003           | 0.100-0.100            | 10                                    | 0.00                                  |
| 44142       | Bike_Sharing_Demand                 | 17,379     | 6    | 869          | not stated (OpenML: "Public") | 17,379     | 869                 | 0.015          | 1.28              | no                    | 5   | 0.092-0.098           | 0.100-0.101            | 407                                   | 0.00                                  |
| 44143       | nyc-taxi-green-dec-2016             | 50,000     | 9    | 957          | not stated (OpenML: "Public") | 581,835    | 1,811               | 0.152          | -0.00             | yes                   | 4   | 0.181-0.250           | 0.100-0.101            | 1155                                  | 0.00                                  |
| 44145       | sulfur                              | 10,081     | 6    | 9,368        | not stated (OpenML: "Public") | 10,081     | 9,368               | 0.003          | 6.72              | no                    | 5   | 0.100-0.100           | 0.100-0.100            | 221                                   | 0.08                                  |
| 44146       | medical_charges                     | 50,000     | 3    | 49,061       | Public Domain (CC0)           | 163,065    | 154,891             | 0.000          | 0.88              | no                    | 5   | 0.100-0.100           | 0.100-0.100            | 1191                                  | 0.01                                  |
| 45032       | yprop_4_1                           | 8,885      | 42   | 1,336        | not stated (OpenML: "Public") | 8,885      | 1,336               | 0.005          | -2.23             | no                    | 5   | 0.100-0.100           | 0.100-0.101            | 195                                   | 0.05                                  |
| 45034       | delays_zurich_transport             | 50,000     | 8    | 1,019        | CCZero                        | 5,465,575  | 4,082               | 0.009          | -0.87             | yes                   | 5   | 0.096-0.100           | 0.100-0.101            | 1121                                  | 0.00                                  |
| 45041       | topo_2_1                            | 8,885      | 261  | 1,336        | not stated (OpenML: "Public") | 8,885      | 1,336               | 0.005          | -2.23             | no                    | 5   | 0.100-0.100           | 0.100-0.101            | 195                                   | 0.05                                  |
| 45043       | seattlecrime6                       | 50,000     | 26   | 29           | CC0                           | 52,031     | 29                  | 0.062          | -0.42             | no                    | 5   | 0.064-0.100           | 0.117-0.124            | 780                                   | 0.00                                  |
| 45046       | Allstate_Claims_Severity            | 50,000     | 587  | 47,550       | not stated (OpenML: "Public") | 188,318    | 158,223             | 0.001          | 0.10              | yes                   | 5   | 0.100-0.100           | 0.100-0.100            | 1190                                  | 0.02                                  |
| 45047       | Airlines_DepDelay_1M                | 50,000     | 5    | 330          | CC0                           | 1,000,000  | 629                 | 0.189          | 0.52              | yes                   | 5   | 0.090-0.095           | 0.101-0.102            | 1126                                  | 0.02                                  |

# S2. Leakage audit

Exact duplicate rows (features and target), duplicate feature vectors, the share of test feature vectors that also occur in the training split (seed 0), and the share of missing values, recomputed on the final data files (scripts/leakage_audit.py), for the CTR23 and the held-out datasets; the share of test feature vectors seen in training is given for seed 0 and as the range over all seeds. Random splitting keeps rows exchangeable, so the coverage guarantees hold for new rows from the same pool; repeated units (duplicates, repeated videos, repeat sales) mean that they do not transfer to new units.

**Table S3.** Leakage audit (sorted by the share of test feature vectors seen in training).

| Suite    | Dataset                             | n     | Duplicate rows   | Duplicate feature vectors   | Test feature vectors seen in training (seed 0)   | Min over seeds   | Max over seeds   | Missing values   |
|:---------|:------------------------------------|:------|:-----------------|:----------------------------|:-------------------------------------------------|:-----------------|:-----------------|:-----------------|
| held-out | seattlecrime6                       | 50000 | 0.8703           | 0.9914                      | 0.9988                                           | 0.9982           | 0.9989           | 0.0000           |
| held-out | delays_zurich_transport             | 50000 | 0.0399           | 0.9322                      | 0.9952                                           | 0.9952           | 0.9968           | 0.0000           |
| ctr23    | cps88wages                          | 28155 | 0.0756           | 0.7740                      | 0.8245                                           | 0.8245           | 0.8377           | 0.0000           |
| ctr23    | superconductivity                   | 21263 | 0.0031           | 0.2866                      | 0.3138                                           | 0.2992           | 0.3187           | 0.0000           |
| held-out | Mercedes_Benz_Greener_Manufacturing | 4209  | 0.0002           | 0.2186                      | 0.2469                                           | 0.2365           | 0.2469           | 0.0000           |
| ctr23    | QSAR_fish_toxicity                  | 908   | 0.0011           | 0.1465                      | 0.1542                                           | 0.1322           | 0.2203           | 0.0000           |
| ctr23    | sarcos                              | 48933 | 0.0909           | 0.0909                      | 0.0908                                           | 0.0873           | 0.0963           | 0.0000           |
| ctr23    | health_insurance                    | 22272 | 0.0436           | 0.0798                      | 0.0875                                           | 0.0828           | 0.0938           | 0.0000           |
| ctr23    | brazilian_houses                    | 10692 | 0.0337           | 0.0677                      | 0.0849                                           | 0.0707           | 0.0849           | 0.0000           |
| ctr23    | physiochemical_protein              | 45730 | 0.0374           | 0.0384                      | 0.0396                                           | 0.0379           | 0.0420           | 0.0000           |
| ctr23    | concrete_compressive_strength       | 1030  | 0.0243           | 0.0330                      | 0.0233                                           | 0.0233           | 0.0623           | 0.0000           |
| ctr23    | forest_fires                        | 517   | 0.0077           | 0.0251                      | 0.0231                                           | 0.0154           | 0.0385           | 0.0000           |
| held-out | Bike_Sharing_Demand                 | 17379 | 0.0006           | 0.0227                      | 0.0228                                           | 0.0221           | 0.0258           | 0.0000           |
| held-out | yprop_4_1                           | 8885  | 0.0000           | 0.0125                      | 0.0122                                           | 0.0108           | 0.0135           | 0.0000           |
| ctr23    | diamonds                            | 53940 | 0.0027           | 0.0064                      | 0.0065                                           | 0.0056           | 0.0076           | 0.0000           |
| ctr23    | cars                                | 804   | 0.0000           | 0.0012                      | 0.0050                                           | 0.0000           | 0.0050           | 0.0000           |
| held-out | topo_2_1                            | 8885  | 0.0000           | 0.0028                      | 0.0027                                           | 0.0027           | 0.0036           | 0.0000           |
| held-out | particulate-matter-ukair-2017       | 50000 | 0.0000           | 0.0016                      | 0.0019                                           | 0.0010           | 0.0020           | 0.0000           |
| held-out | nyc-taxi-green-dec-2016             | 50000 | 0.0010           | 0.0012                      | 0.0013                                           | 0.0010           | 0.0018           | 0.0000           |
| ctr23    | video_transcoding                   | 68784 | 0.0000           | 0.0012                      | 0.0010                                           | 0.0008           | 0.0015           | 0.0000           |
| ctr23    | miami_housing                       | 13932 | 0.0000           | 0.0007                      | 0.0003                                           | 0.0000           | 0.0014           | 0.0000           |
| held-out | SGEMM_GPU_kernel_performance        | 50000 | 0.0001           | 0.0003                      | 0.0002                                           | 0.0001           | 0.0003           | 0.0000           |
| ctr23    | wave_energy                         | 72000 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | energy_efficiency                   | 768   | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | Moneyball                           | 1232  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0169           |
| ctr23    | grid_stability                      | 10000 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | geographical_origin_of_music        | 1059  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | naval_propulsion_plant              | 11934 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | auction_verification                | 2043  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | airfoil_self_noise                  | 1503  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | abalone                             | 4177  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | kin8nm                              | 8192  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | visualizing_soil                    | 8641  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | space_ga                            | 3107  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | fifa                                | 19178 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | fps_benchmark                       | 24624 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0029           |
| ctr23    | kings_county                        | 21613 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0002           | 0.0000           |
| ctr23    | cpu_activity                        | 8192  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | pumadyn32nh                         | 8192  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | socmob                              | 1156  | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| ctr23    | california_housing                  | 20640 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | Ailerons                            | 13750 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | elevators                           | 16599 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | house_16H                           | 22784 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | sulfur                              | 10081 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | medical_charges                     | 50000 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | Allstate_Claims_Severity            | 50000 | 0.0000           | 0.0000                      | 0.0000                                           | 0.0000           | 0.0000           | 0.0000           |
| held-out | Airlines_DepDelay_1M                | 50000 | 0.0000           | 0.0001                      | 0.0000                                           | 0.0000           | 0.0002           | 0.0000           |

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
| naval_propulsion_plant        | 2984.000  | 0.000    | 0.000       | 0.060          | 0.891           | 0.168   | 1.002   | 0.954     | 0.995     | 0.018        |
| kin8nm                        | 2048.000  | 0.090    | 0.000       | 0.472          | 0.883           | 1.491   | 1.012   | 0.990     | 0.953     | 0.000        |
| sarcos                        | 12233.000 | 0.152    | 0.002       | 0.130          | 0.896           | 0.356   | 1.013   | 0.942     | 0.898     | 0.001        |
| fps_benchmark                 | 6156.000  | 1.053    | 0.000       | 0.022          | 0.892           | 0.059   | 1.024   | 0.911     | 0.988     | 0.021        |
| physiochemical_protein        | 11432.000 | 0.567    | 0.006       | 0.607          | 0.898           | 1.673   | 1.026   | 0.970     | 0.903     | 0.000        |
| Moneyball                     | 308.000   | 0.174    | 0.000       | 0.268          | 0.881           | 0.963   | 1.042   | 0.984     | 1.017     | 0.000        |
| cpu_activity                  | 2048.000  | −3.416   | 0.035       | 0.127          | 0.895           | 0.362   | 1.042   | 0.966     | 0.952     | 0.000        |
| wave_energy                   | 18000.000 | 0.144    | 0.000       | 0.399          | 0.896           | 1.300   | 1.043   | 0.991     | 0.984     | 0.000        |
| california_housing            | 5160.000  | 0.978    | 0.000       | 0.406          | 0.897           | 1.122   | 1.046   | 0.972     | 0.917     | 0.000        |
| auction_verification          | 511.000   | 1.502    | 0.000       | 0.170          | 0.905           | 0.342   | 1.050   | 0.770     | 0.967     | 0.019        |
| pumadyn32nh                   | 2048.000  | −0.050   | 0.000       | 0.611          | 0.888           | 2.148   | 1.065   | 0.997     | 1.000     | 0.000        |
| superconductivity             | 5316.000  | 0.860    | 0.000       | 0.293          | 0.890           | 0.674   | 1.065   | 0.915     | 0.810     | 0.001        |
| brazilian_houses              | 2673.000  | 58.953   | 0.000       | 1.261          | 0.899           | 0.550   | 1.094   | 0.912     | 0.812     | 0.000        |
| airfoil_self_noise            | 376.000   | −0.419   | 0.000       | 0.278          | 0.876           | 0.951   | 1.110   | 0.912     | 0.936     | 0.001        |
| health_insurance              | 5568.000  | −0.342   | 0.299       | 0.778          | 0.893           | 2.176   | 1.113   | 0.964     | 0.876     | 0.000        |
| kings_county                  | 5403.000  | 4.024    | 0.000       | 0.333          | 0.896           | 0.774   | 1.139   | 0.951     | 0.834     | 0.000        |
| diamonds                      | 13485.000 | 1.618    | 0.000       | 0.142          | 0.896           | 0.301   | 1.171   | 0.969     | 0.887     | 0.000        |
| concrete_compressive_strength | 258.000   | 0.416    | 0.000       | 0.297          | 0.886           | 1.137   | 1.184   | 0.950     | 1.037     | 0.000        |
| space_ga                      | 777.000   | −1.020   | 0.000       | 0.557          | 0.896           | 2.015   | 1.194   | 0.972     | 1.002     | 0.000        |
| video_transcoding             | 17196.000 | 4.245    | 0.000       | 0.068          | 0.895           | 0.112   | 1.194   | 0.886     | 0.919     | 0.006        |
| miami_housing                 | 3483.000  | 3.215    | 0.000       | 0.280          | 0.900           | 0.594   | 1.196   | 0.944     | 0.755     | 0.000        |
| abalone                       | 1044.000  | 1.114    | 0.000       | 0.649          | 0.903           | 2.418   | 1.254   | 0.960     | 0.969     | 0.000        |
| energy_efficiency             | 192.000   | 0.360    | 0.000       | 0.061          | 0.855           | 0.322   | 1.291   | 0.902     | 0.917     | 0.030        |
| QSAR_fish_toxicity            | 227.000   | 0.252    | 0.000       | 0.622          | 0.881           | 2.750   | 1.334   | 1.008     | 1.002     | 0.000        |
| geographical_origin_of_music  | 265.000   | −0.990   | 0.000       | 0.901          | 0.886           | 3.779   | 1.350   | 0.991     | 0.968     | 0.000        |
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

**Table S14.** Fitting and prediction time of the model components in seconds (seed 0, one CPU thread). SDLC uses the mean model, the scale model with out-of-fold residuals, the cross-fitted scale models and the kernel density.

| did   | dataset                       | n_train   | n_pred   | fit_mean   | fit_scale_with_oof   | fit_scale_crossfit   | fit_kde   | build_table   | fit_quantile_pair   | fit_histogram_classifier   | predict_mean   | predict_scale   | predict_histogram   |
|:------|:------------------------------|:----------|:---------|:-----------|:---------------------|:---------------------|:----------|:--------------|:--------------------|:---------------------------|:---------------|:----------------|:--------------------|
| 41021 | Moneyball                     | 616       | 616      | 0.092      | 0.145                | 0.037                | 0.080     | 0.001         | 0.077               | 0.377                      | 0.012          | 0.001           | 0.034               |
| 44956 | abalone                       | 2088      | 2089     | 0.080      | 0.196                | 0.139                | 0.005     | 0.001         | 0.123               | 0.419                      | 0.012          | 0.008           | 0.059               |
| 44957 | airfoil_self_noise            | 752       | 751      | 0.187      | 0.293                | 0.078                | 0.002     | 0.001         | 0.135               | 0.247                      | 0.049          | 0.009           | 0.027               |
| 44958 | auction_verification          | 1022      | 1021     | 0.599      | 0.253                | 0.313                | 0.046     | 0.031         | 0.361               | 0.825                      | 0.217          | 0.025           | 0.285               |
| 44959 | concrete_compressive_strength | 515       | 515      | 0.177      | 0.201                | 0.064                | 0.002     | 0.001         | 0.151               | 0.356                      | 0.034          | 0.002           | 0.052               |
| 44960 | energy_efficiency             | 384       | 384      | 0.312      | 0.228                | 0.047                | 0.041     | 0.030         | 0.278               | 0.381                      | 0.052          | 0.004           | 0.075               |
| 44962 | forest_fires                  | 258       | 259      | 0.008      | 0.034                | 0.023                | 0.002     | 0.001         | 0.014               | 0.157                      | 0.001          | 0.001           | 0.004               |
| 44963 | physiochemical_protein        | 22865     | 22865    | 2.629      | 7.609                | 4.125                | 0.037     | 0.029         | 3.209               | 21.010                     | 3.606          | 2.362           | 21.760              |
| 44964 | superconductivity             | 10632     | 10631    | 5.123      | 10.065               | 3.590                | 0.039     | 0.030         | 12.208              | 23.396                     | 0.714          | 0.271           | 2.714               |
| 44965 | geographical_origin_of_music  | 530       | 529      | 0.157      | 0.842                | 0.439                | 0.002     | 0.004         | 0.537               | 6.318                      | 0.002          | 0.008           | 0.215               |
| 44969 | naval_propulsion_plant        | 5967      | 5967     | 2.081      | 5.123                | 0.404                | 0.002     | 0.001         | 3.607               | 5.760                      | 1.447          | 0.009           | 3.056               |
| 44970 | QSAR_fish_toxicity            | 454       | 454      | 0.024      | 0.064                | 0.030                | 0.002     | 0.001         | 0.045               | 0.225                      | 0.004          | 0.001           | 0.012               |
| 44973 | grid_stability                | 5000      | 5000     | 0.993      | 3.297                | 0.356                | 0.002     | 0.001         | 4.300               | 4.547                      | 0.329          | 0.038           | 1.222               |
| 44974 | video_transcoding             | 34392     | 34392    | 4.576      | 17.826               | 2.446                | 0.035     | 0.030         | 12.384              | 53.184                     | 5.642          | 0.900           | 47.243              |
| 44975 | wave_energy                   | 36000     | 36000    | 10.411     | 32.191               | 3.315                | 0.005     | 0.001         | 9.605               | 60.629                     | 6.179          | 0.308           | 30.375              |
| 44976 | sarcos                        | 24466     | 24467    | 5.544      | 20.305               | 2.680                | 0.004     | 0.001         | 10.497              | 39.533                     | 4.518          | 0.686           | 23.936              |
| 44977 | california_housing            | 10320     | 10320    | 0.308      | 1.531                | 0.616                | 0.003     | 0.001         | 0.930               | 5.244                      | 0.193          | 0.064           | 3.247               |
| 44978 | cpu_activity                  | 4096      | 4096     | 0.500      | 1.024                | 0.555                | 0.038     | 0.030         | 0.850               | 3.270                      | 0.092          | 0.031           | 0.723               |
| 44979 | diamonds                      | 26970     | 26970    | 0.562      | 2.199                | 0.627                | 0.004     | 0.001         | 3.410               | 19.468                     | 0.351          | 0.154           | 19.145              |
| 44980 | kin8nm                        | 4096      | 4096     | 0.829      | 2.049                | 0.326                | 0.002     | 0.001         | 0.345               | 3.362                      | 0.262          | 0.011           | 1.002               |
| 44981 | pumadyn32nh                   | 4096      | 4096     | 0.312      | 1.010                | 0.461                | 0.002     | 0.001         | 0.863               | 5.765                      | 0.020          | 0.002           | 0.342               |
| 44983 | miami_housing                 | 6966      | 6966     | 0.470      | 2.616                | 0.402                | 0.002     | 0.001         | 1.464               | 5.658                      | 0.195          | 0.086           | 2.265               |
| 44984 | cps88wages                    | 14078     | 14077    | 0.142      | 0.562                | 0.305                | 0.003     | 0.001         | 0.368               | 4.598                      | 0.058          | 0.031           | 2.019               |
| 44987 | socmob                        | 578       | 578      | 0.106      | 0.080                | 0.071                | 0.033     | 0.030         | 0.090               | 0.268                      | 0.017          | 0.005           | 0.038               |
| 44989 | kings_county                  | 10806     | 10807    | 1.025      | 2.006                | 0.515                | 0.003     | 0.001         | 1.212               | 9.309                      | 0.413          | 0.057           | 4.194               |
| 44990 | brazilian_houses              | 5346      | 5346     | 0.054      | 1.836                | 1.751                | 0.036     | 0.030         | 0.204               | 2.691                      | 0.004          | 0.002           | 0.988               |
| 44992 | fps_benchmark                 | 12312     | 12312    | 2.932      | 10.452               | 2.377                | 0.037     | 0.031         | 7.583               | 15.182                     | 2.245          | 0.486           | 8.375               |
| 44993 | health_insurance              | 11136     | 11136    | 0.158      | 0.604                | 0.602                | 0.004     | 0.001         | 0.664               | 1.576                      | 0.036          | 0.041           | 0.500               |
| 44994 | cars                          | 402       | 402      | 0.016      | 0.146                | 0.150                | 0.037     | 0.029         | 0.079               | 0.271                      | 0.002          | 0.001           | 0.019               |
| 45012 | fifa                          | 9589      | 9589     | 0.289      | 0.851                | 0.385                | 0.003     | 0.001         | 0.779               | 4.192                      | 0.071          | 0.052           | 1.746               |
| 45402 | space_ga                      | 1554      | 1553     | 0.075      | 0.343                | 0.137                | 0.002     | 0.001         | 0.134               | 0.726                      | 0.016          | 0.005           | 0.071               |

**Table S15.** Grouped versus random splits on datasets with repeated units ($\alpha=0.1$, 5 seeds; normalised size; random-split values from the same seeds of the main benchmark).

| dataset           | split       | method    | coverage_grouped   | coverage_random   | worst_grouped   | worst_random   | size_grouped   | size_random   | n_seeds   |
|:------------------|:------------|:----------|:-------------------|:------------------|:----------------|:---------------|:---------------|:--------------|:----------|
| superconductivity | by_features | SCP       | 0.901              | 0.897             | 0.819           | 0.803          | 0.785          | 0.754         | 5         |
| superconductivity | by_features | CQR       | 0.897              | 0.900             | 0.777           | 0.751          | 1.015          | 1.006         | 5         |
| superconductivity | by_features | HPD-split | 0.897              | 0.900             | 0.876           | 0.881          | 0.768          | 0.720         | 5         |
| superconductivity | by_features | BCCP      | 0.903              | 0.898             | 0.891           | 0.889          | 0.852          | 0.831         | 5         |
| superconductivity | by_features | S-NCP     | 0.897              | 0.903             | 0.879           | 0.889          | 0.767          | 0.730         | 5         |
| superconductivity | by_features | S-CQR     | 0.897              | 0.901             | 0.890           | 0.882          | 1.025          | 1.010         | 5         |
| superconductivity | by_features | SDLC      | 0.899              | 0.900             | 0.890           | 0.894          | 0.701          | 0.674         | 5         |
| video_transcoding | by_video    | SCP       | 0.896              | 0.901             | 0.431           | 0.466          | 0.503          | 0.126         | 5         |
| video_transcoding | by_video    | CQR       | 0.892              | 0.900             | 0.700           | 0.857          | 0.466          | 0.253         | 5         |
| video_transcoding | by_video    | HPD-split | 0.920              | 0.900             | 0.766           | 0.897          | 0.726          | 0.130         | 5         |
| video_transcoding | by_video    | BCCP      | 0.875              | 0.900             | 0.852           | 0.895          | 0.643          | 0.123         | 5         |
| video_transcoding | by_video    | S-NCP     | 0.917              | 0.901             | 0.904           | 0.893          | 0.878          | 0.127         | 5         |
| video_transcoding | by_video    | S-CQR     | 0.873              | 0.899             | 0.855           | 0.895          | 0.516          | 0.259         | 5         |
| video_transcoding | by_video    | SDLC      | 0.900              | 0.900             | 0.873           | 0.897          | 0.775          | 0.113         | 5         |
| sarcos            | dedup       | SCP       | 0.898              | 0.900             | 0.787           | 0.796          | 0.414          | 0.395         | 5         |
| sarcos            | dedup       | CQR       | 0.902              | 0.901             | 0.821           | 0.834          | 0.582          | 0.556         | 5         |
| sarcos            | dedup       | HPD-split | 0.898              | 0.901             | 0.889           | 0.891          | 0.385          | 0.382         | 5         |
| sarcos            | dedup       | BCCP      | 0.900              | 0.901             | 0.895           | 0.899          | 0.419          | 0.398         | 5         |
| sarcos            | dedup       | S-NCP     | 0.898              | 0.902             | 0.889           | 0.895          | 0.386          | 0.384         | 5         |
| sarcos            | dedup       | S-CQR     | 0.904              | 0.900             | 0.900           | 0.898          | 0.586          | 0.559         | 5         |
| sarcos            | dedup       | SDLC      | 0.898              | 0.901             | 0.891           | 0.897          | 0.373          | 0.356         | 5         |

Table S15 (continued). Grouped splits: range over the five seeds of marginal and worst-stratum coverage (each seed is one calibration set; the guarantees hold on average over calibration sets).

| Dataset           | Method    | Marginal cov. (min over seeds)   | Marginal cov. (max)   | Worst-stratum cov. (min)   | Worst-stratum cov. (max)   | Seeds   |
|:------------------|:----------|:---------------------------------|:----------------------|:---------------------------|:---------------------------|:--------|
| sarcos            | BCCP      | 0.897                            | 0.905                 | 0.880                      | 0.892                      | 5       |
| sarcos            | CQR       | 0.898                            | 0.905                 | 0.817                      | 0.828                      | 5       |
| sarcos            | HPD-split | 0.895                            | 0.901                 | 0.878                      | 0.886                      | 5       |
| sarcos            | S-CQR     | 0.899                            | 0.909                 | 0.886                      | 0.895                      | 5       |
| sarcos            | S-NCP     | 0.896                            | 0.901                 | 0.880                      | 0.891                      | 5       |
| sarcos            | SCP       | 0.891                            | 0.901                 | 0.770                      | 0.784                      | 5       |
| sarcos            | SDLC      | 0.893                            | 0.902                 | 0.871                      | 0.893                      | 5       |
| superconductivity | BCCP      | 0.886                            | 0.913                 | 0.875                      | 0.898                      | 5       |
| superconductivity | CQR       | 0.891                            | 0.903                 | 0.754                      | 0.792                      | 5       |
| superconductivity | HPD-split | 0.894                            | 0.901                 | 0.866                      | 0.880                      | 5       |
| superconductivity | S-CQR     | 0.886                            | 0.907                 | 0.865                      | 0.889                      | 5       |
| superconductivity | S-NCP     | 0.890                            | 0.904                 | 0.852                      | 0.893                      | 5       |
| superconductivity | SCP       | 0.888                            | 0.911                 | 0.794                      | 0.842                      | 5       |
| superconductivity | SDLC      | 0.890                            | 0.905                 | 0.867                      | 0.892                      | 5       |
| video_transcoding | BCCP      | 0.807                            | 0.931                 | 0.743                      | 0.893                      | 5       |
| video_transcoding | CQR       | 0.872                            | 0.912                 | 0.660                      | 0.742                      | 5       |
| video_transcoding | HPD-split | 0.841                            | 0.957                 | 0.632                      | 0.852                      | 5       |
| video_transcoding | S-CQR     | 0.857                            | 0.901                 | 0.647                      | 0.866                      | 5       |
| video_transcoding | S-NCP     | 0.844                            | 0.939                 | 0.776                      | 0.925                      | 5       |
| video_transcoding | SCP       | 0.864                            | 0.932                 | 0.341                      | 0.632                      | 5       |
| video_transcoding | SDLC      | 0.788                            | 0.935                 | 0.750                      | 0.893                      | 5       |

Table S15 (continued). Splits by time (post hoc; experiments/run_temporal.py). Moneyball "forward": earliest seasons for training (50% of rows), next for calibration (25%), latest for test; "blocked": whole seasons assigned at random. Bike_Sharing_Demand "blocked": whole months assigned at random (the curated data contain no year or day). Random-split values from the same seeds of the main benchmark.

| dataset             | split   | method    | coverage   | coverage_min   | coverage_max   | worst   | worst_min   | coverage_random   | worst_random   | size   | size_random   | n_seeds   |
|:--------------------|:--------|:----------|:-----------|:---------------|:---------------|:--------|:------------|:------------------|:---------------|:-------|:--------------|:----------|
| Moneyball           | blocked | SCP       | 0.888      | 0.871          | 0.918          | 0.784   | 0.766       | 0.903             | 0.804          | 0.842  | 0.906         | 5         |
| Moneyball           | blocked | CQR       | 0.892      | 0.833          | 0.930          | 0.789   | 0.744       | 0.897             | 0.793          | 0.962  | 1.110         | 5         |
| Moneyball           | blocked | HPD-split | 0.885      | 0.849          | 0.908          | 0.793   | 0.737       | 0.914             | 0.814          | 0.857  | 0.947         | 5         |
| Moneyball           | blocked | BCCP      | 0.883      | 0.862          | 0.902          | 0.823   | 0.792       | 0.908             | 0.806          | 0.859  | 0.949         | 5         |
| Moneyball           | blocked | S-NCP     | 0.884      | 0.855          | 0.908          | 0.796   | 0.708       | 0.914             | 0.813          | 0.875  | 1.003         | 5         |
| Moneyball           | blocked | S-CQR     | 0.883      | 0.833          | 0.922          | 0.786   | 0.744       | 0.899             | 0.811          | 0.970  | 1.129         | 5         |
| Moneyball           | blocked | SDLC      | 0.890      | 0.874          | 0.905          | 0.817   | 0.778       | 0.912             | 0.813          | 0.872  | 0.979         | 5         |
| Moneyball           | forward | SCP       | 0.953      | 0.942          | 0.961          | 0.862   | 0.667       | 0.903             | 0.804          | 1.422  | 0.906         | 5         |
| Moneyball           | forward | CQR       | 0.970      | 0.961          | 0.985          | 0.927   | 0.908       | 0.897             | 0.793          | 1.757  | 1.110         | 5         |
| Moneyball           | forward | HPD-split | 0.939      | 0.927          | 0.955          | 0.814   | 0.667       | 0.914             | 0.814          | 1.368  | 0.947         | 5         |
| Moneyball           | forward | BCCP      | 0.886      | 0.864          | 0.900          | 0.819   | 0.791       | 0.908             | 0.806          | 3.063  | 0.949         | 5         |
| Moneyball           | forward | S-NCP     | 0.882      | 0.864          | 0.897          | 0.805   | 0.783       | 0.914             | 0.813          | 2.959  | 1.003         | 5         |
| Moneyball           | forward | S-CQR     | 0.927      | 0.915          | 0.961          | 0.877   | 0.837       | 0.899             | 0.811          | 3.351  | 1.129         | 5         |
| Moneyball           | forward | SDLC      | 0.881      | 0.870          | 0.900          | 0.802   | 0.775       | 0.912             | 0.813          | 3.831  | 0.979         | 5         |
| Bike_Sharing_Demand | blocked | SCP       | 0.901      | 0.876          | 0.925          | 0.481   | 0.421       | 0.899             | 0.495          | 1.798  | 1.590         | 5         |
| Bike_Sharing_Demand | blocked | CQR       | 0.890      | 0.835          | 0.928          | 0.543   | 0.499       | 0.898             | 0.665          | 1.470  | 1.397         | 5         |
| Bike_Sharing_Demand | blocked | HPD-split | 0.894      | 0.838          | 0.937          | 0.722   | 0.664       | 0.896             | 0.721          | 1.644  | 1.361         | 5         |
| Bike_Sharing_Demand | blocked | BCCP      | 0.906      | 0.890          | 0.927          | 0.870   | 0.824       | 0.898             | 0.883          | 2.005  | 1.695         | 5         |
| Bike_Sharing_Demand | blocked | S-NCP     | 0.898      | 0.859          | 0.941          | 0.875   | 0.816       | 0.897             | 0.878          | 1.937  | 1.503         | 5         |
| Bike_Sharing_Demand | blocked | S-CQR     | 0.891      | 0.830          | 0.941          | 0.826   | 0.718       | 0.900             | 0.883          | 1.693  | 1.482         | 5         |
| Bike_Sharing_Demand | blocked | SDLC      | 0.899      | 0.863          | 0.942          | 0.870   | 0.821       | 0.894             | 0.873          | 1.857  | 1.469         | 5         |

**Table S16.** Pre-specified secondary analyses of the held-out replication (hull forms) and post hoc equivalence tests (±5% on the log-size scale, TOST with two one-sided Wilcoxon tests), on CTR23 and the held-out datasets.

| suite        | analysis             | comparison              | n   | geo_ratio   | geo_lo   | geo_hi   | hl_ratio   | wins   | losses   | p     | p_holm   |
|:-------------|:---------------------|:------------------------|:----|:------------|:---------|:---------|:-----------|:-------|:---------|:------|:---------|
| ctr23        | hull (secondary)     | SDLC-hull vs BCCP-hull  | 31  | 0.900       | 0.820    | 0.986    | 0.926      | 26     | 5        | 0.000 | 0.001    |
| ctr23        | hull (secondary)     | SDLC-hull vs S-NCP-hull | 31  | 1.009       | 0.958    | 1.079    | 0.980      | 23     | 8        | 0.029 | 0.029    |
| ctr23        | TOST +-5% (post hoc) | SDLC vs S-NCP           | 31  | 0.964       | 0.941    | 0.988    | 0.964      | 27     | 4        | 0.108 | 0.108    |
| ctr23        | TOST +-5% (post hoc) | SDLC vs S-HPD           | 31  | 0.949       | 0.931    | 0.964    | 0.956      | 29     | 2        | 0.284 | 0.284    |
| confirmatory | hull (secondary)     | SDLC-hull vs BCCP-hull  | 17  | 0.894       | 0.820    | 0.964    | 0.920      | 13     | 4        | 0.007 | 0.013    |
| confirmatory | hull (secondary)     | SDLC-hull vs S-NCP-hull | 17  | 1.045       | 0.980    | 1.162    | 0.996      | 10     | 7        | 0.712 | 0.712    |
| confirmatory | TOST +-5% (post hoc) | SDLC vs S-NCP           | 17  | 0.979       | 0.940    | 1.035    | 0.973      | 15     | 2        | 0.054 | 0.054    |
| confirmatory | TOST +-5% (post hoc) | SDLC vs S-HPD           | 17  | 0.988       | 0.963    | 1.027    | 0.979      | 15     | 2        | 0.004 | 0.004    |

**Table S17.** Held-out datasets: skewness and octile skewness of the training targets, and size comparisons of SDLC by skewness subgroup (post hoc, descriptive).

| did   | skew   | octile_skew   | min_y   | n_distinct   |
|:------|:-------|:--------------|:--------|:-------------|
| 44056 | 0.331  | 0.290         | 1.000   | 40           |
| 44061 | 0.750  | 0.177         | 72.110  | 1600         |
| 44068 | -0.573 | 0.010         | -1.642  | 3811         |
| 44069 | 0.793  | 0.460         | 2.748   | 15039        |
| 44134 | 2.352  | 0.455         | 0.012   | 56           |
| 44137 | -1.442 | -0.250        | -0.004  | 35           |
| 44139 | -3.434 | 0.104         | 0.000   | 1653         |
| 44142 | 1.293  | 0.350         | 1.000   | 791          |
| 44143 | -0.005 | -0.280        | 0.000   | 799          |
| 44145 | 7.362  | 0.111         | 0.000   | 4855         |
| 44146 | 0.869  | 0.213         | 7.908   | 24760        |
| 45032 | -4.856 | 0.376         | 0.000   | 1117         |
| 45034 | -0.860 | -0.632        | -8.161  | 807          |
| 45041 | -4.856 | 0.376         | 0.000   | 1117         |
| 45043 | -0.420 | -0.333        | 0.000   | 29           |
| 45046 | 0.113  | 0.047         | 4.138   | 24374        |
| 45047 | 0.501  | 0.273         | -6.550  | 281          |

| suite        | analysis                                   | comparison    | n   | geo_ratio   | geo_lo   | geo_hi   | hl_ratio   | wins   | losses   | p     | p_holm   |
|:-------------|:-------------------------------------------|:--------------|:----|:------------|:---------|:---------|:-----------|:-------|:---------|:------|:---------|
| confirmatory | subgroup skewed (post hoc, descriptive)    | SDLC vs BCCP  | 7   | 0.829       | 0.683    | 0.970    | 0.886      | 5      | 2        | 0.078 |          |
| confirmatory | subgroup skewed (post hoc, descriptive)    | SDLC vs S-NCP | 7   | 1.017       | 0.950    | 1.136    | 0.977      | 5      | 2        | 0.375 |          |
| confirmatory | subgroup skewed (post hoc, descriptive)    | SDLC vs S-CQR | 7   | 0.870       | 0.732    | 0.991    | 0.937      | 5      | 2        | 0.156 |          |
| confirmatory | subgroup skewed (post hoc, descriptive)    | SDLC vs S-HPD | 7   | 1.004       | 0.950    | 1.094    | 0.974      | 6      | 1        | 0.297 |          |
| confirmatory | subgroup symmetric (post hoc, descriptive) | SDLC vs BCCP  | 10  | 0.882       | 0.801    | 0.950    | 0.904      | 9      | 1        | 0.006 |          |
| confirmatory | subgroup symmetric (post hoc, descriptive) | SDLC vs S-NCP | 10  | 0.954       | 0.915    | 0.983    | 0.969      | 10     | 0        | 0.002 |          |
| confirmatory | subgroup symmetric (post hoc, descriptive) | SDLC vs S-CQR | 10  | 0.812       | 0.653    | 0.930    | 0.885      | 10     | 0        | 0.002 |          |
| confirmatory | subgroup symmetric (post hoc, descriptive) | SDLC vs S-HPD | 10  | 0.977       | 0.959    | 0.991    | 0.983      | 9      | 1        | 0.004 |          |

**Table S17b.** Post hoc checks of the held-out replication and of CTR23 (review round 5; scripts/analyze_review05.py; no model was refitted). Size comparisons of SDLC with the stratified comparators (per-dataset geometric-mean normalised size, two-sided Wilcoxon signed-rank test, Holm over the four comparators within a subset) on: all held-out datasets as pre-specified; the duplicate pair yprop_4_1/topo_2_1 merged into one dataset (log-scale mean); continuous targets (at least 100 distinct values and largest atom at most 5% of rows); datasets with nominal tail strata (realised training mass of the lowest and highest stratum within [0.08, 0.12] in every seed, K = 5); and without house_16H.

| suite    | subset                         | comparison    | n   | geo_ratio   | wins   | losses   | p     | p_holm   |
|:---------|:-------------------------------|:--------------|:----|:------------|:-------|:---------|:------|:---------|
| held-out | all 17 (pre-specified set)     | SDLC vs BCCP  | 17  | 0.860       | 14     | 3        | 0.000 | 0.001    |
| held-out | all 17 (pre-specified set)     | SDLC vs S-NCP | 17  | 0.979       | 15     | 2        | 0.004 | 0.008    |
| held-out | all 17 (pre-specified set)     | SDLC vs S-CQR | 17  | 0.835       | 15     | 2        | 0.000 | 0.001    |
| held-out | all 17 (pre-specified set)     | SDLC vs S-HPD | 17  | 0.988       | 15     | 2        | 0.005 | 0.008    |
| held-out | duplicate pair merged (n = 16) | SDLC vs BCCP  | 16  | 0.851       | 14     | 2        | 0.000 | 0.001    |
| held-out | duplicate pair merged (n = 16) | SDLC vs S-NCP | 16  | 0.980       | 14     | 2        | 0.006 | 0.013    |
| held-out | duplicate pair merged (n = 16) | SDLC vs S-CQR | 16  | 0.825       | 15     | 1        | 0.000 | 0.000    |
| held-out | duplicate pair merged (n = 16) | SDLC vs S-HPD | 16  | 0.989       | 14     | 2        | 0.008 | 0.013    |
| heldout  | continuous targets             | SDLC vs BCCP  | 10  | 0.900       | 7      | 3        | 0.037 | 0.039    |
| heldout  | continuous targets             | SDLC vs S-NCP | 10  | 0.953       | 10     | 0        | 0.002 | 0.008    |
| heldout  | continuous targets             | SDLC vs S-CQR | 10  | 0.945       | 8      | 2        | 0.020 | 0.039    |
| heldout  | continuous targets             | SDLC vs S-HPD | 10  | 0.972       | 10     | 0        | 0.002 | 0.008    |
| heldout  | nominal tail strata            | SDLC vs BCCP  | 11  | 0.905       | 8      | 3        | 0.019 | 0.020    |
| heldout  | nominal tail strata            | SDLC vs S-NCP | 11  | 0.954       | 11     | 0        | 0.001 | 0.004    |
| heldout  | nominal tail strata            | SDLC vs S-CQR | 11  | 0.946       | 9      | 2        | 0.010 | 0.020    |
| heldout  | nominal tail strata            | SDLC vs S-HPD | 11  | 0.974       | 11     | 0        | 0.001 | 0.004    |
| ctr23    | continuous targets             | SDLC vs BCCP  | 23  | 0.933       | 18     | 5        | 0.001 | 0.001    |
| ctr23    | continuous targets             | SDLC vs S-NCP | 23  | 0.951       | 21     | 2        | 0.000 | 0.000    |
| ctr23    | continuous targets             | SDLC vs S-CQR | 23  | 0.754       | 21     | 2        | 0.000 | 0.000    |
| ctr23    | continuous targets             | SDLC vs S-HPD | 23  | 0.942       | 22     | 1        | 0.000 | 0.000    |
| ctr23    | nominal tail strata            | SDLC vs BCCP  | 24  | 0.935       | 19     | 5        | 0.001 | 0.001    |
| ctr23    | nominal tail strata            | SDLC vs S-NCP | 24  | 0.951       | 22     | 2        | 0.000 | 0.000    |
| ctr23    | nominal tail strata            | SDLC vs S-CQR | 24  | 0.748       | 22     | 2        | 0.000 | 0.000    |
| ctr23    | nominal tail strata            | SDLC vs S-HPD | 24  | 0.942       | 23     | 1        | 0.000 | 0.000    |
| held-out | merged pair, without house_16H | SDLC vs BCCP  | 15  | 0.882       | 13     | 2        | 0.000 | 0.001    |
| held-out | merged pair, without house_16H | SDLC vs S-NCP | 15  | 0.957       | 14     | 1        | 0.000 | 0.000    |
| held-out | merged pair, without house_16H | SDLC vs S-CQR | 15  | 0.849       | 14     | 1        | 0.000 | 0.001    |
| held-out | merged pair, without house_16H | SDLC vs S-HPD | 15  | 0.972       | 14     | 1        | 0.000 | 0.001    |

Table S17b (continued). Coverage of the top 1% of outcomes with one definition in both pipelines ($y\ge q_{0.99}$ of the training targets; a seed counts only if the group holds at least 10 test points; mean, minimum and maximum over datasets).

| suite    | method    | n_datasets   | mean   | min   | max   |
|:---------|:----------|:-------------|:-------|:------|:------|
| ctr23    | BCCP      | 24           | 0.697  | 0.151 | 1.000 |
| ctr23    | CQR       | 24           | 0.494  | 0.000 | 0.972 |
| ctr23    | HPD-split | 24           | 0.691  | 0.001 | 1.000 |
| ctr23    | S-CQR     | 24           | 0.696  | 0.150 | 0.917 |
| ctr23    | S-HPD     | 24           | 0.781  | 0.246 | 0.956 |
| ctr23    | S-NCP     | 24           | 0.782  | 0.246 | 0.952 |
| ctr23    | SCP       | 24           | 0.467  | 0.000 | 0.994 |
| ctr23    | SDLC      | 24           | 0.750  | 0.190 | 1.000 |
| held-out | BCCP      | 17           | 0.699  | 0.357 | 0.877 |
| held-out | CQR       | 17           | 0.420  | 0.000 | 0.947 |
| held-out | HPD-split | 17           | 0.576  | 0.000 | 0.937 |
| held-out | S-CQR     | 17           | 0.696  | 0.294 | 0.934 |
| held-out | S-HPD     | 17           | 0.796  | 0.391 | 0.958 |
| held-out | S-NCP     | 17           | 0.793  | 0.391 | 0.958 |
| held-out | SCP       | 17           | 0.471  | 0.000 | 0.990 |
| held-out | SDLC      | 17           | 0.760  | 0.401 | 0.928 |

Table S17b (continued). RW-DLC versus stratified methods with dedicated 1% tail strata (stratum edges at the training quantiles 0.01, 0.10, 0.25, 0.75, 0.90, 0.99; review round 8; experiments/eval_tail1.py, scripts/analyze_review08.py; held-out data, 5 seeds). Top-1% coverage ($y\ge q_{0.99}$, seeds with at least 10 such test points), marginal coverage and normalised size (geometric-mean and Hodges-Lehmann ratios); two-sided Wilcoxon tests, Holm over all six tests.

| comparison                       | top1_rw   | top1_comp   | top1_diff   | top1_wins   | top1_losses   | top1_n   | top1_p_holm   | cov_rw   | cov_comp   | size_geo   | size_hl   | size_wins   | size_losses   | size_p_holm   |
|:---------------------------------|:----------|:------------|:------------|:------------|:--------------|:---------|:--------------|:---------|:-----------|:-----------|:----------|:------------|:--------------|:--------------|
| RW-DLC vs SDLC (1% tail strata)  | 0.884     | 0.906       | -0.022      | 12          | 5             | 17       | 1.000         | 0.884    | 0.901      | 0.952      | 0.987     | 9           | 8             | 1.000         |
| RW-DLC vs S-NCP (1% tail strata) | 0.884     | 0.908       | -0.024      | 12          | 5             | 17       | 1.000         | 0.884    | 0.902      | 0.941      | 0.957     | 10          | 7             | 1.000         |
| RW-DLC vs BCCP (1% tail strata)  | 0.884     | 0.911       | -0.026      | 11          | 6             | 17       | 1.000         | 0.884    | 0.901      | 0.818      | 0.876     | 10          | 7             | 0.209         |

Table S17b (continued). RW-3 (top-1% coverage of RW-DLC versus SDLC, held-out data, one-sided Wilcoxon test): the pre-specified definition ($y>q_{0.99}$) and post hoc variants.

| variant                               | n   | diff_mean   | wins   | p     | rw    | rw_min   | rw_max   | sdlc   |
|:--------------------------------------|:----|:------------|:-------|:------|:------|:---------|:---------|:-------|
| pre-specified (strict y > q99)        | 15  | 0.184       | 13     | 0.011 | 0.872 | 0.508    | 0.988    | 0.688  |
| strict, pair merged                   | 14  | 0.214       | 13     | 0.002 | 0.897 | 0.514    | 0.988    | 0.683  |
| strict, without Ailerons              | 14  | 0.143       | 12     | 0.021 | 0.866 | 0.508    | 0.988    | 0.723  |
| unified (y >= q99, >= 10 test points) | 17  | 0.125       | 15     | 0.009 | 0.884 | 0.521    | 0.988    | 0.760  |
| unified, pair merged                  | 16  | 0.147       | 15     | 0.001 | 0.905 | 0.549    | 0.988    | 0.759  |

**Table S18.** Pre-specified hypothesis tests RW-1 to RW-4 of the relevance-weighted study (column suite: collection of datasets).

| suite        | hypothesis   | comparison                                        | estimate   | p      | p_holm   | supported   |
|:-------------|:-------------|:--------------------------------------------------|:-----------|:-------|:---------|:------------|
| confirmatory | RW-1         | Cov_phiU(RW-DLC) equivalent to 0.90 (margin 0.02) | 0.8976     | 0.0000 | 0.0000   | True        |
| confirmatory | RW-2         | Cov_phiU: RW-DLC > SCP                            | 0.1791     | 0.0000 | 0.0000   | True        |
| confirmatory | RW-2         | Cov_phiU: RW-DLC > NCP                            | 0.1216     | 0.0000 | 0.0001   | True        |
| confirmatory | RW-2         | Cov_phiU: RW-DLC > CQR                            | 0.1519     | 0.0000 | 0.0001   | True        |
| confirmatory | RW-2         | Cov_phiU: RW-DLC > DLS-M                          | 0.1801     | 0.0000 | 0.0000   | True        |
| confirmatory | RW-3         | top-1% coverage: RW-DLC > SDLC                    | 0.1837     | 0.0108 | 0.0108   | True        |
| confirmatory | RW-4         | size: RW-DLC vs RW-DLS-U                          | 0.8854     | 0.0305 | 0.0533   | False       |
| confirmatory | RW-4         | size: RW-DLC vs RW-NCP-U                          | 0.9037     | 0.0267 | 0.0533   | False       |

**Table S19.** Relevance-weighted study on the OpenML-CTR23 datasets: not yet available.

![**Fig. S1.** Coverage of the upper calibration stratum per dataset ($\alpha=0.1$).](/home/user/p_c1_2/Target_Journal_Submission/figures/F4_upper_tail_per_dataset.png){width=100%}

![**Fig. S2.** Error analysis. Left: price of stratum-wise validity (SDLC/DLS size ratio) against relative RMSE. Right: worst-stratum coverage of SDLC minus its null mean against calibration-set size, with the 5% null band.](/home/user/p_c1_2/Target_Journal_Submission/figures/F8_error_analysis.png){width=100%}

![**Fig. S3.** Effect of the calibration-set size on worst-stratum coverage (left) and size (right).](/home/user/p_c1_2/Target_Journal_Submission/figures/F7_calibration_size.png){width=100%}

# S5. Earlier implementations

The first run (v1) evaluated all density-based sets on a fixed grid of 200 equal-mass cells of the marginal training-target distribution. The second (v2) used an exact implementation but standardised residuals with an in-sample scale model and used a density floor. Their complete analyses are archived in the anonymised code package provided as supplementary material. The coverage results were the same in all versions. Table S20 shows how the size comparisons changed; this dependence on the implementation is why the comparisons on CTR23 are labelled exploratory and were replicated on held-out data (v1 reported medians of log ratios; v2 also geometric means; the final version reports the Hodges–Lehmann estimate).

**Table S20.** Size comparisons of SDLC with the stratified comparators in the three implementations ($\alpha=0.1$, 31 datasets; negative log ratios favour SDLC).

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

# S6. Pre-specified analysis plan of the confirmatory replication (verbatim)

Reproduced from the analysis-plan file of the code package, committed (identifier `ccba99b`) before any confirmatory evaluation. The plan was written before we adopted the term *pre-specified*; its original wording ("pre-registered", "public repository") is kept. As stated in the manuscript, the plan was committed to the authors' version-controlled repository, not registered with a third party, and the repository will be made public upon acceptance; the anonymised code package provided as supplementary material lists the commit identifiers, commit times and SHA-256 hashes of both plans (PLAN_TIMESTAMPS.md).


**Status.** This document and `code/scripts/analyze_confirmatory.py` are committed to the public repository
[branch name redacted for double-blind review] BEFORE any method has been evaluated on the confirmatory datasets. At the time of the
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

# S7. Pre-specified analysis plan of the relevance-weighted study (verbatim)

Reproduced from the analysis-plan file of the code package, committed (identifier `a9f31d2`) before RW-DLC was evaluated on any dataset. The same note on wording as for Section S6 applies.


Committed to the repository on 2026-11-20 **before** any RW method was evaluated on any real dataset. [Motivation paragraph referring to internal project documents redacted for double-blind review.]

### 1. Method (fixed)
* Relevance function φ, fitted on the proper-training targets only: p̂_Y = Gaussian KDE of y_train with Silverman
  bandwidth (scipy.stats.gaussian_kde, bw_method="silverman"); τ = 0.01 · max_i p̂_Y(y_train,i).
  - **RW-U** ("uniform over the target range"): φ_U(y) = 1 / max(p̂_Y(y), τ).
  - **RW-H** ("half-way"): φ_H(y) = max(p̂_Y(y), τ)^(-1/2).
* Guarantee targeted: relevance-weighted coverage Cov_φ(C) = E[φ(Y) 1{Y ∈ C(X)}] / E[φ(Y)] ≥ 1 − α.
* Weighted split-conformal calibration: for a candidate y with calibration scores S_i and weights φ_i = φ(Y_i),
  q(y) = inf{s : Σ_i φ_i 1{S_i ≤ s} ≥ (1 − α)(Σ_i φ_i + φ(y))} (= +∞ if no such s); y ∈ C(x) iff s(x, y) ≤ q(y).
  Validity follows from weighted exchangeability with the known likelihood ratio dQ/dP ∝ φ(y) (Tibshirani et al. 2019).
* Scores (all use the same μ̂, σ̂, ĝ as SDLC, results/raw_contexts_v3 noise sample, same floor, same domain D):
  - **RW-DLC** (proposed; size-optimal for the weighted constraint): s(x, y) = −φ(y) f̂(y | x);
  - **RW-DLS** (ablation: weighting only in calibration): s = −f̂(y | x);
  - **RW-NCP** (ablation: weighted normalised residual): s = |y − μ̂(x)| / σ̂(x).
* Comparators recomputed on the same grid and the same splits: SCP, NCP, CQR (marginal intervals), DLS-M (marginal
  density level set), S-NCP and SDLC (five-stratum S5 design of the main benchmark).
* Geometry: y-grid of G = 4000 equally spaced points over D; a grid point is in the set iff its score ≤ its threshold;
  size = (number of included points) × (grid spacing). Coverage of each test target is decided exactly by the rule
  (not by the grid). α = 0.1 only.

### 2. Data
* Exploratory: all 31 OpenML-CTR23 datasets of the main benchmark, seeds 0–9 (same splits; contexts re-fitted by
  `experiments/run_benchmark.py --mode fitonly`, checked against the stored seed-0 contexts).
* Confirmatory: the 17 held-out datasets of the confirmatory replication, seeds 0–4 (stored contexts).
The same analysis is run on both; claims in the paper rest on the held-out data when the two disagree.

### 3. Metrics (per dataset × seed, then averaged over seeds)
Marginal coverage; Cov_φU and Cov_φH estimated on test points with φ evaluated at the test targets; coverage per
training-target decile → macro-decile coverage (mean of the ten) and worst-decile coverage; top-1 % and bottom-1 %
coverage (training-target 1 % quantiles); mean set size divided by sd(y_train); empty-set rate; Kish effective sample size
of the calibration weights (Σφ)²/Σφ²; share of test points with an infinite threshold.

### 4. Hypotheses and tests (unit of analysis = dataset; α_test = 0.05)
* **RW-1 (validity).** Dataset-mean Cov_φU of RW-DLC is equivalent to 0.90: TOST with two one-sided Wilcoxon
  signed-rank tests, margin 0.02. Supported if both one-sided p < 0.05.
* **RW-2 (marginal methods miss the weighted target).** Cov_φU of RW-DLC > that of each of SCP, NCP, CQR, DLS-M:
  one-sided Wilcoxon, Holm over the four. Supported if all four Holm p < 0.05.
* **RW-3 (extreme tail).** Top-1 % coverage of RW-DLC (φ_U) > that of SDLC: one-sided Wilcoxon. Reported with the
  mean difference and bootstrap CI.
* **RW-4 (score optimality).** Set size of RW-DLC < RW-DLS and < RW-NCP (φ_U): two-sided Wilcoxon on log sizes, Holm
  over the two; a size claim requires Holm p < 0.05 AND a 95 % bootstrap CI of the geometric-mean ratio excluding 1.
* Descriptive only (no hypothesis): RW-DLC vs SDLC and vs S-NCP in size, macro-decile and worst-decile coverage; the
  φ_H results; ESS and infinite-threshold shares.
Negative or null outcomes will be reported whatever their direction.

### 5. Deviations
Any change after this commit will be listed in the manuscript as a deviation with its reason.

# S8. Additional results and analyses moved from the main text

**S8.1 Further size comparisons on CTR23.**

Post hoc, equivalence within ±5% was not established with S-NCP (TOST $p$ = 0.108) or S-HPD ($p$ = 0.284), and SDLC's sets were reliably smaller than S-NCP's (seed-level 95% interval below zero) on 18 datasets and reliably larger on 0. When an interval is required, SDLC-hull was smaller than BCCP-hull (ratio 0.903, 25/6), whereas against S-NCP-hull the median favoured SDLC-hull (23/8, Hodges–Lehmann ratio 0.979) and the geometric mean did not (1.014). These comparisons are exploratory (the protocol section of the main text); the confirmatory section of the main text tests them on held-out data.

**S8.2 Synthetic study with known densities.**

Five synthetic designs with known densities (Table S21; A skewed, B covariate-dependent skewness, C bimodal, D heavy-tailed, E zero-inflated) separate the score from its estimate. With the true density, the oracle SDLC set was smaller than the oracle normalised residual in every design, by 2.9% to 35.2%. The estimated SDLC was smaller than S-NCP in 41 of 50 design-seed combinations, but under the misspecified design C its sets were 53.2% larger than the oracle's. Under a genuine label shift (Supplementary Table S10), all stratified methods degraded similarly.

**Table S21.** Synthetic study ($n_{\mathrm{train}}=n_{\mathrm{cal}}=5000$, 10 seeds, $\alpha=0.1$, 20,000 test points per seed). Designs: A skewed noise; B covariate-dependent skewness; C bimodal; D heavy-tailed; E zero-inflated. Each cell: coverage of the upper stratum / mean set size relative to S-NCP. Oracle methods (O-) use the true conditional density or the true $\mu$ and $\sigma$; O-BCCP is BCCP with the true $\mu$, and O-HDR-X is the shortest set with exact covariate-conditional coverage. Design E has an atom at zero, so its conditional law has no Lebesgue density and the oracle rows are empty.

| Method    | A             | B             | C             | D             | E             |
|:----------|:--------------|:--------------|:--------------|:--------------|:--------------|
| O-HDR-X   | 0.693 / 0.804 | 0.841 / 0.920 | 0.897 / 0.672 | 0.832 / 0.889 |               |
| O-SDLC    | 0.897 / 0.860 | 0.903 / 0.907 | 0.903 / 0.643 | 0.907 / 0.914 |               |
| O-S-NCP   | 0.897 / 0.904 | 0.898 / 0.938 | 0.909 / 0.993 | 0.906 / 0.941 |               |
| O-BCCP    | 0.894 / 1.023 | 0.898 / 1.026 | 0.911 / 1.211 | 0.904 / 1.000 |               |
| SCP       | 0.709 / 0.978 | 0.806 / 1.041 | 0.865 / 1.114 | 0.813 / 0.994 | 0.370 / 0.963 |
| CQR       | 0.694 / 1.020 | 0.752 / 1.071 | 0.795 / 1.080 | 0.758 / 1.087 | 0.556 / 0.751 |
| HPD-split | 0.675 / 0.906 | 0.814 / 0.983 | 0.883 / 0.993 | 0.818 / 0.951 | 0.590 / 0.776 |
| BCCP      | 0.893 / 1.066 | 0.899 / 1.070 | 0.894 / 1.122 | 0.901 / 1.055 | 0.902 / 1.631 |
| S-NCP     | 0.895 / 1.000 | 0.894 / 1.000 | 0.902 / 1.000 | 0.901 / 1.000 | 0.893 / 1.000 |
| S-CQR     | 0.891 / 1.091 | 0.896 / 1.075 | 0.899 / 1.069 | 0.902 / 1.131 | 0.903 / 1.018 |
| S-HPD     | 0.896 / 0.997 | 0.894 / 1.000 | 0.902 / 1.000 | 0.901 / 1.000 | 0.893 / 0.983 |
| SDLC-N    | 0.893 / 0.981 | 0.896 / 0.985 | 0.895 / 0.983 | 0.901 / 0.990 | 0.896 / 0.989 |
| SDLC      | 0.894 / 0.966 | 0.898 / 0.986 | 0.894 / 0.986 | 0.903 / 0.992 | 0.896 / 0.912 |


**S8.3 Secondary and post hoc analyses of the held-out replication.**

Post hoc checks of the held-out collection (main text, Datasets; Table S17b) leave every C-H3 decision unchanged. With the duplicate pair merged (16 independent targets), SDLC was smaller than S-NCP on 14 of 16 datasets (ratio 0.980, Holm $p$ = 0.013) and than BCCP on 14 (ratio 0.851). On the 10 held-out datasets with continuous targets (at least 100 distinct values, no atom above 5%) it was smaller than S-NCP and S-HPD on all of them (ratios 0.953 and 0.972), and the same held for the 11 datasets whose tail strata had their nominal mass. The small advantage over S-NCP is therefore a result for continuous targets; on discretised or atom-heavy targets the two scores were indistinguishable.

The secondary results repeated the trade-off seen on CTR23. SDLC covered 0.747 of the top 1%, against 0.781 for S-NCP (range over datasets 0.40–0.93; top 1% defined as $y\ge q_{0.99}$ of the training targets, as everywhere in the main pipeline), and its worst coverage over deciles of $\hat\sigma(x)$ was 0.817, against 0.831. The price of stratification relative to DLS was 1.22. The pre-specified secondary analyses (Supplementary Table S16) were less favourable for the interval forms: SDLC-hull was smaller than BCCP-hull (ratio 0.894, Holm $p$ = 0.013) but not than S-NCP-hull (ratio 1.045, 10/7 datasets, $p$ = 0.712). Post hoc, SDLC was equivalent to S-HPD within ±5% (TOST $p$ = 0.004), equivalence with S-NCP narrowly failed ($p$ = 0.054), and SDLC was reliably smaller than S-NCP on 8 of 17 datasets and reliably larger on 1. On the 7 held-out targets with $|$skewness$|>1$, the advantage over S-NCP and S-HPD disappeared (ratios 1.017 and 1.004), while that over BCCP and S-CQR remained (Supplementary Table S17). Among scores that use $\hat\sigma$, the choice matters little for size; the clear gains are over BCCP and stratified CQR.

**S8.3b Definition of the top 1% in the relevance-weighted study.**

The pre-specified definition ($y>q_{0.99}$) differs from that of the main pipeline ($y\ge q_{0.99}$) and leaves the group empty or nearly empty on targets whose maximum is an atom. With the main-pipeline definition and at least 10 test points per seed, RW-3 still held (RW-DLC 0.884 against 0.760, higher on 15 of 17 datasets, one-sided $p$ = 0.009; post hoc), also with the duplicate pair merged (Supplementary Table S17b). The mean hides a wide range: RW-DLC covered between 0.52 and 0.99 of the top 1% across datasets.

**S8.4 Coverage under target shift.**

**Table S22.** Coverage under target shift ($\alpha=0.1$; means over datasets). *Positive control*: the upper stratum is up-weighted by 5 and the lower stratum down-weighted by 0.5, without changing the within-stratum laws. *Tilts*: importance weights $\omega_\gamma(y)=\exp(\gamma\zeta_y)$ with $\zeta_y$ the normal score of $y$ under the training distribution; the coverage of the upper calibration stratum is shown for all datasets and for the 15 datasets whose effective sample size is at least 50.

| Method     | Positive control: marginal   | Positive control: worst stratum   | Tilt γ=1: upper stratum   | Tilt γ=2: upper stratum   | Tilt γ=2: upper (ESS ≥ 50)   | Tilt γ=2: marginal   |
|:-----------|:-----------------------------|:----------------------------------|:--------------------------|:--------------------------|:-----------------------------|:---------------------|
| SCP        | 0.838                        | 0.630                             | 0.633                     | 0.550                     | 0.532                        | 0.637                |
| NCP        | 0.875                        | 0.765                             | 0.776                     | 0.720                     | 0.751                        | 0.766                |
| CQR        | 0.861                        | 0.720                             | 0.695                     | 0.596                     | 0.624                        | 0.668                |
| Mondrian-ŷ | 0.877                        | 0.770                             | 0.750                     | 0.654                     | 0.649                        | 0.717                |
| DCP        | 0.877                        | 0.783                             | 0.783                     | 0.726                     | 0.765                        | 0.770                |
| HPD-split  | 0.874                        | 0.759                             | 0.773                     | 0.719                     | 0.748                        | 0.765                |
| DLS        | 0.848                        | 0.660                             | 0.664                     | 0.577                     | 0.530                        | 0.658                |
| BCCP       | 0.904                        | 0.890                             | 0.861                     | 0.777                     | 0.754                        | 0.803                |
| S-NCP      | 0.904                        | 0.891                             | 0.881                     | 0.833                     | 0.825                        | 0.847                |
| S-CQR      | 0.905                        | 0.892                             | 0.859                     | 0.770                     | 0.761                        | 0.797                |
| S-HPD      | 0.905                        | 0.893                             | 0.881                     | 0.833                     | 0.825                        | 0.846                |
| SDLC-N     | 0.906                        | 0.893                             | 0.877                     | 0.816                     | 0.795                        | 0.833                |
| SDLC       | 0.904                        | 0.891                             | 0.869                     | 0.798                     | 0.774                        | 0.819                |


Under the positive control, which re-weights whole strata, the stratum-wise coverage of every stratified method was unchanged, as Corollary 1(i) states (Supplementary Table S22, the shift figure of the main text). Their marginal coverage stayed at the nominal level (0.904 for SDLC), whereas that of the marginal methods fell to 0.838–0.877. Continuous tilts towards the upper tail also re-weight targets *within* strata, so Corollary 1(i) does not apply. Under a moderate tilt ($\gamma=1$) the stratified methods kept 0.861–0.881 coverage of the upper stratum, against 0.633–0.783 for the marginal methods. Under a strong tilt ($\gamma=2$) every method lost coverage. The stratified methods lost less (0.770–0.833, against 0.550–0.726). Among them, SDLC (0.798) was below S-NCP and S-HPD (0.833), which is the same reallocation away from the most extreme outcomes seen above; Remark A.1 (Appendix A) shows why coverage is lowest near the outer end of a tail stratum, where the tilts move mass. The effective sample size of the $\gamma=2$ weights was small (median 49, minimum 5.9), but restricting the analysis to the 15 datasets where it was at least 50 left the ordering unchanged.

**S8.5 Upper-tail alerts.**

**Table S23.** Upper-tail alerts ($\alpha=0.1$; means over datasets): recall, alert rate and precision, the number of datasets with recall at least 0.9, and the expected cost per unit when a missed extreme outcome costs $c$ times a false alert. Set-based alerts (SCP to SDLC-floor) versus dedicated rules built from the same models: conformal tail classifiers (TC-LS, TC-H), conformal selection with FDR level $q_{\mathrm{FDR}}$ (CS-BH-$q_{\mathrm{FDR}}$) and the point-prediction rule (Point).

| Rule       | Recall   | Alert rate   | Precision   | Datasets recall ≥ 0.9   | Cost c=1   | Cost c=10   | Cost c=20   |
|:-----------|:---------|:-------------|:------------|:------------------------|:-----------|:------------|:------------|
| SCP        | 0.947    | 0.273        | 0.512       | 26                      | 0.175      | 0.229       | 0.289       |
| CQR        | 0.952    | 0.286        | 0.495       | 27                      | 0.187      | 0.234       | 0.285       |
| HPD-split  | 0.952    | 0.278        | 0.493       | 25                      | 0.179      | 0.226       | 0.279       |
| BCCP       | 0.983    | 0.468        | 0.379       | 31                      | 0.362      | 0.381       | 0.402       |
| S-NCP      | 0.983    | 0.358        | 0.449       | 31                      | 0.253      | 0.270       | 0.289       |
| S-CQR      | 0.988    | 0.430        | 0.397       | 31                      | 0.323      | 0.334       | 0.346       |
| SDLC       | 0.978    | 0.382        | 0.428       | 31                      | 0.277      | 0.300       | 0.325       |
| SDLC-floor | 0.966    | 0.330        | 0.467       | 30                      | 0.228      | 0.262       | 0.301       |
| TC-LS      | 0.906    | 0.248        | 0.590       | 19                      | 0.159      | 0.253       | 0.357       |
| TC-H       | 0.909    | 0.272        | 0.523       | 18                      | 0.182      | 0.273       | 0.374       |
| CS-BH-0.1  | 0.479    | 0.054        | 0.861       | 6                       | 0.066      | 0.611       | 1.217       |
| CS-BH-0.2  | 0.603    | 0.076        | 0.766       | 10                      | 0.062      | 0.490       | 0.965       |
| Point      | 0.625    | 0.077        | 0.813       | 5                       | 0.056      | 0.457       | 0.903       |


The preferable rule depends on the cost of a miss relative to a false alert. With equal costs, the rules that raise few alerts were cheapest: the point rule and conformal selection (expected cost 0.056 and 0.062 per unit, against 0.277 for SDLC). When a miss costs ten times a false alert, SDLC's expected cost did not differ significantly from that of TC-LS (SDLC lower on 14 of 31 datasets, $p$ = 0.130) and was lower than that of conformal selection on 19 datasets. At a cost ratio of 20, SDLC was cheaper than TC-LS on 22 datasets ($p$ = 0.083), because its recall exceeds the guaranteed 0.9 while TC-LS attains it almost exactly. Among the stratified scores, however, S-NCP gave the cheapest alerts: SDLC's expected cost was higher than S-NCP's on 27 of 31 datasets at $c=10$ and on 29 at $c=20$, because S-NCP raised fewer upper-tail alerts. These $p$-values are unadjusted and descriptive. Alerts read off *marginal* sets (SCP, CQR, HPD-split) were the cheapest on average at high cost ratios (0.279 for HPD-split at $c=20$). They had no recall guarantee, however, and their recall fell below 0.9 on 4–6 datasets. the cost figure of the main text shows cost curves for three valuation datasets.

**S8.6 Sensitivity analyses.**

*Miscoverage level and strata.* The conclusions held at $\alpha=0.05$ and $\alpha=0.2$ (SDLC worst stratum 0.947 and 0.789; Supplementary Table S6). With decile strata the worst decile coverage of SDLC rose to 0.888, from 0.863 with five strata, at a size increase from 0.874 to 0.898. The floor variant (SDLC-floor, $\beta=0.2$) reached its weaker guarantee with smaller sets (worst stratum 0.821, size 0.806).

*Calibration-set size.* With a quarter of the calibration split (on average 1,082 points) stratum-wise validity was retained, but SDLC's sets grew from 0.874 to 1.243, mainly because tail strata with fewer than $1/\alpha-1$ points have an infinite threshold (87 runs, against 2 with the full split; Supplementary Table S8).

*Base learner.* With a two-layer perceptron (5 seeds), marginal methods reached a worst-stratum coverage of 0.650–0.830 and stratified methods 0.889–0.891. SDLC again gave the smallest stratified sets: smaller than BCCP on 23 of 31 datasets (ratio 0.946), than S-NCP on 27 (ratio 0.938, Holm $p$ < 0.001) and than S-HPD on 29 (ratio 0.927).

*Imbalance-aware training.* With DenseWeight sample weights (Steininger et al. 2021), SCP's worst-stratum coverage rose from 0.630 to 0.759, but the shortfall remained large and its sets grew by a factor of 1.31. Stratified calibration remained valid (0.885 for SDLC), and SDLC again gave the smallest stratified sets (Holm $p$ < 0.001, < 0.001, < 0.001 and < 0.001 against BCCP, S-NCP, S-CQR and S-HPD). Imbalance-aware learning and stratified calibration are complementary; the former does not deliver the guarantee.

*Grouped splits.* On three datasets with repeated units (sarcos, superconductivity, video_transcoding) we repeated the main comparison with splits that keep each unit in one part (5 seeds; Supplementary Table S15). On sarcos and superconductivity the results were close to those of random splits (SDLC/S-NCP size ratios 0.965 and 0.914). On video_transcoding, splitting by video increased every method's sets several-fold (SDLC: 0.113 to 0.775), so random splits of this dataset measure interpolation between runs of known videos. Stratified methods still covered their worst stratum at 0.852–0.904, against at most 0.766 for marginal methods, but SDLC's sets were larger than BCCP's (ratio 1.205), and BCCP and S-CQR covered less than nominal marginally (0.875 and 0.873), as expected when exchangeability holds between groups rather than rows. SDLC's size advantage thus depends on the density model transferring to unseen units, and grouped validation is advisable for such data. Post hoc, we also split two datasets by time (Supplementary Table S15). With whole months held out (Bike_Sharing_Demand; the curated data contain no year or day), stratified methods kept a worst-stratum coverage of 0.87 (SDLC) against at most 0.72 for marginal methods, sets grew by about a quarter, and SDLC remained smaller than BCCP and S-NCP. With Moneyball split forward in time (earliest seasons for training, then calibration, latest for test), stratified methods kept close to nominal coverage (0.881 for SDLC) but their sets became three to four times larger than under random splits, SDLC's most of all (3.83 against 3.06 for BCCP). Under a genuine shift over time, the density score loses its advantage.

**S8.7 Error analysis.**

The price of stratum-wise validity (SDLC relative to DLS) rose with the skewness of the target (Spearman $\rho$ = 0.62, $p$ < 0.001) and fell with the calibration-set size ($\rho$ = -0.41). It was largest for forest fires (8.75), whose atom at zero merges the two lower strata. Its upper-stratum coverage also includes automatic misses: whether the largest fire falls into the training split decides the domain $\mathcal{Y}_D$, and in three of ten seeds one to three test targets lay above it. Across all datasets, out-of-domain test targets were rare (at most 2.3% of a run's test points on CTR23 and 0.2% on the held-out data; Supplementary Tables S1–S2). SDLC was larger than S-NCP on 4 datasets (socmob, cars, forest fires and QSAR fish toxicity; ratios up to 1.64), all small or with many ties, so that the scale and noise models rest on few distinct values. The density score helps most when the location model is accurate and the noise is heteroscedastic ($\rho$ = 0.47 with the relative RMSE).

Fig. S4 shows prediction sets for one dataset whose target is capped at its maximum, California housing. CQR's sets around the capped top values are wide but do not cover all of them, whereas the stratified sets do; SDLC adds disjoint pieces in the upper stratum because its threshold there is lower than in the neighbouring stratum. Across all 70 points the methods miss similar numbers of targets (panel titles).

![**Fig. S4.** Prediction sets for 70 test points of the California housing data (seed 0; 14 per calibration stratum, sorted by the true value; dashed lines are stratum boundaries; crosses mark missed targets; the panel titles give the number of missed targets). CQR's sets around the capped top values are wide but do not cover all of them; SDLC adds disjoint pieces in the upper stratum, where its threshold is lower.](/home/user/p_c1_2/Target_Journal_Submission/figures/F9_example_sets_california.png){width=100%}


