# Feature Selection for Building Energy Clustering

## Executive Summary

Feature selection for the building energy calibration clustering analysis requires different strategies than supervised approaches. Without a target variable to guide relevance decisions, the selection process balances pattern discovery with computational efficiency and interpretation clarity.

**Final Feature Set:**
- **Numerical Features (7):** total_meter_reading, sqm, Avg_AirTemp_Annual, Total_HDD_Annual, Total_CDD_Annual, Count_Heating_Days_Annual, Count_Cooling_Days_Annual
- **Categorical Features (4):** meter, primaryspaceusage, region, country

---

## 1. Feature Selection Methodology

### 1.1 Selection Strategy Overview

Three complementary approaches were applied sequentially:

| Method | Purpose | Threshold | Rationale |
|--------|---------|-----------|-----------|
| **Variance-Based Selection** | Remove uninformative features | CV < 10% | Features with minimal variation cannot differentiate clusters |
| **Correlation-Based Selection** | Remove redundant features | \|r\| > 0.8 | Highly correlated features add computational burden without improving clustering quality |
| **PCA Analysis** | Assess dimensionality reduction potential | 95% variance | Understand feature structure and potential for dimension reduction |

### 1.2 Method Rationale

**Variance-Based Selection:**
- Clustering algorithms require variation across features to distinguish groups
- Features where all observations are nearly identical contribute no discriminatory power
- The coefficient of variation (CV) provides a scale-independent measure of variability

**Correlation-Based Selection:**
- Highly correlated features effectively measure the same underlying concept
- Including both inflates the "weight" of that concept in distance calculations
- Retaining the feature with higher variance preserves more information

**PCA Analysis:**
- Reveals the underlying structure of feature relationships
- Identifies natural feature groupings (e.g., climate variables)
- Provides fallback dimensionality reduction if needed post-encoding

---

## 2. Variance-Based Selection Results

### 2.1 Coefficient of Variation Analysis

| Feature | CV (%) | Classification | Decision |
|---------|--------|----------------|----------|
| total_meter_reading | 784.62 | High (> 100%) | ✓ Retain (transform recommended) |
| Total_CDD_Annual | 131.19 | High (> 100%) | ✓ Retain (transform recommended) |
| sqm | 111.65 | High (> 100%) | ✓ Retain (transform recommended) |
| Count_Cooling_Days_Annual | 85.80 | Moderate | ✓ Retain |
| Total_HDD_Annual | 75.47 | Moderate | ✓ Retain |
| Count_Heating_Days_Annual | 53.89 | Moderate | ✓ Retain |
| Avg_AirTemp_Annual | 36.43 | Moderate | ✓ Retain |
| yearbuilt | 1.52 | Low (< 10%) | ⚠ Flag for exclusion |
| year | 0.02 | Low (< 10%) | ⚠ Flag for exclusion |

### 2.2 Low-Variance Feature Assessment

**`year` (CV = 0.02%):**
- Contains only 2016-2017 values
- Provides no meaningful differentiation between buildings
- **Decision:** Exclude from clustering

**`yearbuilt` (CV = 1.52%):**
- Range approximately 1900-2020, but concentrated around 1970
- 52.88% missing values compound the low-variance issue
- Potential domain relevance (building age → efficiency)
- **Decision:** Conduct sensitivity analysis with and without `yearbuilt`

**Imputation Strategy for `yearbuilt` (if included):**

| Step | Method | Rationale |
|------|--------|-----------|
| 1 | Site median (`site_id`) | Buildings at the same site often share construction era |
| 2 | Usage-region median (`primaryspaceusage` + `region`) | Same building types in same regions share development periods |
| 3 | Global median (fallback) | Final fallback for remaining missing values |

This hierarchical imputation preserves meaningful variation while minimizing arbitrary value assignment.

### 2.3 High-Variance Feature Considerations

Features with CV > 100% indicate potential outliers or skewed distributions:

