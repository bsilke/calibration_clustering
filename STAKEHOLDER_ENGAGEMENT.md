# Stakeholder Engagement: Building Energy Benchmarking

## 1. Project Context

This document outlines stakeholder considerations for a clustering analysis for building energy benchmarking. The analysis uses a multi-national research dataset of non-residential buildings from the US, UK, Canada, and Netherlands.

## 2. Stakeholder Mapping

### Identified Stakeholders

| # | Stakeholder | Role | Primary Interest |
|---|-------------|------|------------------|
| 1 | Building Energy Researchers | Academic community | Novel methodology; reproducible results; published findings |
| 2 | Building Portfolio Managers | Practitioners | Practical applicability; actionable peer groupings |
| 3 | Energy Consultants | Practitioners | Clear methodology for client recommendations |
| 4 | Dataset Providers | Data stewards | Appropriate use of data; acknowledgment; findings that validate data quality |

### Power/Interest Matrix

```
                              INTEREST IN PROJECT
                         Low                    High
                    ┌─────────────────────┬─────────────────────┐
               High │                     │                     │
                    │                     │                     │
      POWER         │                     │                     │
                    ├─────────────────────┼─────────────────────┤
               Low  │                     │ Building Energy     │
                    │                     │   Researchers       │
                    │                     │ Portfolio Managers  │
                    │                     │ Energy Consultants  │
                    │                     │ Dataset Providers   │
                    └─────────────────────┴─────────────────────┘
```

### Priority Relationships

| Priority | Stakeholder | Rationale |
|----------|-------------|-----------|
| **1** | Building Energy Researchers | Potential users of methodology; peer review audience |
| **2** | Building Portfolio Managers | Primary practitioners who could apply peer grouping in practice |
| **3** | Energy Consultants | Could use methodology to advise clients on building performance |

---

## 3. Stakeholder Interests

### Research Community

| Stakeholder | Key Questions | Communication Approach |
|-------------|---------------|------------------------|
| **Building Energy Researchers** | Is the methodology novel? Are results reproducible? How does it compare to existing approaches? | Published methodology; open code repository; clear documentation |

### Practitioners

| Stakeholder | Key Questions | Communication Approach |
|-------------|---------------|------------------------|
| **Building Portfolio Managers** | Can this approach help identify underperforming buildings in my portfolio? | Plain-language summary; example applications |
| **Energy Consultants** | Is the peer grouping logic defensible to clients? | Technical documentation; cluster interpretation guide |

### Data Stakeholders

| Stakeholder | Key Questions | Communication Approach |
|-------------|---------------|------------------------|
| **Dataset Providers** | Is the data being used appropriately? Are limitations acknowledged? | Proper citation; acknowledge data source; note limitations |

---

## 4. Documentation for Reproducibility

| Element | Purpose |
|---------|---------|
| **Code repository** | Enable replication of analysis |
| **Data preprocessing documentation** | Explain cleaning and transformation decisions |
| **Parameter selection rationale** | Justify clustering choices (k, feature weights) |
| **Cluster interpretation guide** | Explain what each cluster represents |

---

## 5. Potential Applications

If this methodology were applied in practice, potential stakeholders would include:

- **Municipal energy offices**: Setting differentiated performance standards by building type
- **Utility program managers**: Targeting efficiency programs to high-opportunity buildings
- **Building owners**: Understanding how their buildings compare to true peers
- **Financial institutions**: Assessing climate risk in building portfolios

The clustering approach enables fair peer-adjusted benchmarking that accounts for climate, building age, and usage type—avoiding unfair comparisons between dissimilar buildings.

---

## 6. Summary

| Component | Key Elements |
|-----------|--------------|
| **Primary stakeholders** | Building energy researchers, portfolio managers, energy consultants |
| **Key deliverables** | Methodology documentation, code repository, cluster interpretation guide |
| **Transparency mechanisms** | Reproducible code, documented decisions, clear limitations |

This project contributes a methodology for building energy peer grouping using K-Prototypes clustering on mixed data types. The primary audience is the building energy research community, with potential future application by energy policy practitioners and building portfolio managers.
