# Problem Decomposition: Building Energy Benchmarking

## 1. Ultimate Impact Goal

**Reduce operational carbon emissions from the built environment by enabling data-driven identification and prioritization of inefficient buildings for retrofit intervention.**

The building and construction sector accounts for approximately 34% of global energy-related CO₂ emissions. Targeted retrofits of the worst-performing buildings offer one of the highest-leverage decarbonization opportunities, but effective targeting requires fair, peer-adjusted benchmarking.

---

## 2. Sub-Problem Decomposition (5W Framework)

### Sub-Problem 1: Peer Group Formation for Fair Benchmarking

| Dimension | Description |
|-----------|-------------|
| **Who** | Non-residential buildings across diverse usage types (office, retail, industrial, educational, healthcare) |
| **What** | Structural characteristics (age, size), operational profiles (usage type), and climatic context (temperature, region) |
| **Where** | Multiple climate zones and geographic regions represented in the dataset |
| **When** | Annual energy consumption patterns (2016–2017 data) |
| **Why** | Traditional benchmarking methods compare dissimilar buildings, producing misleading efficiency assessments and misdirected interventions |

**Clustering Objective:** Segment buildings into homogeneous peer groups based on energy-relevant characteristics to enable like-for-like comparisons.

---

### Sub-Problem 2: Efficiency Outlier Identification

| Dimension | Description |
|-----------|-------------|
| **Who** | Buildings within each peer group; policymakers and asset owners requiring prioritization guidance |
| **What** | Energy Use Intensity (EUI; kWh/sqm) deviations from peer-group medians |
| **Where** | Within each identified cluster |
| **When** | Post-clustering analysis phase |
| **Why** | Limited retrofit budgets require targeting buildings with the largest efficiency gaps relative to comparable peers |

**Clustering Objective:** Identify buildings that consume significantly more energy than structurally and climatically similar peers.

---

### Sub-Problem 3: Retrofit Prioritization and Resource Allocation

| Dimension | Description |
|-----------|-------------|
| **Who** | Policymakers allocating subsidies; financial institutions assessing climate risk; facility managers justifying capital expenditure |
| **What** | Ranked lists of buildings by retrofit priority; eligibility criteria for subsidy programs |
| **Where** | Policy jurisdictions and investment portfolios |
| **When** | Budget cycles, policy review periods, investment decision windows |
| **Why** | Emission reduction targets require efficient allocation of limited retrofit funding |

**Clustering Objective:** Translate peer-group membership and efficiency gap magnitude into actionable prioritization frameworks.

---

### Sub-Problem 4: Temporal Energy Pattern Analysis

| Dimension | Description |
|-----------|-------------|
| **Who** | Buildings with multi-year consumption data |
| **What** | Year-over-year changes in EUI; seasonal consumption patterns |
| **Where** | Across all peer groups |
| **When** | Longitudinal comparison (2016 vs. 2017) |
| **Why** | Static snapshots may miss buildings with deteriorating performance or successful efficiency improvements |

**Clustering Objective:** Segment buildings by temporal consumption trajectories to identify deteriorating assets and successful retrofits.

> 💡 **Future Project Opportunity:** This sub-problem presents a worthwhile extension once additional years of consumption data become available. Longitudinal clustering could reveal buildings experiencing performance degradation (indicating maintenance needs) or successful efficiency improvements (providing retrofit case studies). With 3+ years of data, trajectory-based segmentation would complement the static peer grouping developed in the current project.

---

### Sub-Problem 5: Climate-Adjusted Baseline Development

| Dimension | Description |
|-----------|-------------|
| **Who** | Buildings in regions with extreme or variable climates |
| **What** | Climate-normalized EUI baselines accounting for heating and cooling degree days |
| **Where** | Climate zones with significant seasonal variation |
| **When** | Annual normalization |
| **Why** | Raw EUI comparisons penalize buildings in harsh climates; climate adjustment enables fairer cross-regional benchmarking |