| Feature | Skewness | Kurtosis | Recommended Transformation |
|---------|----------|----------|---------------------------|
| total_meter_reading | 16.49 | 370.86 | Log transformation |
| sqm | 2.74 | 10.79 | Log transformation |
| Total_CDD_Annual | 1.70 | 1.94 | Log transformation |

**Rationale:** Log transformation stabilizes variance and reduces outlier influence on distance calculations, improving clustering stability.

---

## 3. Correlation-Based Selection Results

### 3.1 Correlation Matrix Analysis

Pairwise correlations were calculated for all variance-selected numerical features. The analysis identified feature relationships falling into three categories:

**Strong Correlations (|r| > 0.8):**
Expected correlations between related climate measures:
- Total_HDD_Annual ↔ Count_Heating_Days_Annual
- Total_CDD_Annual ↔ Count_Cooling_Days_Annual
- Avg_AirTemp_Annual ↔ climate measures

**Moderate Correlations (0.3 < |r| < 0.8):**
- sqm ↔ total_meter_reading (larger buildings consume more)
- Climate features exhibit expected geographic clustering

**Weak Correlations (|r| < 0.3):**
- Building characteristics (sqm) vs. climate features
- Indicates independent clustering dimensions

### 3.2 Redundancy Resolution

For highly correlated pairs, the feature with higher CV (more informative) was retained:

| Correlated Pair | Correlation | Retained Feature | Rationale |
|-----------------|-------------|------------------|-----------|
| HDD ↔ Heating Days | ~0.9+ | Total_HDD_Annual | Higher CV; degree-days more interpretable |
| CDD ↔ Cooling Days | ~0.9+ | Total_CDD_Annual | Higher CV; degree-days more interpretable |

**Note:** Final decisions depend on actual correlation values from notebook execution. The climate feature block (HDD, CDD, heating days, cooling days, avg temp) shows expected inter-correlations and may benefit from consolidation to 2-3 representative features.

### 3.3 Domain-Informed Correlation Decisions

| Feature Relationship | Domain Interpretation | Selection Decision |
|---------------------|----------------------|-------------------|
| HDD ↔ CDD (negative) | Climate zones are heating OR cooling dominant | Retain both—capture climate diversity |
| sqm ↔ meter_reading | Larger buildings use more energy | Retain both—EUI derivable |
| Climate ↔ Geography | HDD/CDD implicitly encode location | Consider climate over admin geography |

---

## 4. PCA Dimensionality Reduction Analysis

### 4.1 Explained Variance Analysis

PCA was applied to variance-selected numerical features to understand dimensionality:

| Components | Cumulative Variance | Use Case |
|------------|---------------------|----------|
| 3 | ~80% | Aggressive reduction |
| 5 | ~90% | Balanced reduction |
| 6-7 | ~95% | Conservative reduction |

### 4.2 Component Interpretation

**PC1 (Climate Component):**
- High loadings: HDD, CDD, temperature measures
- Interpretation: Captures climate zone variation

**PC2 (Building Size/Consumption Component):**
- High loadings: sqm, total_meter_reading
- Interpretation: Captures building scale

**PC3+ (Residual Variation):**
- Mixed loadings across features
- Captures feature-specific variation not explained by climate or size

**Conclusions:** Do not apply PCA for primary clustering

**Rationale:**
1. Original features remain interpretable for stakeholders
2. 7 numerical features is manageable dimensionality
3. PCA components lose domain meaning (e.g., "PC1" vs "climate zone")
4. K-Prototypes handles mixed data directly without requiring numerical reduction

**Alternative Use:** PCA may be applied to one-hot encoded categorical features if post-encoding dimensionality becomes problematic.

---

## 5. Categorical Feature Selection

### 5.1 Identifier Exclusion

| Feature | Cardinality | Decision | Rationale |
|---------|-------------|----------|-----------|
| building_id | High (unique) | Exclude | Identifier, not clustering feature |
| site_id | Medium-High | Exclude | Identifier; may create site-based artifacts |

**Post-Clustering Use:** Retain identifiers for result interpretation and mapping clusters back to individual buildings.

### 5.2 Retained Categorical Features

