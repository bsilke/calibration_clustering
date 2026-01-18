# Building Energy Peer Group Analysis

A clustering-based approach for creating fair building peer groups for energy benchmarking, using K-Prototypes clustering validated by hierarchical methods.

## Overview

Energy benchmarking programs compare building energy performance, but *fair* comparisons require comparing similar buildings. A parking garage shouldn't be compared to a laboratory, and a building in Arizona shouldn't be compared to one in Wales without accounting for climate differences.

This project uses **K-Prototypes clustering**—an algorithm that handles both categorical and numerical data simultaneously—to create meaningful building peer groups based on characteristics, then analyzes energy performance *within* each peer group.

## Key Results

| Metric | Value |
|--------|-------|
| **Buildings Analyzed** | 4,946 |
| **Peer Groups Identified** | 3 |
| **Hopkins Statistic** | 0.948 (strong clustering tendency) |
| **Silhouette Score** | 0.34 (moderate separation) |
| **Algorithm Agreement (ARI)** | 0.51 (moderate consensus) |
| **Underperformers Identified** | 912 (18.4%) |

### Peer Group Summary

| Peer Group | Buildings | Avg Temperature | Median EUI |
|------------|-----------|-----------------|------------|
| Warm-Climate Educational | 1,611 (33%) | 22–23°C | 183 kWh/m²/yr |
| Cold-Climate Educational | 2,119 (43%) | 11–12°C | 115 kWh/m²/yr |
| Temperate-Climate Educational | 1,216 (25%) | 14–15°C | 122 kWh/m²/yr |

## Key Features

- **Mixed Data Type Clustering**: Handles both categorical (building type, region, meter type) and numerical (year built, climate, building size) features
- **Fair Benchmarking**: Creates peer groups based on building characteristics, excluding energy use intensity (EUI) from clustering
- **Efficiency Classification**: Identifies top performers, average performers, and underperformers within each peer group using z-scores
- **Cross-Validation**: K-Prototypes results validated against hierarchical clustering with Gower distance
- **Publication-Ready Visualizations**: Colorblind-safe figures with detailed captions for policymakers

## Project Structure

```
calibration_clustering/
├── README.md                            # This file
├── impact_brief.md                      # Executive summary for stakeholders
├── problem_framing.md                   # Problem definition and methodology
├── ETHICS_FRAMEWORK.md                  # Ethical considerations
├── data/
│   ├── df_analysis.csv                  # Input: building energy data
│   ├── df_complete.csv                  # Input: complete dataset
│   ├── metadata_analysis.csv            # Input: building metadata with size (sqm)
│   ├── quality_metrics.csv              # Data quality assessment
│   └── df_analysis_with_clusters.csv    # Output: clustered building data
├── jupyter_notebooks/
│   ├── clustering.ipynb                 # Main analysis notebook
│   ├── data_quality_assessment.ipynb    # Data quality checks
│   ├── data_adequacy_assessment.ipynb   # Clustering adequacy assessment (Hopkins, sample size)
│   └── algorithm_decision_tree.ipynb    # Algorithm selection rationale
└── figures/
    ├── fig7_enhanced_pca_tsne.png       # Peer group visualization
    ├── fig8_radar_cluster_profiles.png  # Cluster profile comparison
    ├── fig9_parallel_coordinates.png    # How buildings compare across all features
    ├── fig10_statistical_heatmap.png    # Z-scores with significance
    └── fig11_executive_summary.png      # One-page summary for policymakers
```

## Methodology

### Clustering Features vs. Analysis Features

| Feature Type | Variables | Purpose |
|--------------|-----------|---------|
| **Clustering Features** | `primaryspaceusage`, `region`, `meter`, `yearbuilt`, `Avg_AirTemp_Annual`, `log_sqm` | Used to form peer groups |
| **Analysis Features** | `log_eui` | Analyzed *within* peer groups (NOT used for clustering) |

### Why Exclude EUI from Clustering?

By excluding EUI from the clustering process, we:
1. Create peer groups based on building characteristics only
2. Enable fair benchmarking by comparing buildings to true peers
3. Identify efficiency outliers relative to similar buildings
4. Analyze energy intensity variation *within* each peer group

### Variable Definitions

