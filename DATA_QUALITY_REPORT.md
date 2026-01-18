# Data Quality Assessment and Validation Report

## Executive Summary

This report contains a comprehensive data quality assessment for the building energy dataset. Data quality directly determines clustering success; in unsupervised contexts, data quality assessment requires evaluating whether the selected dataset contains sufficient signal to support meaningful clustering while identifying issues that could mislead stakeholders.

**Quality Assessment Dimensions:**

| Dimension | Status | Key Finding |
|-----------|--------|-------------|
| Data completeness | △ | 46.2% complete cases; yearbuilt 52.88% missing |
| Accuracy | △ | High outlier counts in energy/size features |
| Logical Consistency | ? | Requires validation of variable relationships |
| External Benchmarks | ? | EUI comparison to published standards pending |
| Representativeness | ? | Sample vs. population comparison pending |
| Subgroup Quality | ? | Quality variation by region/type pending |

**Legend:** ✓ = Adequate, △ = Action needed, ✗ = Concern, ? = Assessment pending

---

## 1. Data Provenance Documentation

### 1.1 Source Information

| Attribute | Value | Notes |
|-----------|-------|-------|
| Dataset Name | Building Energy Calibration Dataset | |
| Source | TBD - Document data origin | |
| Collection Period | 2016-2017 | Annual meter readings |
| Geographic Scope | Multiple countries/regions | Europe-focused based on feature names |
| Collection Method | TBD - Meter readings + building records | |
| Data Provider | TBD | |

### 1.2 Known Data Collection Characteristics

**Questions Requiring Clarification:**

- [ ] What meter types are represented (electricity, gas, district heating)?
- [ ] How were buildings selected for inclusion (census, sample, voluntary)?
- [ ] What is the definition of `sqm` (gross floor area, net floor area, conditioned area)?
- [ ] What weather stations provided climate data (HDD, CDD)?
- [ ] Are meter readings actual or estimated?
- [ ] What quality control was applied during collection?

### 1.3 Data Integration Notes

| Data Component | Likely Source | Integration Consideration |
|----------------|---------------|---------------------------|
| Meter readings | Utility records | May have different reporting standards |
| Building characteristics | Property registers | sqm definitions may vary |
| Climate data | Weather services | Weather station proximity varies |
| Geographic identifiers | Administrative records | Coding consistency across sources |

**Recommendation:** Document data sources and integration methods before finalizing clustering analysis.

---

## 2. Completeness Analysis

### 2.1 Missing Data Summary

| Feature | Missing Count | Missing % | Complete Count | Severity |
|---------|---------------|-----------|----------------|----------|
| yearbuilt | 3,121 | 52.88% | 2,781 | **Critical** |
| region | 1,005 | 17.03% | 4,897 | Moderate |
| country | 1,005 | 17.03% | 4,897 | Moderate |
| primaryspaceusage | 55 | 0.93% | 5,847 | Low |
| Other features | 0 | 0.00% | 5,902 | None |

**Overall Completeness:**
- Total observations: 5,902
- Complete cases (all features): 2,726 (46.2%)
- Complete cases (excluding yearbuilt): ~4,800 (estimated ~81%)

### 2.2 Missingness Pattern Analysis

**Pattern Type Assessment:**

| Feature | Likely Mechanism | Evidence | Implication |
|---------|------------------|----------|-------------|
| yearbuilt | MAR or MNAR | Older buildings may lack records | Imputation may introduce bias |
| region/country | MAR | Specific data sources lack geography | Geographic analysis limited for subset |
| primaryspaceusage | MCAR | Low rate, likely random gaps | Simple imputation acceptable |

**Co-occurrence Analysis Required:**

- [ ] Do buildings with missing `yearbuilt` also have missing `region/country`?
- [ ] Are missingness patterns concentrated in specific sites?
- [ ] Does missingness correlate with building size or energy consumption?

### 2.3 Subgroup Missingness Analysis

**Framework for Analysis:**

| Subgroup Variable | Check | Concern if True |
|-------------------|-------|-----------------|
| By meter type | Does missingness vary by meter? | Systematic data collection differences |
| By region | Is missingness concentrated in certain regions? | Geographic data access inequity |
| By building size | Are small/large buildings more likely to have missing data? | Sample bias |
| By primaryspaceusage | Do certain building types have more missing data? | Usage-type bias |

**Analysis Code Template:**
```python
# Missingness by subgroup analysis
for subgroup in ['meter', 'region', 'primaryspaceusage']:
    missing_by_subgroup = df.groupby(subgroup)['yearbuilt'].apply(
        lambda x: x.isnull().mean() * 100
    )
    print(f"\nMissingness by {subgroup}:")
    print(missing_by_subgroup.round(1))
```

