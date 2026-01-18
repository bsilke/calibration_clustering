# Data-Method Alignment: Building Energy Benchmarking

## 1. Feature Categorization by Data Type

The dataset contains ~5,900 observations of non-residential buildings with the following features:

| Feature | Data Type | Category | Role in Clustering |
|---------|-----------|----------|-------------------|
| `Avg_AirTemp_Annual` | Continuous numerical | Climate | ✅ Clustering feature |
| `year` | Discrete numerical | Temporal identifier | ❌ Stratification variable |
| `meter` | Categorical (nominal) | Meter type | ⚠️ Potential filter/stratifier |
| `site_id` | Categorical (nominal) | Building identifier | ❌ Identifier only |
| `region` | Categorical (nominal) | Geography | ✅ Clustering feature |
| `country` | Categorical (nominal) | Geography | ⚠️ Low variance (mostly USA) |
| `yearbuilt` | Discrete numerical | Structural | ✅ Clustering feature |
| `primaryspaceusage` | Categorical (nominal) | Operational | ✅ Clustering feature |
| `total_meter_reading` | Continuous numerical | Energy consumption | ❌ Used to derive EUI |
| `eui` | Continuous numerical | Energy intensity | ❌ Outcome variable (not for clustering) |
| `log_eui` | Continuous numerical | Transformed outcome | ❌ Outcome variable (not for clustering) |

---

## 2. Dominant Data Characteristics

### Primary Characteristic: Mixed Data Types

The clustering features span both numerical and categorical types:

- **Numerical features (2):** `Avg_AirTemp_Annual`, `yearbuilt`
- **Categorical features (2–3):** `primaryspaceusage`, `region`, potentially `meter`

This mixed-type structure is the dominant characteristic driving algorithm selection.

### Secondary Characteristics

| Characteristic | Present? | Implications |
|----------------|----------|--------------|
| **High dimensionality** | No | Only 4–5 clustering features; no dimensionality reduction needed |
| **Spatial structure** | Partial | `region` captures geography at coarse level, but no coordinates for spatial clustering |
| **Temporal sequences** | No | Annual aggregates only; no intra-year time series |
| **Network relationships** | No | Buildings are independent entities |

---

## 3. Appropriate Clustering Approaches

Based on the data-method alignment matrix, the following approaches are suitable:

### Recommended: Mixed Data Methods

| Approach | Suitability | Rationale |
|----------|-------------|-----------|
| **K-Prototypes** | ✅ Excellent | Purpose-built for mixed numerical/categorical data; extends K-Means with categorical handling via Huang (1997) |
| **Gower distance + hierarchical** | ⚠️ Moderate | Gower distance handles mixed types, but hierarchical clustering scales poorly (~5,900² distance matrix) |
| **Two-step clustering** | ⚠️ Moderate | Pre-clusters then hierarchical; handles mixed data but adds complexity |

### Alternative: Encoding-Based Methods

| Approach | Suitability | Rationale |
|----------|-------------|-----------|
| **One-hot encoding + K-Means** | ⚠️ Moderate | Converts categoricals to binary; inflates dimensionality and treats all category distances as equal |
| **One-hot encoding + GMM** | ⚠️ Moderate | Provides soft assignments but same encoding limitations |

### Not Recommended for Primary Analysis

| Approach | Suitability | Rationale |
|----------|-------------|-----------|
| **DBSCAN/HDBSCAN** | ❌ Primary, ✅ Secondary | Density-based methods less suited for mixed data; useful for outlier detection post-clustering |
| **Time series clustering (DTW)** | ❌ Not applicable | No temporal sequences in current dataset |
| **Spatial clustering** | ❌ Not applicable | No coordinate data; `region` is categorical |

### Selected Approach

**K-Prototypes** is selected as the primary clustering method based on:

1. Native support for mixed categorical and numerical features
2. Efficient scaling to ~5,900 observations
3. Established use in building stock modelling literature (Alrasheed & Mourshed, 2024)
4. Interpretable cluster centroids (mode for categorical, mean for numerical)

---

## 4. Preprocessing Challenges

### Numerical Features

| Challenge | Feature(s) | Mitigation Strategy |
|-----------|------------|---------------------|
| **Scale differences** | `Avg_AirTemp_Annual` (°C, ~0–30), `yearbuilt` (years, ~1900–2020) | Standardize (z-score) numerical features before clustering |
| **Outliers** | `yearbuilt` may have erroneous values (e.g., future years, implausibly old) | Validate range; cap or exclude extreme values |
| **Skewness** | `yearbuilt` distribution likely right-skewed toward recent construction | Consider binning into building age eras (see below) |

### Option: Binning `yearbuilt` into Building Age Eras

Converting `yearbuilt` from a continuous variable to categorical building eras is a preprocessing option with trade-offs:

**Arguments for binning:**
- Improves interpretability—building eras are more meaningful to stakeholders than exact years
- Aligns with policy-relevant periods (energy code introductions, construction booms)
- Reduces noise—adjacent years (e.g., 1983 vs. 1984) are not meaningfully different for energy benchmarking
- Handles date outliers by placing erroneous values in boundary bins

**Arguments against binning:**
- K-Prototypes handles continuous `yearbuilt` natively; binning discards granularity
- Bin boundaries are subjective choices
- Changes distance logic from continuous to mode-based matching

**Suggested era bins (if binning is applied):**

