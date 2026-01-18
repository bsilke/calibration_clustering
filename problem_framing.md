# Problem Framing
#problemstatement #clustering #climatechange

1\. Introduction: The Central Role of the Built Environment

The building and construction sector is a primary driver of the global climate crisis, accounting for approximately **34% of global energy-related CO₂ emissions** and **32% of global final energy consumption** (UN Environment Programme [UNEP], 2025). In 2024, sector emissions reached a record peak of nearly **ten gigatonnes**, driven largely by extreme temperatures that triggered a massive surge in energy demand for space cooling (International Energy Agency [IEA], 2025; UNEP, 2025). As the global building stock is projected to double by 2050, the "physical environment"---the human-made structures in which we live and work---represents a critical frontier for climate mitigation (UNEP, 2025). Effective decarbonization therefore requires a precise understanding of how structural characteristics and local climatic conditions influence these energy patterns (Alrasheed & Mourshed, 2024).

Since the majority of building-sector emissions stem from operational energy consumption—primarily electricity and natural gas for heating, cooling, and lighting—improving energy efficiency represents the a highly relevant lever for emissions reduction. This analysis therefore focuses on **Energy Use Intensity (EUI)** as the primary metric, recognizing it as both a direct measure of energy consumption and a proxy for carbon intensity.

**Problem Statement:** Segment commercial buildings by structural characteristics, usage type, and climatic context to develop a data-driven prioritization matrix for identifying and profiling efficiency outliers, thereby optimizing investment in high-impact retrofit interventions.

> **🎯 Clustering Objective**
> 
> - **Who:** Commercial buildings across diverse usage types and climate zones
> - **What:** Energy-relevant peer groups based on structural, operational, and climatic similarity
> - **Why:** Enable fair benchmarking of Energy Use Intensity (EUI; kWh/sqm/year) and identify efficiency outliers for targeted retrofit prioritization

> **📋 SMART Criteria**
> 
> - **Specific:** Segment non-residential buildings across various usage types (e.g., office, retail, industrial) and climate zones using structural, operational, and climatic features.
> - **Measurable:** Discover 3–6 peer groups with distinct Energy Use Intensity profiles, characterized by within-cluster variance reduction of at least 30% compared to the full dataset.
> - **Achievable:** Data quality has been assessed and cleaning pipelines established; read literature about mixed-type clustering methods (K-Prototypes).
> - **Relevant:** Directly informs policymakers and asset owners by enabling fair benchmarking and supporting the development of evidence-based energy efficiency standards.
> - **Time-bound:** Analysis to be completed and cluster profiles to be delivered within one month (clustering challenge time frame)

2\. Stakeholders

The following stakeholders can benefit from or be affected by the outcomes of this analysis:

- **Policymakers and regulators:** Responsible for setting energy performance standards, allocating retrofit subsidies, and enforcing emission reduction targets.
- **Building owners and asset managers:** Require accurate benchmarks to assess portfolio performance and identify underperforming physical assets.
- **Facility managers:** Use peer comparisons to set operational improvement targets and justify capital expenditure requests.
- **Energy auditors and consultants:** Benefit from data-driven prioritization when recommending retrofit measures.
- **Financial institutions:** Utilize energy performance benchmarks for green bond eligibility, sustainability-linked loan conditions, and climate risk assessments.
- **Tenants and occupants:** Indirectly benefit from improved building efficiency through reduced operating costs and healthier indoor environments.

3\. Dataset Justification

The analysis uses the **Building Data Genome Project 2 (BDG2)**, an open dataset published in *Nature Scientific Data* (Miller et al., 2020). The following aspects justify its selection for this clustering study:

| Aspect | Assessment | Evidence |
|--------|------------|----------|
| **Credibility** | ✓ Strong | Peer-reviewed publication in *Nature Scientific Data*; developed by researchers at National University of Singapore, University College Dublin, and Princeton University; DOI-registered on Zenodo |
| **Representativeness** | ✓ Adequate | 3,053 meters across 1,636 non-residential buildings from 19 sites in North America and Europe; diverse climate zones and building types |
| **Ethical/Privacy** | ✓ Low risk | Aggregated building-level data with no individual tenant or occupant information; anonymized site identifiers |
| **Beneficiary Relevance** | ✓ Direct | Directly supports building owners seeking benchmarking, policymakers targeting retrofit investments, and financial institutions assessing climate risk |
| **Temporal Scope** | △ Noted | 2016–2017 data (~9 years old at time of analysis); building efficiency standards and occupancy patterns may have evolved |
| **Geographic Balance** | △ Noted | 80.8% US buildings; European buildings may exhibit different patterns due to regulatory differences |