### 2.4 Completeness Recommendations

| Priority | Action | Rationale |
|----------|--------|-----------|
| High | Investigate yearbuilt missingness pattern | 52.88% missing requires understanding before imputation |
| High | Document region/country data source | Identify why 17% lack geographic info |
| Medium | Conduct subgroup missingness analysis | Ensure no systematic bias |
| Low | Simple imputation for primaryspaceusage | 0.93% missing is manageable |

---

## 3. Accuracy Validation

### 3.1 Implausible Value Checks

**Numerical Features - Domain Constraints:**

| Feature | Valid Range | Constraint Rationale | Check Required |
|---------|-------------|---------------------|----------------|
| total_meter_reading | > 0 | Energy consumption cannot be negative | Count negatives |
| sqm | > 0 | Building area cannot be negative | Count negatives |
| sqm | < 1,000,000 | Upper bound for single buildings | Count extreme values |
| yearbuilt | 1800-2017 | Reasonable building age range | Count out-of-range |
| Avg_AirTemp_Annual | -20 to 35°C | Reasonable annual averages | Count out-of-range |
| Total_HDD_Annual | ≥ 0 | Degree days cannot be negative | Count negatives |
| Total_CDD_Annual | ≥ 0 | Degree days cannot be negative | Count negatives |

**Validation Code Template:**
```python
# Domain constraint validation
validation_results = {}

# Negative values where not allowed
for col in ['total_meter_reading', 'sqm', 'Total_HDD_Annual', 'Total_CDD_Annual']:
    negatives = (df[col] < 0).sum()
    validation_results[f'{col}_negative'] = negatives

# Yearbuilt range
out_of_range = ((df['yearbuilt'] < 1800) | (df['yearbuilt'] > 2017)).sum()
validation_results['yearbuilt_out_of_range'] = out_of_range

# Extreme sqm values
extreme_sqm = (df['sqm'] > 500000).sum()
validation_results['sqm_extreme'] = extreme_sqm
```

### 3.2 Outlier Analysis

**Statistical Outlier Detection:**

| Feature | CV (%) | Expected Outliers | Detection Method |
|---------|--------|-------------------|------------------|
| total_meter_reading | 784.62 | Many | IQR + domain benchmarks |
| sqm | 111.65 | Moderate | IQR |
| Total_CDD_Annual | 131.19 | Moderate | IQR |
| Count_Cooling_Days_Annual | 85.80 | Few | IQR |
| Total_HDD_Annual | 75.47 | Few | IQR |

**Outlier Counts (IQR Method) - To Be Calculated:**

| Feature | Lower Fence | Upper Fence | Outliers Below | Outliers Above | Total Outliers |
|---------|-------------|-------------|----------------|----------------|----------------|
| total_meter_reading | TBD | TBD | TBD | TBD | TBD |
| sqm | TBD | TBD | TBD | TBD | TBD |
| Total_CDD_Annual | TBD | TBD | TBD | TBD | TBD |

**Outlier Investigation Protocol:**

1. **Identify outliers** using IQR method (1.5 × IQR from Q1/Q3)
2. **Cross-reference** outliers with other features (is high energy consumption explained by large sqm?)
3. **Domain validation** - consult benchmarks for plausible ranges
4. **Decision**: Remove (if error), retain (if genuine), or winsorize (if extreme but plausible)

### 3.3 Distribution Analysis

**Skewness and Kurtosis Assessment:**

| Feature | Skewness | Kurtosis | Distribution Type | Action |
|---------|----------|----------|-------------------|--------|
| total_meter_reading | 16.49 | 370.86 | Extremely right-skewed | Log transform |
| sqm | 2.74 | 10.79 | Right-skewed | Log transform |
| Total_CDD_Annual | 1.70 | 1.94 | Moderately skewed | Log transform |
| yearbuilt | -0.51 | -0.54 | Slightly left-skewed | No transform |
| Avg_AirTemp_Annual | 0.40 | -1.36 | Approximately normal | No transform |
| Total_HDD_Annual | 0.15 | -1.31 | Approximately normal | No transform |

**Interpretation:**
- Features with |skewness| > 1 or kurtosis > 3 require transformation before distance-based clustering
- Extreme kurtosis (370.86 for total_meter_reading) suggests very heavy tails with significant outliers

### 3.4 Accuracy Recommendations