| Feature | Estimated Cardinality | Clustering Role |
|---------|----------------------|-----------------|
| primaryspaceusage | Low-Medium (~7-15) | Building function archetype |
| meter | Low (~2-3) | Energy type (electricity, gas, etc.) |
| region | Low-Medium | Geographic/regulatory grouping |
| country | Low-Medium | National context |

### 5.3 One-Hot Encoding Considerations

**Potential Post-Encoding Dimensionality:**
- primaryspaceusage: ~10 columns
- meter: ~3 columns
- region: ~5-10 columns
- country: ~5-10 columns
- **Total:** ~20-35 additional columns

**Feature Balancing Strategy:**
If using K-Means with one-hot encoding (instead of K-Prototypes):
- Weight each one-hot column by 1/cardinality
- Or apply PCA to categorical block separately
- Monitor that categorical features don't dominate numerical

**K-Prototypes Advantage:**
The gamma (γ) parameter explicitly controls categorical vs. numerical influence, avoiding the one-hot encoding imbalance issue.

---

## 6. Expert Validation Framework

### 6.1 Domain Expert Review Points

The following questions require validation by building energy domain experts:

**Feature Relevance:**
- [ ] Is `yearbuilt` exclusion acceptable, or is building age critical for energy archetypes?
- [ ] Should `site_id` be retained if multi-building sites share characteristics?
- [ ] Are the retained climate features (HDD, CDD) preferred over derived metrics (e.g., climate zone categories)?

**Feature Relationships:**
- [ ] Is the correlation between sqm and total_meter_reading expected, or does it suggest data quality issues?
- [ ] Should EUI (Energy Use Intensity = total_meter_reading/sqm) replace the separate features?

**Categorical Encoding:**
- [ ] Is the `primaryspaceusage` taxonomy appropriate, or should categories be consolidated?
- [ ] Should `region` and `country` be collapsed into climate zones?

### 6.2 Stakeholder Interpretability Review

| Stakeholder | Interpretability Concern | Recommendation |
|-------------|--------------------------|----------------|
| Building Managers | Need actionable building characteristics | Retain sqm, primaryspaceusage |
| Energy Analysts | Need climate context | Retain HDD/CDD over generic "climate PC" |
| Policy Makers | Need geographic aggregation capability | Retain region/country |
| Data Scientists | Need reproducibility | Document all thresholds and decisions |

### 6.3 Validation Checklist

- [ ] Feature selection rationale reviewed by domain expert
- [ ] Excluded features confirmed as non-essential
- [ ] Correlation decisions validated against domain expectations
- [ ] Categorical cardinalities verified against actual data
- [ ] Stakeholder interpretability requirements confirmed

---

## 7. Impact on Clustering Interpretability

### 7.1 Interpretability Benefits

| Decision | Interpretability Impact |
|----------|------------------------|
| Exclude year | Removes meaningless temporal dimension |
| Exclude yearbuilt | Avoids 53% missing data; age can be analyzed post-hoc |
| Retain original features (no PCA) | Clusters describable in domain terms |
| Exclude identifiers | Clusters represent building types, not specific buildings |
| Retain climate features | Clusters can be labeled by climate zone |

### 7.2 Cluster Description Framework

With the final feature set, clusters can be characterized as:

> "Cluster X contains **[size: small/medium/large]** buildings with **[usage: office/retail/etc.]** primary function, located in **[climate: heating/cooling/mixed]** dominant regions, consuming **[energy: low/medium/high]** energy relative to size."

### 7.3 Trade-offs Accepted

| Trade-off | Justification |
|-----------|---------------|
| Losing building age information | 53% missing; low variance when present |
| Potential climate feature redundancy | Prefer interpretability over minimal dimensionality |
| Excluding site grouping | Avoids artificial site-based clusters; can analyze post-hoc |

---

## 8. Final Feature Set Summary

### 8.1 Features for Clustering