**Citation:**
> Miller, C., Kathirgamanathan, A., Picchetti, B. et al. The Building Data Genome Project 2, energy meter data from the ASHRAE Great Energy Predictor III competition. *Sci Data* 7, 368 (2020). https://doi.org/10.1038/s41597-020-00712-x

**Data Aggregation:** The original BDG2 dataset contains hourly meter readings (~17,544 measurements per meter). For this analysis, data has been aggregated to annual totals to align with the industry-standard EUI metric (kWh/m²/year) and climate variables (HDD, CDD).

*For detailed ethical considerations, see [ETHICS_FRAMEWORK.md](ETHICS_FRAMEWORK.md). For beneficiary analysis, see [BENEFICIARY_IMPACT.md](BENEFICIARY_IMPACT.md).*

4\. Dataset Profiling Summary

Comprehensive data profiling was conducted in two dedicated notebooks to assess data quality and clustering adequacy. The key findings are summarized below:

**Quality Checks Performed** *(Source: [data_quality_assessment.ipynb](jupyter_notebooks/data_quality_assessment.ipynb))*

| Check | Finding | Clustering Impact |
|-------|---------|-------------------|
| **Missing Values** | `yearbuilt`: 52.9% missing; `region`: 17.0% missing | Imputation required; mode imputation for yearbuilt, proxy assignment for region |
| **Distribution Analysis** | `total_meter_reading`: skewness=16.50, kurtosis=371; `sqm`: skewness=2.74 | Log transformation applied to reduce outlier influence on distance calculations |
| **Correlation Analysis** | Climate variables highly correlated (HDD-CDD r=-0.68; first PC explains 88.6% variance) | Only `Avg_AirTemp_Annual` used for clustering to avoid multicollinearity |
| **Outlier Detection** | 14.6% outliers in `total_meter_reading`; 5.7% in `sqm` (IQR method) | Conservative EUI caps applied (500 kWh/m²/year) for savings calculations |
| **Logical Consistency** | HDD-CDD negative correlation confirmed; no negative meter readings; yearbuilt ≤ measurement year | Data passes physical plausibility checks |

**Adequacy Checks Performed** *(Source: [data_adequacy_assessment.ipynb](jupyter_notebooks/data_adequacy_assessment.ipynb))*

| Check | Finding | Clustering Impact |
|-------|---------|-------------------|
| **Coefficient of Variation** | `year` (CV=0.02%) and `yearbuilt` (CV=1.52%) show low variance | Limited discriminatory power; `year` excluded from features |
| **Hopkins Statistic** | H=0.9677 | Strong clustering tendency—data exhibits non-random structure suitable for clustering |
| **Sample Size Adequacy** | n=5,902 (4,946 after cleaning) | Sufficient for k=3–6 clusters with ~800–1,600 buildings per cluster |
| **Dimensionality** | 6 clustering features (3 numerical, 3 categorical) | Manageable dimensionality; no reduction required |

**Visualizations Supporting Profiling:**
- Distribution histograms with KDE overlays
- Box plots with IQR-based outlier highlighting
- Correlation heatmaps for numerical features
- Q-Q plots for normality assessment
- Log transformation before/after comparisons
- CV bar charts by feature

*For complete analysis, see [data_quality_assessment.ipynb](jupyter_notebooks/data_quality_assessment.ipynb), [data_adequacy_assessment.ipynb](jupyter_notebooks/data_adequacy_assessment.ipynb), [DATA_QUALITY_REPORT.md](DATA_QUALITY_REPORT.md), and [data_adequacy_assessment.md](data_adequacy_assessment.md).*

5\. The Problem of "Fair" Benchmarking