| Priority | Action | Feature(s) |
|----------|--------|------------|
| Critical | Check for negative values | total_meter_reading, sqm, HDD, CDD |
| Critical | Investigate extreme kurtosis | total_meter_reading |
| High | Apply log transformation | total_meter_reading, sqm, Total_CDD_Annual |
| Medium | Validate yearbuilt range | yearbuilt |
| Medium | Document outlier handling decisions | All high-CV features |

---

## 4. Logical Consistency Checks

### 4.1 Variable Relationship Validation

**Expected Relationships:**

| Variable Pair | Expected Relationship | Validation Check |
|---------------|----------------------|------------------|
| sqm ↔ total_meter_reading | Positive correlation | Larger buildings consume more |
| Total_HDD_Annual ↔ Total_CDD_Annual | Negative correlation | Climate zones are heating OR cooling dominant |
| Total_HDD_Annual ↔ Avg_AirTemp_Annual | Negative correlation | Colder climates have more heating needs |
| Total_CDD_Annual ↔ Avg_AirTemp_Annual | Positive correlation | Warmer climates have more cooling needs |
| Count_Heating_Days ↔ Total_HDD_Annual | Strong positive | More heating days = more heating degree days |
| Count_Cooling_Days ↔ Total_CDD_Annual | Strong positive | More cooling days = more cooling degree days |

**Consistency Check Code Template:**
```python
# Correlation consistency checks
expected_relationships = [
    ('sqm', 'total_meter_reading', 'positive'),
    ('Total_HDD_Annual', 'Total_CDD_Annual', 'negative'),
    ('Total_HDD_Annual', 'Avg_AirTemp_Annual', 'negative'),
    ('Total_CDD_Annual', 'Avg_AirTemp_Annual', 'positive'),
]

for var1, var2, expected in expected_relationships:
    corr = df[[var1, var2]].corr().iloc[0, 1]
    actual = 'positive' if corr > 0 else 'negative'
    status = '✓' if actual == expected else '✗ INCONSISTENT'
    print(f"{var1} ↔ {var2}: r={corr:.3f} ({actual}) {status}")
```

### 4.2 Energy Use Intensity (EUI) Validation

EUI (Energy Use Intensity) provides a normalized metric for identifying implausible combinations:

**EUI Calculation:**
```
EUI = total_meter_reading / sqm
```

**EUI Plausibility Ranges by Building Type:**

| Building Type | Typical EUI Range (kWh/m²/year) | Source |
|---------------|--------------------------------|--------|
| Office | 100-300 | CIBSE TM46 |
| Retail | 200-400 | CIBSE TM46 |
| Education | 100-200 | CIBSE TM46 |
| Healthcare | 300-600 | CIBSE TM46 |
| Warehouse | 50-150 | CIBSE TM46 |
| Residential | 50-200 | Various |

**EUI Validation Protocol:**

1. Calculate EUI for all buildings
2. Flag buildings with EUI < 10 kWh/m²/year (implausibly low)
3. Flag buildings with EUI > 1000 kWh/m²/year (implausibly high)
4. Cross-reference extreme EUI with primaryspaceusage
5. Investigate flagged buildings for data errors

### 4.3 Geographic-Climate Consistency

Buildings should have climate features consistent with their geographic location:

| Check | Validation |
|-------|------------|
| Region ↔ HDD/CDD alignment | Northern regions should have higher HDD |
| Country ↔ climate features | Same-country buildings should have similar climate ranges |
| Impossible combinations | Mediterranean region with very high HDD is suspicious |

**Validation Code Template:**
```python
# Climate by region consistency
climate_by_region = df.groupby('region')[['Total_HDD_Annual', 'Total_CDD_Annual']].agg(['mean', 'std'])
print("Climate features by region:")
print(climate_by_region)

# Flag buildings with climate values >3 SD from regional mean
# (may indicate data integration errors)
```

### 4.4 Identifier Consistency

| Check | Expected | Issue if Violated |
|-------|----------|-------------------|
| building_id uniqueness | Each building has unique ID | Duplicate records |
| site_id grouping | Buildings at same site share site_id | Data integration error |
| building_id ↔ site_id | Multiple buildings can share site_id | None (expected) |

**Validation Code Template:**
```python
# Check for duplicate building_ids
duplicates = df['building_id'].duplicated().sum()
print(f"Duplicate building_ids: {duplicates}")

# Check site_id consistency
buildings_per_site = df.groupby('site_id')['building_id'].nunique()
print(f"Buildings per site - min: {buildings_per_site.min()}, max: {buildings_per_site.max()}")
```

### 4.5 Consistency Recommendations