| Variable | Description | Type | Units/Values |
|----------|-------------|------|--------------|
| `primaryspaceusage` | Primary function of the building | Categorical | Education, Office, Parking, etc. |
| `region` | Geographic location of the building | Categorical | City/region names |
| `meter` | Type of energy meter | Categorical | electricity, chilledwater, gas, etc. |
| `yearbuilt` | Year the building was constructed | Numerical | Year (e.g., 1975) |
| `Avg_AirTemp_Annual` | Average annual air temperature at location | Numerical | °C |
| `sqm` | Building floor area (from metadata) | Numerical | m² |
| `log_sqm` | Log-transformed building floor area | Numerical | log(m²) |
| `log_eui` | Log-transformed Energy Use Intensity | Numerical | log(kWh/m²/year) |
| `Cluster` | Assigned peer group from K-Prototypes | Numerical | 0, 1, 2, ... |
| `efficiency_status` | Performance relative to cluster peers | Categorical | Top Performer, Average, Underperformer |
| `eui_zscore` | Z-score of EUI within cluster | Numerical | Standard deviations from cluster mean |

## Installation

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab

### Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn kmodes
```

Or install kmodes specifically if other packages are already available:

```bash
pip install kmodes
```

## Usage

1. **Open the main analysis notebook**:
   ```bash
   jupyter notebook jupyter_notebooks/clustering.ipynb
   ```

2. **Run the analysis**:
   - The notebook includes data loading, preprocessing, clustering validation, model fitting, and publication-ready visualizations
   - Section 12 generates enhanced figures for the impact report (Figures 7–11)

3. **Outputs**:
   - Clustered data: `data/df_analysis_with_clusters.csv`
   - Figures: `figures/fig7_enhanced_pca_tsne.png`, `fig10_statistical_heatmap.png`, `fig11_executive_summary.png`, etc.

4. **Supporting notebooks**:
   - `data_quality_assessment.ipynb` — Data quality checks and validation
   - `algorithm_decision_tree.ipynb` — Algorithm selection rationale

## Key Findings

### Peer Groups Identified

The K-Prototypes algorithm identifies three distinct peer groups primarily differentiated by:
- **Climate** (average annual air temperature) — the dominant factor (η² = 0.45)
- **Building type** (primary space usage)
- **Building size** (floor area in m²)

### Key Finding: Climate is the Primary Driver

Temperature difference across cluster centroids exceeds 10°C, confirming that climate should be the primary stratification factor in any building benchmarking system.

### EUI Analysis Within Peer Groups

- **Warm-Climate** buildings show highest median EUI (183 kWh/m²/yr) due to cooling loads
- **Cold-Climate** buildings show lowest median EUI (115 kWh/m²/yr) despite heating needs
- **18.4% of buildings** are underperformers (>1 standard deviation above peer median)

### Practical Applications

| Application | Description |
|-------------|-------------|
| **Peer-Group Benchmarking** | Compare buildings within climate-appropriate peer groups |
| **Retrofit Prioritization** | Focus on the 912 identified underperformers |
| **Policy Development** | Support climate-specific efficiency standards |
| **Green Finance** | Use peer-relative metrics for sustainability assessments |

## Data Source

- **Dataset**: BDG2 (Building Data Genome Project 2) — Miller et al., 2020
- **Buildings**: 4,946 non-residential buildings (primarily educational) across multiple climate zones
- **Time Period**: 2016–2017 annual energy data
- **Geographic Coverage**: 80.8% US buildings; remainder from other regions

## Limitations

- **Temporal scope**: 2016–2017 data may not reflect current building stock
- **Geographic bias**: Primarily US buildings; European patterns may differ
- **Missing data**: 52.9% missing year-built data (imputation applied)
- **Cross-method agreement**: ARI = 0.51 indicates moderate (not strong) consensus

## Documentation

- [**Impact Brief**](impact_brief.md) — Executive summary with recommendations for policymakers, building owners, and researchers
- [**Problem Framing**](problem_framing.md) — Detailed problem statement and methodology
- [**Ethics Framework**](ETHICS_FRAMEWORK.md) — Fairness, privacy, and appropriate use considerations

## References

- Miller, C., et al. (2020). The Building Data Genome Project 2. *Scientific Data*, 7, 368. https://doi.org/10.1038/s41597-020-00712-x
- Alrasheed, M., & Mourshed, M. (2024). Building stock modelling using k-prototype algorithm. *Energy and Buildings*, 311, 114111.

## License

This project is for research and educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

*Last updated: 18 January 2026*