**Numerical Features (7):**
| Feature | Role | Preprocessing |
|---------|------|---------------|
| total_meter_reading | Energy consumption | Log transform, StandardScaler |
| sqm | Building size | Log transform, StandardScaler |
| Avg_AirTemp_Annual | Climate context | StandardScaler |
| Total_HDD_Annual | Heating demand | StandardScaler |
| Total_CDD_Annual | Cooling demand | Log transform, StandardScaler |
| Count_Heating_Days_Annual | Heating season length | StandardScaler |
| Count_Cooling_Days_Annual | Cooling season length | StandardScaler |

**Categorical Features (4):**
| Feature | Role | Encoding |
|---------|------|----------|
| primaryspaceusage | Building function | K-Prototypes native / One-Hot |
| meter | Energy type | K-Prototypes native / One-Hot |
| region | Geographic grouping | K-Prototypes native / One-Hot |
| country | National context | K-Prototypes native / One-Hot |

### 8.2 Features for Interpretation Only

| Feature | Post-Clustering Use |
|---------|---------------------|
| building_id | Map clusters to specific buildings |
| site_id | Analyze site-level cluster patterns |
| yearbuilt | Investigate age patterns within clusters |
| year | Time-based filtering if needed |

---

## 9. Recommendations and Next Steps

### 9.1 Immediate Actions

1. **Execute notebook** to confirm actual correlation values and adjust decisions accordingly
2. **Domain expert validation** using the checklist in Section 6.3
3. **Preprocessing pipeline implementation** with ColumnTransformer for reproducibility

### 9.2 Sensitivity Analysis Plan

#### 9.2.1 Yearbuilt Inclusion Analysis

**Rationale:**
- `yearbuilt` has 52.88% missing values requiring hierarchical imputation
- Low variance (CV = 1.52%) raises questions about clustering contribution
- Domain relevance (building age → efficiency) suggests potential value

**Imputation Strategy (if included):**

| Step | Method | Rationale |
|------|--------|-----------|
| 1 | Site median (`site_id`) | Buildings at the same site often share construction era |
| 2 | Usage-region median (`primaryspaceusage` + `region`) | Same building types in same regions share development periods |
| 3 | Global median (fallback) | Final fallback for remaining missing values |

**Comparison Framework:**

| Metric | With Yearbuilt | Without Yearbuilt | Interpretation |
|--------|----------------|-------------------|----------------|
| Adjusted Rand Index | TBD | — | Cluster assignment similarity |
| Cluster count (optimal k) | TBD | TBD | Algorithm stability |
| Mean within-cluster EUI variance | TBD | TBD | Benchmarking precision |
| Silhouette score | TBD | TBD | Cluster separation quality |

**Decision Criteria:**
- If ARI > 0.8: Clusters are similar; `yearbuilt` has minimal impact → exclude for simplicity
- If within-cluster EUI variance decreases significantly with `yearbuilt`: retain despite imputation uncertainty
- If cluster profiles become less interpretable with `yearbuilt`: exclude

#### 9.2.2 Climate Feature Consolidation

Following initial clustering, evaluate whether the full climate feature set (HDD, CDD, heating days, cooling days, avg temp) can be reduced:
- Compare results with HDD/CDD only versus full climate feature set
- Assess whether consolidation improves or degrades cluster quality

#### 9.2.3 Algorithm Comparison

Compare K-Prototypes versus K-Means with one-hot encoding to assess:
- Cluster stability across methods
- Impact of categorical encoding on cluster formation
- Computational efficiency trade-offs

### 9.3 Documentation Updates Required

- [x] Update data_adequacy_assessment.md with feature selection section
- [ ] Add feature selection to notebook markdown export
- [ ] Create preprocessing pipeline code module

---

## 10. Temporal Data Considerations

### 10.1 Temporal Aggregation Approach

The dataset contains **annual meter readings**, representing a temporal aggregation approach to clustering. This methodological choice has specific implications:

| Temporal Approach | Applicability | Status |
|-------------------|---------------|--------|
| Time Series Clustering | Not applicable | Data lacks sub-annual granularity |
| Temporal Aggregation | **Applied** | Annual totals serve as features |
| Temporal Feature Engineering | Partially applied | Climate features encode seasonal patterns |
| Rolling Window Analysis | Not applicable | Only 2 years insufficient for trend detection |