| Priority | Check | Action if Failed |
|----------|-------|------------------|
| Critical | No negative energy/area values | Remove or investigate records |
| Critical | EUI within plausible range | Investigate extreme values |
| High | Expected correlations hold | Investigate unexpected patterns |
| High | No duplicate building_ids | Deduplicate records |
| Medium | Climate-geography alignment | Flag potential data integration errors |

---

## 5. External Benchmark Validation

### 5.1 Energy Benchmark Sources

| Source | Coverage | Metrics | Use Case |
|--------|----------|---------|----------|
| CIBSE TM46 | UK | EUI by building type | European benchmark |
| ASHRAE 90.1 | US | Energy targets | Cross-reference |
| EU Energy Performance | Europe | kWh/m²/year by class | Regulatory context |
| EnergyStar Portfolio Manager | US | Percentile rankings | Comparative benchmark |

### 5.2 EUI Distribution Comparison Framework

**Sample EUI Distribution vs. Published Benchmarks:**

| Statistic | Sample EUI | CIBSE TM46 Typical | Assessment |
|-----------|------------|---------------------|------------|
| Median | TBD | ~150-200 kWh/m²/year | TBD |
| 25th percentile | TBD | ~100 kWh/m²/year | TBD |
| 75th percentile | TBD | ~300 kWh/m²/year | TBD |
| Min | TBD | >10 kWh/m²/year | TBD |
| Max | TBD | <1000 kWh/m²/year | TBD |

### 5.3 Benchmark Comparison by Building Type

**Framework for Analysis:**

| primaryspaceusage | Sample Median EUI | Benchmark EUI | Ratio | Assessment |
|-------------------|-------------------|---------------|-------|------------|
| Office | TBD | 150-200 | TBD | TBD |
| Retail | TBD | 250-350 | TBD | TBD |
| Education | TBD | 120-180 | TBD | TBD |
| Healthcare | TBD | 350-500 | TBD | TBD |

**Interpretation Guidelines:**
- Ratio 0.8-1.2: Sample aligns with benchmarks
- Ratio < 0.5: Sample may underreport or have metering issues
- Ratio > 2.0: Sample may include data errors or atypical buildings

### 5.4 Climate Feature Benchmark Validation

**HDD/CDD Benchmarks by Climate Zone:**

| Climate Zone | Typical HDD Range | Typical CDD Range |
|--------------|-------------------|-------------------|
| Northern Europe | 2500-4000 | 0-200 |
| Central Europe | 2000-3000 | 100-400 |
| Southern Europe | 1000-2000 | 400-1000 |
| Mediterranean | 500-1500 | 500-1200 |

**Validation:** Compare sample HDD/CDD distributions against expected ranges for regions represented.

### 5.5 Benchmark Validation Recommendations

| Priority | Action | Purpose |
|----------|--------|---------|
| High | Calculate EUI for all buildings | Enable benchmark comparison |
| High | Compare median EUI to CIBSE TM46 | Validate overall data plausibility |
| Medium | Compare EUI by building type | Identify usage-specific anomalies |
| Medium | Validate HDD/CDD against regional norms | Check climate data integration |

---

## 6. Representativeness Evaluation

### 6.1 Sample vs. Population Comparison Framework

**Target Population Definition:**
The target population for calibration clustering is the European commercial and institutional building stock.

**Comparison Dimensions:**

| Dimension | Sample Characteristic | Population Benchmark | Source | Assessment |
|-----------|----------------------|---------------------|--------|------------|
| Building size distribution | TBD | TBD | Eurostat/national registries | TBD |
| Building type mix | TBD | TBD | Commercial building surveys | TBD |
| Geographic coverage | TBD | TBD | Country/region population | TBD |
| Building age distribution | TBD | TBD | Building stock studies | TBD |
| Climate zone coverage | TBD | TBD | HDD/CDD maps | TBD |

### 6.2 Known Population Benchmarks

**European Building Stock Characteristics:**

| Characteristic | Typical Distribution | Source |
|----------------|---------------------|--------|
| Office buildings | 15-25% of commercial stock | EU Building Stock Observatory |
| Retail buildings | 20-30% of commercial stock | EU Building Stock Observatory |
| Pre-1980 buildings | 60-70% of stock | Various national studies |
| >10,000 m² buildings | 5-10% of stock | Eurostat |

### 6.3 Sample Characteristics Analysis

**Building Type Distribution:**
```python
# Calculate sample distribution
type_distribution = df['primaryspaceusage'].value_counts(normalize=True) * 100
print("Sample building type distribution:")
print(type_distribution.round(1))
```

**Geographic Coverage:**
```python
# Calculate geographic distribution
geo_distribution = df['country'].value_counts(normalize=True) * 100
print("Sample country distribution:")
print(geo_distribution.round(1))
```