| Era | Years | Rationale |
|-----|-------|-----------|
| Pre-war | < 1945 | Older construction methods, no energy standards |
| Post-war boom | 1945–1969 | Rapid expansion, minimal insulation requirements |
| Early energy codes | 1970–1989 | Post-oil crisis awareness, first ASHRAE standards |
| Modern codes | 1990–2009 | Strengthened efficiency requirements |
| Recent high-efficiency | ≥ 2010 | Contemporary green building standards |

**Recommendation:** Run clustering both ways (continuous vs. binned) and compare cluster interpretability and stability. If results are similar, prefer binned for stakeholder communication; if continuous yields better separation, retain granularity.

### Categorical Features

| Challenge | Feature(s) | Mitigation Strategy |
|-----------|------------|---------------------|
| **High cardinality** | `region` may have many unique values | Consider grouping into climate zones or broader geographic regions |
| **Imbalanced categories** | `primaryspaceusage` may have rare categories | Merge rare usage types or handle as "Other" |
| **Gamma parameter tuning** | K-Prototypes requires balancing numerical vs. categorical weight | Use Huang's rule of thumb (γ = 0.5 × average std of numerical features) or tune via silhouette score |

### Feature Redundancy: Region vs. Climate Overlap

The features `region` and `Avg_AirTemp_Annual` partially encode the same underlying information—geographic location influences climate. Including both may overweight geography in distance calculations, causing the clustering algorithm to emphasize location-related factors more than intended.

**Potential issues:**
- Double-counting geographic signal inflates its influence on cluster formation
- May mask the contribution of other features (e.g., `primaryspaceusage`, `yearbuilt`)
- Clusters could become geography-dominated rather than balanced peer groups

**Justification for retaining both:**
- `region` captures non-climate geographic factors (local building codes, energy prices, grid carbon intensity)
- `Avg_AirTemp_Annual` captures climate-driven energy demand (heating/cooling loads)
- Together, they provide complementary information that neither captures alone

**Recommended ablation study:**

| Scenario | Features Included | Purpose |
|----------|-------------------|---------|
| **Full model** | All features including both `region` and `Avg_AirTemp_Annual` | Baseline clustering |
| **Climate only** | Replace `region` with `Avg_AirTemp_Annual` only | Test if region adds value beyond climate |
| **Region only** | Replace `Avg_AirTemp_Annual` with `region` only | Test if climate adds value beyond region |

Compare cluster solutions across scenarios using:
- Silhouette score (cluster separation quality)
- Within-cluster EUI variance (homogeneity of outcome variable)
- Cluster interpretability (do profiles make domain sense?)

If results are similar across scenarios, the simpler model (fewer features) is preferred. If results differ substantially, retain both features with documented justification.

### Data Quality

| Challenge | Mitigation Strategy |
|-----------|---------------------|
| Missing values | Assess missingness patterns; impute or exclude as appropriate |
| Duplicate building-year combinations | Decide whether to cluster at building level (aggregate years) or observation level |
| Year as stratification variable | Consider running separate clustering for 2016 and 2017, or pooling with year as a covariate |

---

## 5. Cluster Interpretation Strategy

Given the mixed data characteristics, cluster interpretation will proceed as follows:

### Centroid Characterization

For each cluster, report:

- **Numerical features:** Mean and standard deviation of `Avg_AirTemp_Annual` and `yearbuilt`
- **Categorical features:** Mode (most frequent category) and distribution of `primaryspaceusage` and `region`

### Cluster Profiles

Translate centroids into human-readable peer group descriptions:

| Example Cluster | Profile Description |
|-----------------|---------------------|
| Cluster 1 | "Modern office buildings in temperate climates" (mean yearbuilt ~2000, mode usage = Office, mean temp ~15°C) |
| Cluster 2 | "Older educational facilities in cold regions" (mean yearbuilt ~1960, mode usage = Education, mean temp ~8°C) |
| Cluster 3 | "Retail buildings in warm climates" (mean yearbuilt ~1985, mode usage = Retail, mean temp ~22°C) |

### Outcome Variable Analysis

After clustering, analyze `eui` (Energy Use Intensity) within each cluster:

- Report cluster-specific EUI distributions (median, IQR, range)
- Identify efficiency outliers as buildings exceeding cluster median + 1 SD
- Validate that within-cluster EUI variance is lower than full-dataset variance (success criterion: ≥30% reduction)

### Visualization Approach

| Visualization | Purpose |
|---------------|---------|
| Parallel coordinates plot | Show feature profiles across clusters |
| Boxplots of EUI by cluster | Compare energy performance distributions |
| Heatmap of categorical distributions | Show usage type and region composition per cluster |
| t-SNE or UMAP projection | Visualize cluster separation in 2D (post-hoc validation) |

---

## 6. Summary: Data-Method Alignment Rationale

| Consideration | Assessment |
|---------------|------------|
| **Dominant data type** | Mixed (numerical + categorical) |
| **Primary algorithm** | K-Prototypes |
| **Key preprocessing** | Standardize numericals; consolidate high-cardinality categoricals; tune gamma |
| **Interpretation approach** | Centroid-based profiles with categorical mode and numerical mean |
| **Validation strategy** | Within-cluster EUI variance reduction; silhouette score; cluster stability |

The mixed-type nature of the building dataset—combining structural characteristics (`yearbuilt`), operational profiles (`primaryspaceusage`), and climatic context (`Avg_AirTemp_Annual`, `region`)—directly motivates the selection of K-Prototypes over pure numerical methods. This alignment ensures that categorical distinctions (e.g., office vs. retail) are preserved as meaningful grouping factors rather than artificially encoded as distances.