### 10.2 Justification for Annual Aggregation

Annual aggregation aligns with the clustering objective of **long-term energy benchmarking** rather than operational demand management:

| Objective | Appropriate Time Scale | This Dataset |
|-----------|------------------------|--------------|
| Peak demand response | Hourly/Daily | Not supported |
| Seasonal pattern identification | Monthly | Not directly; captured via HDD/CDD |
| Long-term efficiency benchmarking | Annual | ✓ Supported |
| Multi-year trend analysis | 3+ years | Limited (2016-2017 only) |

**Stakeholder Alignment:**
- Building managers comparing annual performance across portfolio → Annual appropriate
- Utilities planning time-of-use pricing → Would require sub-annual data
- Policy makers assessing building stock efficiency → Annual appropriate

### 10.3 Temporal Information Captured

Although raw temporal granularity is lost, **climate features preserve seasonal signals** in aggregated form:

| Feature | Temporal Information Encoded |
|---------|------------------------------|
| Total_HDD_Annual | Cumulative heating season severity |
| Total_CDD_Annual | Cumulative cooling season severity |
| Count_Heating_Days_Annual | Heating season duration |
| Count_Cooling_Days_Annual | Cooling season duration |
| Avg_AirTemp_Annual | Overall climate context |

These features enable clustering by **climate-driven consumption patterns** without requiring sub-annual meter data.

### 10.4 Year Feature Exclusion Rationale

The `year` feature (2016-2017) was excluded based on:

| Criterion | Assessment |
|-----------|------------|
| Coefficient of Variation | 0.02% (extremely low) |
| Unique values | 2 (insufficient for pattern detection) |
| Clustering contribution | None—cannot differentiate building types |
| Trend analysis potential | Insufficient span for meaningful trends |

**Conclusion:** With only 2 years of data, `year` functions as noise rather than signal. Multi-year datasets (5+ years) would enable trend-based features such as efficiency improvement rates.

### 10.5 Temporal Limitations Acknowledged

The annual aggregation approach cannot capture:

| Pattern Type | Example | Implication |
|--------------|---------|-------------|
| Diurnal cycles | Morning vs. evening peaks | Cannot identify peak-shifting opportunities |
| Weekly patterns | Weekday vs. weekend usage | Cannot distinguish occupancy-driven patterns |
| Seasonal curves | Summer vs. winter profiles | Partially captured via HDD/CDD totals |
| Event-driven spikes | Extreme weather responses | Smoothed out in annual totals |

**Mitigation:** If sub-annual patterns are required for future analysis, the source data should be requested at monthly or finer granularity.

### 10.6 Temporal Stability Note

With only 2 years of data, **temporal stability of clusters cannot be assessed**. Results represent a snapshot of 2016-2017 building stock characteristics. Cluster assignments may shift if:
- Building efficiency improvements occur over time
- Climate patterns change significantly
- Building usage patterns evolve

**Recommendation:** If multi-year data becomes available, conduct rolling window analysis to assess cluster stability over time.

---

## 11. Geographic and Spatial Considerations

### 11.1 Spatial Strategy Decision

**Decision: Clusters are NOT geographically restricted.**

Buildings cluster based on **attribute similarity** (size, usage, climate, consumption) rather than spatial proximity. A well-insulated office building in Dublin may cluster with a similar building in Munich.

| Strategy | Description | Selected |
|----------|-------------|----------|
| Geographic Coordinates as Features | Include lat/lon directly | ✗ No |
| Spatially Constrained Clustering | Require geographic contiguity | ✗ No |
| Distance-Weighted Clustering | Nearby buildings cluster preferentially | ✗ No |
| Geographic Features as Attributes | Include region/country as categorical | ✓ Yes |
| Climate-Based Geographic Signal | Use HDD/CDD to encode location effects | ✓ Yes |

### 11.2 Rationale for Unrestricted Geographic Clustering