**Building Size Distribution:**
```python
# Size distribution
size_percentiles = df['sqm'].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
print("Sample size distribution:")
print(size_percentiles)
```

### 6.4 Representativeness Concerns

| Potential Bias | Concern | Mitigation |
|----------------|---------|------------|
| Voluntary participation | Larger/more sophisticated buildings may be overrepresented | Weight results or document limitation |
| Data availability | Buildings with better records may dominate | Acknowledge in interpretation |
| Geographic concentration | Certain countries may be overrepresented | Report geographic breakdown |
| Building type skew | Certain usage types may dominate | Stratify analysis by type |
| Missing yearbuilt | Older buildings may be systematically excluded | Sensitivity analysis with/without yearbuilt |

### 6.5 Representativeness Recommendations

| Priority | Action | Purpose |
|----------|--------|---------|
| Medium | Document sample building type distribution | Enable comparison to population |
| Medium | Document geographic coverage | Identify potential regional bias |
| Medium | Compare size distribution to known benchmarks | Assess large-building bias |
| Low | Acknowledge representativeness limitations | Transparent reporting |

---

## 7. Subgroup Quality Analysis

### 7.1 Quality Metrics by Subgroup Framework

Quality should be consistent across subgroups to avoid biased clustering.

**Analysis Framework:**

| Subgroup | Metrics to Compare |
|----------|-------------------|
| By meter type | Missingness rate, outlier rate, EUI distribution |
| By region | Missingness rate, climate consistency, sample size |
| By country | Missingness rate, sample size, data completeness |
| By primaryspaceusage | Missingness rate, EUI plausibility, sample size |

### 7.2 Missingness by Subgroup

**Template Analysis:**

| Subgroup | n | yearbuilt Missing % | region Missing % | Assessment |
|----------|---|---------------------|------------------|------------|
| meter: electricity | TBD | TBD | TBD | TBD |
| meter: gas | TBD | TBD | TBD | TBD |
| region: [each] | TBD | TBD | N/A | TBD |
| primaryspaceusage: office | TBD | TBD | TBD | TBD |
| primaryspaceusage: retail | TBD | TBD | TBD | TBD |

**Concern Threshold:** >20% variation in missingness rate across subgroups suggests systematic data collection differences.

### 7.3 Outlier Rate by Subgroup

**Template Analysis:**

| Subgroup | n | EUI Outlier Rate | sqm Outlier Rate | Assessment |
|----------|---|------------------|------------------|------------|
| meter: electricity | TBD | TBD | TBD | TBD |
| meter: gas | TBD | TBD | TBD | TBD |

**Concern Threshold:** Subgroups with >3× the overall outlier rate require investigation.

### 7.4 Sample Size by Subgroup

**Minimum Sample Size Requirements:**

| Subgroup Level | Minimum for Clustering | Assessment |
|----------------|------------------------|------------|
| meter type | 100 observations | TBD |
| region | 50 observations | TBD |
| primaryspaceusage | 100 observations | TBD |

**Analysis:**
```python
# Sample size by subgroup
for col in ['meter', 'region', 'primaryspaceusage']:
    counts = df[col].value_counts()
    below_threshold = (counts < 50).sum()
    print(f"\n{col} - categories below 50 observations: {below_threshold}")
    print(counts)
```

### 7.5 Subgroup Quality Recommendations

| Priority | Action | Purpose |
|----------|--------|---------|
| High | Calculate missingness by meter type | Identify meter-specific data gaps |
| High | Calculate missingness by region | Identify geographic data gaps |
| Medium | Check outlier rates by subgroup | Identify measurement differences |
| Medium | Verify minimum sample sizes | Ensure stable subgroup representation |

---

## 8. Expert Validation Framework

### 8.1 Domain Expert Review Requirements

Data quality assessment benefits from domain expert validation at key decision points.

**Expert Review Checklist:**

| Area | Question for Expert | Expert Response |
|------|---------------------|-----------------|
| **EUI Ranges** | Are EUI values of [min]-[max] plausible for this building stock? | TBD |
| **Outliers** | Should buildings with EUI > 1000 kWh/m²/year be excluded as errors? | TBD |
| **Building Types** | Is the primaryspaceusage taxonomy appropriate for energy analysis? | TBD |
| **Climate Data** | Are the HDD/CDD values consistent with expected regional patterns? | TBD |
| **Missing Data** | Is 52.88% missingness for yearbuilt acceptable for clustering? | TBD |
| **Meter Types** | Should electricity and gas meters be clustered together or separately? | TBD |