For energy benchmarking to serve as a reliable instrument for emission reduction, it must enable "fair" comparisons between similar assets. Traditionally, benchmarking has relied on simple categories or **multiple linear regression (MLR)**, where buildings are often compared without accounting for essential structural or climatic differences (Ciulla & D'Amico, 2019). However, it is impractical to compare an energy-intensive laboratory to a parking garage, or a facility in a tropical climate to one in a temperate region, without considering these physical variables. Previous studies demonstrate that traditional approaches (e.g., grouping buildings by usage) frequently fail to capture the complex, non-linear relationships inherent in mixed building datasets (Amasyali & El-Gohary, 2018).

6\. Research Methodology: Advanced Clustering

This study addresses these deficits by going beyond static categorizations toward an **unsupervised clustering approach**. Unlike traditional methods, clustering allows "true" peer groups to emerge naturally from the data without the bias of predefined labels (Amasyali & El-Gohary, 2018). The study employs the **K-Prototypes algorithm** (Huang, 1997) as the main clustering algorithm, which is particularly suited for the building sector as it can simultaneously process categorical features (e.g., usage type, region) and numerical features (e.g., age, area, temperature) (Alrasheed & Mourshed, 2024). In addition to K-Prototypes, hierarchical clustering with Gower distance to validate the peer group structure is applied. Running two fundamentally different algorithms on the same data provides a "sanity check"—if both methods identify similar groupings, the peer groups likely reflect genuine patterns rather than algorithmic artifacts. The dendrogram visualization also offers transparency by showing exactly how buildings relate to one another,

7\. Research Hypotheses

The following hypotheses will guide the clustering analysis and provide testable predictions against which results can be evaluated:

> **H1: Climate-Driven Peer Groups**
>
> Buildings will cluster primarily by climate zone (measured by average annual temperature). Heating and cooling represent major energy end-uses, and climate determines baseline energy requirements regardless of building type.
>
> *Testable Prediction:* Clusters will show >5°C mean temperature difference between warm-climate groups (e.g., Austin, Orlando, Tempe) and cold-climate groups (e.g., Minneapolis, Ithaca, Cardiff).

> **H2: Building Type and Size as Differentiating Features**
>
> Building type and size will contribute to peer group formation beyond climate alone. Clusters with similar climate profiles will still differentiate based on primary space usage and building size.
>
> *Testable Prediction:* Educational buildings will form distinct peer groups separate from office buildings, even when located in similar climate zones.

> **H3: Meter Type Differentiation**
>
> Buildings with different primary energy sources (electricity vs. gas vs. district systems) will exhibit different consumption patterns, warranting separate peer groups for fair benchmarking.
>
> *Testable Prediction:* Electricity-only buildings will cluster separately from those with multiple fuel sources.

These hypotheses are evaluated in the analysis notebook (Section 9: Hypothesis Evaluation) using statistical tests including ANOVA for continuous variables and chi-square tests for categorical associations.

**Generalizability of Findings**

These clustering patterns can have broader implications beyond the BDG2 dataset. Climate-driven peer groups (H1) would suggest that any building benchmarking system—whether national energy rating schemes, green building certifications, or portfolio-level ESG assessments—should stratify by climate zone before comparing performance. This principle could inform policy design across jurisdictions: for example, the EU Energy Performance of Buildings Directive could adopt climate-adjusted benchmarks rather than uniform targets. Similarly, if building type emerges as a secondary differentiator (H2), industry-specific efficiency standards (e.g., separate targets for hospitals vs. offices) gain empirical support. The methodology itself—K-Prototypes clustering with hierarchical validation—is transferable to other building stock datasets (e.g., CBECS in the US, NEED in the UK, or proprietary portfolios held by REITs and institutional investors), enabling consistent peer group discovery across different geographies and time periods.

8\. Impact and Objectives

By grouping buildings based on these multidimensional features, the research analyzes **Energy Use Intensity (kWh/sqm/year)** within each specific peer group. This methodology ensures that benchmarking is conducted against the most relevant comparison objects rather than a vague industry average. Ultimately, this approach identifies "efficiency outliers"---buildings that perform significantly worse than similar structures---enabling policymakers to prioritize targeted interventions for the most problematic energy consumers (Deepki, 2023; UNEP, 2025).

**Impact Mechanism:** The resulting peer groups enable stakeholders to identify underperforming buildings, direct retrofitting investments and ultimately reduce emissions across the sector by focusing resources on high-impact targets. The sequence of steps  is as follows: 1) clustering produces homogeneous peer groups, 2) within-group benchmarking reveals efficiency outliers, 3) outlier identification informs resource allocation, and 4) targeted interventions yield measurable emission reductions.

**Actionable Outputs:** The analysis will produce the following decision-support artifacts:

- Prioritization lists for energy audits, ranking buildings by deviation from peer-group benchmarks.
- Eligibility criteria for retrofit subsidies, based on cluster membership and efficiency gap magnitude.
- Risk scoring frameworks for green bond portfolios and sustainability-linked financing.
- Cluster profile summaries describing the structural and climatic characteristics of each peer group.

9\. Success Criteria

The quality and utility of the clustering solution will be evaluated against the following criteria:

- **Within-cluster homogeneity:** Energy Use Intensity variance within clusters should be substantially lower than variance across the full dataset.
- **Interpretability:** Cluster profiles should be explainable in terms of meaningful building characteristics (e.g., usage type, age, climate zone).
- **Actionability:** The resulting peer groups should enable clear differentiation between high-performing and underperforming buildings.
- **Stability:** Cluster assignments should remain consistent across reasonable variations in algorithm parameters and data subsets.

10\. Algorithm Selection Rationale

The choice of clustering algorithm depends on assumptions about cluster geometry, assignment certainty, and data characteristics. Four paradigms were evaluated:

**Density-Based Methods (e.g., DBSCAN, HDBSCAN)**

Density-based approaches excel at discovering arbitrarily shaped clusters and identifying outliers as noise points. However, building peer groups are conceptually compact groupings—structures with similar age, usage type, climate zone, and operational characteristics cluster tightly in feature space rather than forming elongated or irregular shapes. Density-based methods are therefore not recommended as the primary approach but may serve a secondary role in **outlier detection**, flagging buildings that do not fit cleanly into any peer group for manual review.

**Model-Based Methods (e.g., Gaussian Mixture Models)**

Model-based clustering provides soft assignments with membership probabilities, which could accommodate buildings on peer group boundaries (e.g., mixed-use facilities, buildings in climate transition zones). However, policy applications—such as subsidy eligibility and regulatory compliance—typically require hard assignments with clear accountability. Probabilistic outputs may complicate stakeholder communication and decision-making. Model-based methods are therefore considered optional for **sensitivity analysis** on boundary cases.

**Hierarchical Methods (e.g., Agglomerative Clustering with Gower Distance)** ✅ *Selected for Validation*

Hierarchical clustering builds a tree-like structure (dendrogram) that reveals how buildings relate to one another at multiple levels of granularity. When combined with **Gower distance**—a metric that naturally handles mixed categorical and numerical features—hierarchical methods provide several advantages:

- **Visual transparency:** Dendrograms show exactly how peer groups form, making the clustering rationale explainable to stakeholders
- **No pre-specified k:** The tree structure allows exploration of different numbers of clusters without re-running the algorithm
- **Cross-validation:** Running a fundamentally different algorithm alongside K-Prototypes provides a "sanity check"—if both methods identify similar groupings, the peer groups likely reflect genuine patterns rather than algorithmic artifacts

The analysis uses **average linkage** (UPGMA), which balances sensitivity to outliers (single linkage) against tendency to produce spherical clusters (complete linkage). Hierarchical clustering serves as a **validation method** to confirm that peer group structure is robust across algorithmic choices.

**Partitional Methods (e.g., K-Means, K-Prototypes)** ✅ *Selected as Primary*

Partitional methods produce compact, interpretable clusters with deterministic membership—aligning with stakeholder expectations of "peer groups." The K-Prototypes algorithm (Huang, 1997) is selected as the primary method because it:

- Natively handles mixed categorical and numerical features without preprocessing compromises
- Produces defensible, explainable results for non-technical stakeholders (policymakers, asset owners)
- Scales efficiently to the dataset size (~5,900 observations)
- Has established precedent in building stock modelling (Alrasheed & Mourshed, 2024)

| Method Family | Primary Role | Secondary Role |
|---------------|--------------|----------------|
| Density-based (HDBSCAN) | — | Outlier detection |
| Model-based (GMM) | — | Sensitivity analysis |
| Hierarchical (Gower + Average Linkage) | — | **Validation & visualization** |
| Partitional (K-Prototypes) | **Primary clustering** | — |

**Algorithm Limitations**

Despite careful selection, each algorithm has inherent limitations that may affect results:

| Algorithm | Limitation | Mitigation Strategy |
|-----------|------------|---------------------|
| **K-Prototypes** | Requires pre-specification of *k*; sensitive to initialization; gamma parameter balances numerical vs. categorical influence subjectively | Tested k=3–8 with multiple gamma values (0.5, 1.0, 2.0); used both Huang and Cao initialization; validated optimal *k* with silhouette scores and elbow method |
| **K-Prototypes** | Assumes spherical/compact clusters; may force buildings into groups even when natural structure is ambiguous | Cross-validated with hierarchical clustering; examined silhouette scores per cluster to identify poorly-fitting buildings |
| **Hierarchical (Gower)** | Computationally expensive for large datasets; linkage choice affects cluster shape assumptions | Used sampling for dendrogram visualization; tested multiple linkage methods (average, complete, ward) |
| **Hierarchical (Gower)** | Gower distance weights all features equally by default, which may not reflect domain importance | Accepted equal weighting as neutral baseline; future work could explore domain-informed feature weighting |
| **Both methods** | Deterministic assignments do not capture uncertainty for buildings on cluster boundaries | Noted boundary cases in interpretation; recommended manual review for buildings with low silhouette scores |

