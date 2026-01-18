# Ethics Framework: Building Energy Benchmarking

## 1. Potential Harms

This clustering analysis groups non-residential buildings by characteristics (climate, age, usage type, region) to enable fair energy benchmarking. Potential harms include:

| Affected Party | Potential Harm | Likelihood | Severity |
|----------------|----------------|------------|----------|
| **Building owners flagged as outliers** | Reputational concerns if results are published; potential financing implications | Low | Low |
| **Building types associated with public services** | Usage types like "Education" or "Public services" may be systematically flagged if they have older building stock | Low | Low |

The dataset contains aggregated building-level energy data without individual tenant information, income indicators, or neighborhood demographics. This limits both the potential for individual harm and the ability to assess equity impacts.

## 2. Bias Considerations

### Data Limitations

| Data Element | Consideration |
|--------------|---------------|
| **Building age (`yearbuilt`)** | Older buildings (some dating to 1900) may have different energy profiles due to construction standards, not owner behaviour |
| **Usage type (`primaryspaceusage`)** | Ten categories ranging from Education to Warehouse/storage; some types inherently consume more energy |
| **Region** | 13 locations across US, UK, Canada, and Netherlands; regional energy infrastructure and climate vary |
| **Climate (`Avg_AirTemp_Annual`)** | Temperature differences affect baseline energy needs; clustering accounts for this |

### Interpretation Risks

- **Deficit framing**: Clusters should be described by their characteristics, not labeled as "good" or "bad"
- **Deterministic categorization**: Cluster assignments are data-driven estimates, not permanent labels
- **Cross-regional comparisons**: Buildings in different countries operate under different regulatory and climate contexts

## 3. Transparency and Documentation

The analysis maintains transparency through:

- **Published methodology**: Full documentation of clustering approach, feature selection, and parameter choices
- **Uncertainty acknowledgment**: Cluster assignments presented as estimates with silhouette scores and other quality metrics
- **Limitation disclosure**: Dataset covers specific regions and building types; results may not generalize

## 4. Safeguards

- **Asset-based framing**: Outlier status presented as retrofit opportunity, not building failure
- **Peer-adjusted benchmarking**: Buildings compared to similar peers rather than universal standards
- **Methodology transparency**: Full technical documentation published
- **Context preservation**: Results interpreted within regional and usage-type context

## 5. Benefit-Risk Balance

**Benefits:**
- Targeted identification of buildings with largest efficiency gaps relative to peers
- Fair benchmarking that accounts for climate, age, and usage type
- Evidence base for differentiated energy performance standards

**Risks:**
- Misinterpretation of cluster assignments as permanent labels
- Over-generalization of results beyond the dataset's scope

The benefits of fair peer-adjusted benchmarking justify the limited risks, provided that results are communicated with appropriate caveats about data scope and uncertainty.

## 6. Summary

This ethics framework addresses the (limited) potential harms of building energy benchmarking using aggregated, anonymized building data. The dataset contains no individual tenant information or demographic indicators, which limits both harm potential and equity assessment capability.

Key safeguards include asset-based framing, peer-adjusted comparisons, and transparent methodology. Results should be interpreted as data-driven estimates applicable to the specific building types and regions represented in the dataset.