### 8.2 Anomaly Review Process

**Anomalies Requiring Expert Review:**

| Anomaly Type | Identification Method | Expert Question |
|--------------|----------------------|-----------------|
| Extreme EUI | EUI < 10 or > 1000 kWh/m²/year | Data error or legitimate outlier? |
| Zero consumption | total_meter_reading = 0 | Vacant building or metering gap? |
| Very large buildings | sqm > 100,000 m² | Single building or campus aggregate? |
| Old buildings | yearbuilt < 1900 | Historical building or data error? |
| Climate inconsistency | HDD and CDD both very high | Data integration error? |

### 8.3 Expert Validation Documentation

**Template for Recording Expert Input:**

| Date | Expert Name/Role | Issue Reviewed | Decision | Rationale |
|------|------------------|----------------|----------|-----------|
| | | | | |
| | | | | |

### 8.4 Expert Validation Recommendations

| Priority | Action | Purpose |
|----------|--------|---------|
| High | Present EUI distribution to energy expert | Validate plausibility |
| High | Review outlier handling decisions | Ensure domain-appropriate treatment |
| Medium | Validate building type taxonomy | Confirm appropriateness for clustering |
| Low | Document all expert decisions | Audit trail for methodology |

---

## 9. Data Quality Summary and Action Plan

### 9.1 Quality Dimension Summary

| Dimension | Status | Key Issues | Priority Actions |
|-----------|--------|------------|------------------|
| **Completeness** | △ | 52.88% yearbuilt missing; 17% region/country missing | Investigate missingness patterns; imputation strategy |
| **Accuracy - Outliers** | △ | High outlier counts in energy/size features | Apply IQR detection; domain validation |
| **Accuracy - Implausible** | ? | Pending negative value and range checks | Execute validation checks |
| **Consistency - Logical** | ? | Pending relationship validation | Execute correlation checks |
| **Consistency - EUI** | ? | Pending EUI plausibility analysis | Calculate and validate EUI |
| **External Benchmarks** | ? | No benchmark comparison yet | Compare to CIBSE TM46 |
| **Representativeness** | ? | Sample characteristics not compared to population | Document sample distribution |
| **Subgroup Quality** | ? | Quality variation not assessed | Calculate metrics by subgroup |
| **Expert Validation** | ? | No expert review yet | Schedule expert review |

### 9.2 Critical Action Items

| Priority | Action | Section Reference | Status |
|----------|--------|-------------------|--------|
| **Critical** | Check for negative values in energy/area features | 3.1 | ☐ Pending |
| **Critical** | Calculate and validate EUI distribution | 4.2 | ☐ Pending |
| **Critical** | Investigate yearbuilt missingness mechanism | 2.2 | ☐ Pending |
| **High** | Apply IQR outlier detection | 3.2 | ☐ Pending |
| **High** | Validate expected correlations | 4.1 | ☐ Pending |
| **High** | Compare EUI to CIBSE TM46 benchmarks | 5.2 | ☐ Pending |
| **High** | Calculate missingness by subgroup | 7.2 | ☐ Pending |
| **Medium** | Document sample building type distribution | 6.3 | ☐ Pending |
| **Medium** | Schedule domain expert review | 8.1 | ☐ Pending |
| **Low** | Document data provenance | 1.1 | ☐ Pending |

### 9.3 Quality Gates for Proceeding

**Before proceeding to clustering, the following quality gates should be satisfied:**

| Gate | Requirement | Status |
|------|-------------|--------|
| No negative values | Zero negative energy/area values | ☐ |
| Outlier handling documented | Outlier identification and treatment decisions recorded | ☐ |
| EUI plausibility confirmed | Median EUI within reasonable range (50-500 kWh/m²/year) | ☐ |
| Missingness mechanism understood | yearbuilt missingness pattern documented | ☐ |
| Logical consistency verified | Expected correlations confirmed | ☐ |
| Subgroup quality acceptable | No >2× quality variation across subgroups | ☐ |

### 9.4 Data Quality Limitations Acknowledgment

**Limitations to Document in Final Analysis:**

1. **Completeness:** 52.88% of yearbuilt values missing; imputation introduces uncertainty
2. **Representativeness:** Sample selection method unknown; may not represent full building stock
3. **Measurement consistency:** Multiple meter types and data sources may have different quality standards
4. **Geographic coverage:** 17% missing region/country limits geographic analysis
5. **Temporal scope:** 2016-2017 data may not reflect current building stock

---

## 10. Appendix: Validation Code Templates

### 10.1 Comprehensive Quality Assessment Function