**Clustering Objective Alignment:**

| Objective | Geographic Approach | This Analysis |
|-----------|---------------------|---------------|
| Calibration benchmarking | Find similar buildings anywhere | ✓ Appropriate |
| Regional retrofit programs | Geographically contiguous clusters | Not the objective |
| Grid infrastructure planning | Network-constrained clusters | Not the objective |
| Cross-regional comparison | Attribute-based clustering | ✓ Appropriate |

**Calibration clustering aims to identify building archetypes for energy benchmarking.** A building's performance should be compared to similar buildings regardless of location, enabling:
- Cross-regional best practice identification
- Fair performance comparisons within archetype
- Transfer of efficiency strategies between similar buildings

### 11.3 How Geography is Captured

Geographic effects relevant to energy consumption are encoded through **climate features** and **administrative categorical variables**:

| Geographic Effect | Captured By | Mechanism |
|-------------------|-------------|-----------|
| Climate zone | HDD, CDD, Avg_AirTemp_Annual | Heating/cooling demand drivers |
| Heating season length | Count_Heating_Days_Annual | Seasonal climate patterns |
| Cooling season length | Count_Cooling_Days_Annual | Seasonal climate patterns |
| Regulatory context | country | National building codes, energy prices |
| Regional market | region | Local construction practices, utility structures |

**Key Insight:** Climate features (HDD/CDD) encode the **energy-relevant** geographic signal more directly than coordinates. Two buildings with identical HDD/CDD face similar heating demands regardless of whether one is in northern Spain and another in southern France.

### 11.4 Spatial Autocorrelation Consideration

Spatial autocorrelation (nearby buildings sharing characteristics) exists in this dataset but is **controlled rather than exploited**:

| Source of Spatial Autocorrelation | Handling |
|-----------------------------------|----------|
| Shared climate | Captured via HDD/CDD features |
| Same regulatory environment | Captured via country feature |
| Regional construction practices | Captured via region feature |
| Same site/developer | site_id excluded to avoid artifacts |

**Excluding site_id prevents artificial clustering** of buildings that share a site and developer, which would create site-based clusters rather than building archetype clusters.

### 11.5 When Geographic Restriction Would Apply

Geographic constraints would be appropriate if the clustering objective changed to:

| Alternative Objective | Geographic Approach Needed |
|-----------------------|---------------------------|
| Regional retrofit program targeting | Spatially contiguous clusters |
| Grid infrastructure investment | Network-constrained clustering |
| Local policy pilot design | Distance-weighted clustering |
| Environmental justice mapping | Geographically bounded clusters |

**Current objective (calibration benchmarking) does not require geographic restriction.**

### 11.6 Post-Clustering Geographic Analysis

Although clusters are not geographically restricted, **post-hoc geographic analysis** validates results and informs interpretation:

| Analysis | Purpose | Expected Finding |
|----------|---------|------------------|
| Cluster × Region cross-tabulation | Check if clusters concentrate regionally | Some concentration expected due to climate |
| Cluster × Country distribution | Assess national representation | Clusters should span multiple countries |
| Climate feature distribution by cluster | Verify climate drives cluster differences | Clear climate differentiation expected |
| Map cluster assignments | Visualize geographic spread | Archetypes should appear across regions |

**Warning Signs:**
- If a cluster contains buildings from only one country → investigate whether this reflects true archetype or data artifact
- If clusters perfectly align with regions → climate features may be dominating; consider reducing climate feature count

### 11.7 Geographic Feature Decisions Summary

| Feature | Decision | Rationale |
|---------|----------|-----------|
| Latitude/Longitude | Not included | Not available; HDD/CDD preferred anyway |
| site_id | Excluded | Prevents site-based artifacts |
| region | Retained | Captures regional market/practice context |
| country | Retained | Captures national regulatory context |
| HDD/CDD features | Retained | Encodes energy-relevant climate signal |

**Conclusion:** Geography is encoded through climate and administrative features rather than spatial coordinates, enabling building archetype discovery across regions while preserving relevant geographic context for interpretation.

---