**Clustering Objective:** Develop climate-adjusted peer groups that account for heating/cooling demand differences.

> 💡 **Future Project Opportunity:** This sub-problem offers a lot of potential for a follow-on analysis. Incorporating Heating Degree Days (HDD) and Cooling Degree Days (CDD) would enable true climate normalization, producing fairer cross-regional comparisons. This enhancement would be particularly valuable for national or international benchmarking programs where buildings span diverse climate zones. The methodology developed in the current project provides a foundation upon which climate-adjusted peer groups could be built.

---

## 3. Feasibility–Impact Matrix

| Clustering Objective | Impact | Feasibility | Priority |
|---------------------|--------|-------------|----------|
| **Peer group formation** | High | High | ✅ **Start here** |
| **Efficiency outlier identification** | High | High | ✅ **Start here** |
| **Retrofit prioritization framework** | High | High | ✅ **Start here** |
| Temporal pattern analysis | Medium | Medium | 🔮 **Future project** (requires multi-year data) |
| Climate-adjusted baselines | High | Medium | 🔮 **Future project** (requires HDD/CDD data) |

### Matrix Visualization

```
                        FEASIBILITY
                    Low             High
              ┌─────────────┬─────────────┐
         High │ Climate-    │ Peer groups │
              │ adjusted    │ Outlier ID  │
   IMPACT     │ baselines   │ Prioritiz.  │
              ├─────────────┼─────────────┤
         Low  │ (none       │ Temporal    │
              │ identified) │ patterns    │
              └─────────────┴─────────────┘
```

---

## 4. Selected Clustering Problems

Based on the feasibility–impact assessment, three interconnected clustering problems form the scope of the current analysis:

### Primary Objective: Peer Group Formation

Segment non-residential buildings into 4–6 homogeneous clusters based on structural characteristics (year built, floor area), usage type, and climatic context (annual average temperature, region). Success is measured by within-cluster EUI variance reduction of at least 30% compared to the full dataset.

### Secondary Objective: Efficiency Outlier Identification

Within each peer group, identify buildings with EUI exceeding the cluster median by more than one standard deviation. These outliers represent high-priority retrofit candidates.

### Tertiary Objective: Prioritization Framework

Translate cluster membership and efficiency gap magnitude into ranked prioritization lists for energy audits, subsidy eligibility criteria, and climate risk scoring.

---

## 5. SMART Objective (Primary Clustering Problem)

| Criterion | Specification |
|-----------|---------------|
| **Specific** | Segment non-residential buildings across various usage types (office, retail, industrial, educational) and climate zones using structural, operational, and climatic features |
| **Measurable** | Discover 4–6 peer groups with distinct Energy Use Intensity profiles; within-cluster variance reduction ≥30% compared to full dataset |
| **Achievable** | Dataset contains ~5,900 observations with cleaned numerical and categorical features; K-Prototypes algorithm selected for mixed-type clustering |
| **Relevant** | Directly informs policymakers and asset owners by enabling fair benchmarking and supporting evidence-based energy efficiency standards |
| **Time-bound** | Analysis completed and cluster profiles delivered by 1 February 2026 |

---

## 6. Relationship to Broader Sustainability Goal

The selected clustering objectives address one component of the larger decarbonization challenge:

```
Ultimate Goal: Reduce built environment emissions
        │
        ├── Building efficiency (THIS PROJECT)
        │       ├── Peer group formation ← Selected
        │       ├── Outlier identification ← Selected
        │       └── Retrofit prioritization ← Selected
        │
        ├── Energy supply decarbonization
        │       └── (Out of scope)
        │
        ├── New construction standards
        │       └── (Out of scope)
        │
        └── Embodied carbon in materials
                └── (Out of scope)
```

The peer group clustering methodology developed in this project provides a replicable framework that could be extended to other building stocks, jurisdictions, or energy efficiency programs.