```python
import pandas as pd
import numpy as np

def assess_data_quality(df):
    """Comprehensive data quality assessment for building energy data."""
    
    quality_report = {}
    
    # 1. Completeness Analysis
    missing_stats = df.isnull().sum().sort_values(ascending=False)
    quality_report['missing_counts'] = missing_stats[missing_stats > 0]
    quality_report['missing_pct'] = (missing_stats / len(df) * 100).round(2)
    quality_report['complete_cases'] = df.dropna().shape[0]
    quality_report['complete_pct'] = (df.dropna().shape[0] / len(df) * 100).round(2)
    
    # 2. Numerical Summary
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    quality_report['numerical_summary'] = df[numerical_cols].describe()
    
    # 3. Negative Value Checks
    negative_checks = {}
    for col in ['total_meter_reading', 'sqm', 'Total_HDD_Annual', 'Total_CDD_Annual']:
        if col in df.columns:
            negative_checks[col] = (df[col] < 0).sum()
    quality_report['negative_values'] = negative_checks
    
    # 4. Outlier Detection (IQR Method)
    outlier_counts = {}
    for col in numerical_cols:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower_fence = Q1 - 1.5 * IQR
        upper_fence = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower_fence) | (df[col] > upper_fence)).sum()
        outlier_counts[col] = {
            'lower_fence': lower_fence,
            'upper_fence': upper_fence,
            'outlier_count': outliers,
            'outlier_pct': (outliers / df[col].notna().sum() * 100).round(2)
        }
    quality_report['outliers'] = outlier_counts
    
    # 5. EUI Calculation and Validation
    if 'total_meter_reading' in df.columns and 'sqm' in df.columns:
        df_temp = df.copy()
        df_temp['EUI'] = df_temp['total_meter_reading'] / df_temp['sqm']
        quality_report['EUI_summary'] = df_temp['EUI'].describe()
        quality_report['EUI_implausible_low'] = (df_temp['EUI'] < 10).sum()
        quality_report['EUI_implausible_high'] = (df_temp['EUI'] > 1000).sum()
    
    return quality_report


def visualize_data_quality(df):
    """Create data quality visualizations."""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Missing data heatmap
    ax1 = axes[0, 0]
    missing_pct = df.isnull().sum() / len(df) * 100
    missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=True)
    if len(missing_pct) > 0:
        missing_pct.plot(kind='barh', ax=ax1, color='coral')
        ax1.set_xlabel('Missing %')
        ax1.set_title('Missing Data by Feature')
    else:
        ax1.text(0.5, 0.5, 'No missing data', ha='center', va='center')
        ax1.set_title('Missing Data by Feature')
    
    # 2. EUI distribution
    ax2 = axes[0, 1]
    if 'total_meter_reading' in df.columns and 'sqm' in df.columns:
        EUI = df['total_meter_reading'] / df['sqm']
        EUI_clipped = EUI.clip(upper=EUI.quantile(0.99))  # Clip for visualization
        ax2.hist(EUI_clipped.dropna(), bins=50, alpha=0.7, color='steelblue')
        ax2.axvline(x=200, color='red', linestyle='--', label='Typical benchmark')
        ax2.set_xlabel('EUI (kWh/m²/year)')
        ax2.set_title('EUI Distribution (clipped at 99th percentile)')
        ax2.legend()
    
    # 3. Outlier summary
    ax3 = axes[1, 0]
    numerical_cols = df.select_dtypes(include=[np.number]).columns[:6]
    outlier_pcts = []
    for col in numerical_cols:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
        outlier_pcts.append(outliers / df[col].notna().sum() * 100)
    ax3.barh(numerical_cols, outlier_pcts, color='orange')
    ax3.set_xlabel('Outlier %')
    ax3.set_title('Outlier Rate by Feature (IQR Method)')
    
    # 4. Correlation heatmap for consistency check
    ax4 = axes[1, 1]
    corr_cols = ['sqm', 'total_meter_reading', 'Total_HDD_Annual', 'Total_CDD_Annual', 'Avg_AirTemp_Annual']
    corr_cols = [c for c in corr_cols if c in df.columns]
    if len(corr_cols) > 1:
        corr_matrix = df[corr_cols].corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax4, center=0)
        ax4.set_title('Feature Correlations (Consistency Check)')
    
    plt.tight_layout()
    plt.savefig('data_quality_visualization.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    return fig


def check_logical_consistency(df):
    """Check for logical inconsistencies in building energy data."""
    
    issues = []
    
    # 1. Negative values where not allowed
    for col in ['total_meter_reading', 'sqm', 'Total_HDD_Annual', 'Total_CDD_Annual']:
        if col in df.columns:
            negatives = (df[col] < 0).sum()
            if negatives > 0:
                issues.append(f"CRITICAL: {col} has {negatives} negative values")
    
    # 2. Yearbuilt range
    if 'yearbuilt' in df.columns:
        out_of_range = ((df['yearbuilt'] < 1800) | (df['yearbuilt'] > 2025)).sum()
        if out_of_range > 0:
            issues.append(f"WARNING: yearbuilt has {out_of_range} values outside 1800-2025")
    
    # 3. EUI plausibility
    if 'total_meter_reading' in df.columns and 'sqm' in df.columns:
        EUI = df['total_meter_reading'] / df['sqm']
        implausible_low = (EUI < 10).sum()
        implausible_high = (EUI > 1000).sum()
        if implausible_low > 0:
            issues.append(f"WARNING: {implausible_low} buildings with EUI < 10 kWh/m²/year")
        if implausible_high > 0:
            issues.append(f"WARNING: {implausible_high} buildings with EUI > 1000 kWh/m²/year")
    
    # 4. Expected correlations
    expected_negative = [('Total_HDD_Annual', 'Total_CDD_Annual')]
    expected_positive = [('sqm', 'total_meter_reading'), 
                        ('Total_HDD_Annual', 'Count_Heating_Days_Annual'),
                        ('Total_CDD_Annual', 'Count_Cooling_Days_Annual')]
    
    for var1, var2 in expected_negative:
        if var1 in df.columns and var2 in df.columns:
            corr = df[[var1, var2]].corr().iloc[0, 1]
            if corr > 0:
                issues.append(f"INCONSISTENT: {var1} ↔ {var2} should be negative, got r={corr:.3f}")
    
    for var1, var2 in expected_positive:
        if var1 in df.columns and var2 in df.columns:
            corr = df[[var1, var2]].corr().iloc[0, 1]
            if corr < 0:
                issues.append(f"INCONSISTENT: {var1} ↔ {var2} should be positive, got r={corr:.3f}")
    
    # 5. Duplicate building IDs
    if 'building_id' in df.columns:
        duplicates = df['building_id'].duplicated().sum()
        if duplicates > 0:
            issues.append(f"WARNING: {duplicates} duplicate building_id values")
    
    return issues


def subgroup_quality_analysis(df, subgroup_col):
    """Analyze data quality metrics by subgroup."""
    
    results = []
    
    for group_name, group_df in df.groupby(subgroup_col):
        metrics = {
            'subgroup': group_name,
            'n': len(group_df),
            'pct_of_total': len(group_df) / len(df) * 100
        }
        
        # Missingness rates
        for col in ['yearbuilt', 'region', 'country']:
            if col in df.columns:
                metrics[f'{col}_missing_pct'] = group_df[col].isnull().mean() * 100
        
        # Outlier rate for EUI
        if 'total_meter_reading' in df.columns and 'sqm' in df.columns:
            EUI = group_df['total_meter_reading'] / group_df['sqm']
            Q1, Q3 = EUI.quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outliers = ((EUI < Q1 - 1.5*IQR) | (EUI > Q3 + 1.5*IQR)).sum()
            metrics['EUI_outlier_pct'] = outliers / EUI.notna().sum() * 100
        
        results.append(metrics)
    
    return pd.DataFrame(results)
```

### 10.2 Usage Example

```python
# Load data
df = pd.read_csv('data/df_analysis.csv')

# Run comprehensive quality assessment
quality_report = assess_data_quality(df)

# Print key findings
print("=== DATA QUALITY REPORT ===\n")
print(f"Complete cases: {quality_report['complete_cases']} ({quality_report['complete_pct']}%)")
print(f"\nMissing data:\n{quality_report['missing_pct']}")
print(f"\nNegative value checks:\n{quality_report['negative_values']}")
print(f"\nEUI Summary:\n{quality_report['EUI_summary']}")
print(f"Implausibly low EUI (<10): {quality_report['EUI_implausible_low']}")
print(f"Implausibly high EUI (>1000): {quality_report['EUI_implausible_high']}")

# Check logical consistency
issues = check_logical_consistency(df)
print("\n=== CONSISTENCY ISSUES ===")
for issue in issues:
    print(f"  - {issue}")

# Subgroup quality analysis
print("\n=== QUALITY BY METER TYPE ===")
subgroup_quality = subgroup_quality_analysis(df, 'meter')
print(subgroup_quality.to_string(index=False))

# Create visualizations
visualize_data_quality(df)
```

---

*Report template created: 2026-01-05*
*Analysis pending execution of validation code*