11\. Reflections

**How the Problem Statement Guided Choices**

The problem statement—*"Segment commercial buildings by structural characteristics, usage type, and climatic context to develop a data-driven prioritization matrix for identifying efficiency outliers"*—guided my choices throughout the whole analysis. The emphasis on "structural characteristics, usage type, and climatic context" directly informed feature selection: building size (sqm), age (yearbuilt), primary space usage, meter type, and climate variables (temperature) were prioritized over operational factors that vary with occupant behavior. The goal of "identifying efficiency outliers" justified the decision to analyze EUI *within* clusters rather than using it as a clustering feature—ensuring peer groups are formed on comparable characteristics, not performance itself. The "prioritization matrix" objective motivated the underperformer analysis, quantifying how many buildings in each peer group exceed their group median by more than one standard deviation.

**Alignment of Results with Objectives**

The clustering results largely achieved the stated objectives. Three distinct peer groups emerged with interpretable profiles: Warm-Climate, Cold-Climate, and Temperate-Climate peer groups, each with characteristic building types, sizes, and energy patterns. The within-cluster EUI variance was substantially lower than the population variance, confirming that peer groups enable fairer benchmarking. The identification of 912 underperformers (18.4% of buildings) across clusters provides a concrete prioritization list for retrofit targeting. However, the hypothesis that building type would differentiate clusters beyond climate (H2) received only partial support—climate remained the dominant driver, with building type showing association but not separation into distinct clusters.

**Key Insights and Challenges**

*Insights:*
- Climate is the primary determinant of building energy peer groups, validating climate-stratified benchmarking approaches
- The Temperate-Climate peer group achieves the lowest median EUI despite containing older buildings, suggesting that building age alone is not a barrier to efficiency
- Algorithm agreement (ARI = 0.51) between K-Prototypes and hierarchical clustering provides confidence that peer group structure reflects genuine patterns rather than algorithmic artifacts
- Hopkins statistic (0.948) confirmed strong clustering tendency before analysis, reducing risk of forcing structure onto random data

*Challenges:*
- High missingness in `yearbuilt` (52.9%) required imputation, potentially introducing noise into age-related patterns
- The gamma parameter in K-Prototypes required experimentation; different values produced different cluster emphases (climate vs. building type)
- Some buildings exhibited low silhouette scores, indicating ambiguous cluster membership—these boundary cases warrant manual review before policy application
- The dataset's US-heavy geographic distribution (80.8%) limits confidence in generalizing European building patterns
- Extreme skewness in energy consumption data (skewness=16.50 for `total_meter_reading`) and the presence of near-zero EUI values required log transformation; however, log transformation compresses the upper tail, potentially underweighting differences between high-consumption buildings in distance calculations

References 

-   **Alrasheed, M., & Mourshed, M. (2024).** Building stock modelling using k-prototype algorithm: A framework for representative archetype development. *Energy and Buildings*, 311, 114111. doi.org
-   **Amasyali, K., & El-Gohary, N. M. (2018).** A review of data-driven building energy consumption prediction studies. *Renewable and Sustainable Energy Reviews*, 81, 1192--1205. doi.org
-   **Ciulla, G., & D'Amico, A. (2019).** Building energy performance forecasting: A multiple linear regression approach. *Applied Energy*, 253, 113500. doi.org
-   **Deepki. (2023, November 29).** *6 reasons why building archetype clustering can level up your strategy*. [www.deepki.com](https://www.deepki.com/blog/building-archetype-clustering/)
-   **Huang, Z. (1997).** Clustering large data sets with mixed numeric and categorical values. *Proceedings of the 1st Pacific-Asia Conference on Knowledge Discovery and Data Mining*, 21--34.
-   **International Energy Agency. (2025).** *Global Energy Review 2025: CO2 emissions and energy efficiency*. [www.iea.org](https://www.iea.org/reports/global-energy-review-2025)
-   **UN Environment Programme. (2025, March 17).** *Global Status Report for Buildings and Construction 2024/2025: Not just another brick in the wall*. www.unep.org