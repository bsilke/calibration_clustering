"""
Algorithm Decision Tree for Clustering Analysis
================================================

This module provides a systematic, reproducible framework for selecting
clustering algorithms based on dataset characteristics, domain requirements,
and computational constraints.

Adapted for building energy benchmarking applications.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


def algorithm_decision_tree(
    data_characteristics: Dict[str, Any],
    domain_requirements: Dict[str, Any],
    computational_constraints: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Interactive algorithm decision tree for clustering algorithm selection.
    
    Parameters
    ----------
    data_characteristics : dict
        Dictionary containing:
        - n_samples: int, number of samples
        - n_features: int, number of features
        - has_categorical: bool, whether data contains categorical variables
        - has_missing: bool, whether data contains missing values
        - outlier_proportion: float, estimated proportion of outliers (0-1)
        
    domain_requirements : dict
        Dictionary containing:
        - domain: str, domain type (e.g., 'building_energy', 'demographics')
        - outlier_detection: bool, whether outlier detection is needed
        - hierarchy: bool, whether hierarchical structure is needed
        - peer_groups: bool, whether peer group identification is the goal
        - interpretability: str, level of interpretability needed ('high', 'medium', 'low')
        
    computational_constraints : dict
        Dictionary containing:
        - time_minutes: int, maximum time allowed for clustering
        - memory_gb: float, available memory in GB
        - need_reproducibility: bool, whether reproducibility is required
        
    Returns
    -------
    dict
        Dictionary containing:
        - recommendation: str, recommended algorithm
        - alternatives: list, alternative algorithms to consider
        - decision_path: list, sequence of decisions made
        - confidence: str, confidence level in recommendation
        - rationale: str, detailed rationale for recommendation
    """
    
    print("=" * 70)
    print("ALGORITHM DECISION TREE FOR CLUSTERING")
    print("=" * 70)
    
    # Extract characteristics
    n_samples = data_characteristics.get('n_samples', 0)
    n_features = data_characteristics.get('n_features', 0)
    has_categorical = data_characteristics.get('has_categorical', False)
    has_missing = data_characteristics.get('has_missing', False)
    outlier_proportion = data_characteristics.get('outlier_proportion', 0.0)
    
    domain = domain_requirements.get('domain', 'general')
    needs_outliers = domain_requirements.get('outlier_detection', False)
    needs_hierarchy = domain_requirements.get('hierarchy', False)
    needs_peer_groups = domain_requirements.get('peer_groups', False)
    interpretability = domain_requirements.get('interpretability', 'medium')
    
    time_limit = computational_constraints.get('time_minutes', 60)
    need_reproducibility = computational_constraints.get('need_reproducibility', True)
    
    # Decision path tracking
    decisions = []
    alternatives = []
    
    # =========================================================================
    # LEVEL 1: Data Type Assessment (Categorical vs Numerical)
    # =========================================================================
    print("\n📊 LEVEL 1: Data Type Assessment")
    print("-" * 40)
    
    if has_categorical:
        type_decision = "Mixed data types detected → K-Prototypes or Gower distance required"
        decisions.append(("Data Type", type_decision))
        mixed_data = True
        print(f"  → {type_decision}")
    else:
        type_decision = "Numerical data only → Standard distance metrics applicable"
        decisions.append(("Data Type", type_decision))
        mixed_data = False
        print(f"  → {type_decision}")
    
    # =========================================================================
    # LEVEL 2: Sample Size Assessment
    # =========================================================================
    print(f"\n📏 LEVEL 2: Sample Size Assessment (n={n_samples:,})")
    print("-" * 40)
    
    if n_samples < 500:
        size_decision = "Small dataset (<500) → All algorithms feasible"
        size_constraint = None
        decisions.append(("Sample Size", size_decision))
    elif n_samples < 5000:
        size_decision = "Medium dataset (500-5,000) → Most algorithms feasible"
        size_constraint = None
        decisions.append(("Sample Size", size_decision))
    elif n_samples < 50000:
        size_decision = "Large dataset (5,000-50,000) → K-means/K-Prototypes preferred"
        size_constraint = 'large'
        decisions.append(("Sample Size", size_decision))
    else:
        size_decision = "Very large dataset (>50,000) → Scalable algorithms only"
        size_constraint = 'very_large'
        decisions.append(("Sample Size", size_decision))
    
    print(f"  → {size_decision}")
    
    # =========================================================================
    # LEVEL 3: Domain-Specific Requirements
    # =========================================================================
    print(f"\n🏢 LEVEL 3: Domain Requirements (domain={domain})")
    print("-" * 40)
    
    if domain == 'building_energy':
        domain_decision = "Building energy benchmarking → Peer group identification priority"
        decisions.append(("Domain", domain_decision))
        print(f"  → {domain_decision}")
        
        if needs_peer_groups:
            peer_decision = "Peer group identification needed → Centroid-based clustering preferred"
            decisions.append(("Peer Groups", peer_decision))
            print(f"  → {peer_decision}")
    
    elif domain == 'environmental_justice':
        domain_decision = "Environmental justice → Irregular cluster shapes expected"
        decisions.append(("Domain", domain_decision))
        print(f"  → {domain_decision}")
    
    elif domain in ['demographics', 'housing']:
        domain_decision = "Standard demographic clustering → Balanced clusters expected"
        decisions.append(("Domain", domain_decision))
        print(f"  → {domain_decision}")
    
    else:
        domain_decision = "General domain → No specific algorithm preference"
        decisions.append(("Domain", domain_decision))
        print(f"  → {domain_decision}")
    
    # =========================================================================
    # LEVEL 4: Special Requirements
    # =========================================================================
    print(f"\n⚙️ LEVEL 4: Special Requirements")
    print("-" * 40)
    
    if needs_outliers:
        outlier_decision = "Outlier detection needed → DBSCAN advantageous"
        decisions.append(("Outliers", outlier_decision))
        print(f"  → {outlier_decision}")
    
    if needs_hierarchy:
        hierarchy_decision = "Hierarchical structure needed → Hierarchical clustering advantageous"
        decisions.append(("Hierarchy", hierarchy_decision))
        print(f"  → {hierarchy_decision}")
    
    if interpretability == 'high':
        interp_decision = "High interpretability needed → Centroid-based methods preferred"
        decisions.append(("Interpretability", interp_decision))
        print(f"  → {interp_decision}")
    
    if outlier_proportion > 0.10:
        robust_decision = f"High outlier proportion ({outlier_proportion:.1%}) → Robust methods needed"
        decisions.append(("Robustness", robust_decision))
        print(f"  → {robust_decision}")
    
    # =========================================================================
    # FINAL RECOMMENDATION
    # =========================================================================
    print(f"\n🎯 FINAL RECOMMENDATION")
    print("=" * 70)
    
    # Decision logic
    if mixed_data:
        # Mixed data requires special handling
        if size_constraint == 'very_large':
            final_recommendation = "Mini-batch K-Prototypes (if available) or Feature Engineering + K-means"
            alternatives = ["Encode categoricals + K-means", "Sample data + K-Prototypes"]
            confidence = "Medium"
        else:
            final_recommendation = "K-Prototypes"
            alternatives = ["Gower distance + Hierarchical", "Encode categoricals + K-means"]
            confidence = "High"
        
        rationale = (
            "K-Prototypes is recommended for datasets with mixed numerical and categorical "
            "variables. It extends K-means to handle categorical features using a combined "
            "distance metric (Euclidean for numerical, matching for categorical). This is "
            "particularly suitable for building energy data where categorical variables like "
            "building type and region are important clustering features."
        )
    
    elif needs_outliers and not size_constraint:
        final_recommendation = "DBSCAN"
        alternatives = ["HDBSCAN", "K-means with outlier removal"]
        confidence = "High"
        rationale = (
            "DBSCAN is recommended when outlier detection is a priority. It does not force "
            "all points into clusters and explicitly labels outliers as noise. This is useful "
            "for identifying anomalous buildings that may require special attention."
        )
    
    elif needs_hierarchy and not size_constraint:
        final_recommendation = "Hierarchical Clustering (Ward linkage)"
        alternatives = ["Agglomerative with complete linkage", "BIRCH"]
        confidence = "High"
        rationale = (
            "Hierarchical clustering is recommended when nested cluster structures are needed. "
            "Ward linkage minimises within-cluster variance and produces interpretable dendrograms."
        )
    
    elif size_constraint == 'very_large':
        final_recommendation = "Mini-batch K-means"
        alternatives = ["K-means with sampling", "BIRCH"]
        confidence = "High"
        rationale = (
            "Mini-batch K-means is recommended for very large datasets due to its computational "
            "efficiency. It processes data in batches rather than requiring all data in memory."
        )
    
    else:
        final_recommendation = "K-means"
        alternatives = ["K-medoids", "Gaussian Mixture Models"]
        confidence = "High"
        rationale = (
            "K-means is recommended as a robust default for numerical data with balanced clusters. "
            "It is computationally efficient, well-understood, and produces interpretable centroids "
            "that can serve as peer group profiles for benchmarking."
        )
    
    # Print recommendation
    print(f"\n  RECOMMENDED ALGORITHM: {final_recommendation}")
    print(f"  ALTERNATIVES: {', '.join(alternatives)}")
    print(f"  CONFIDENCE: {confidence}")
    print(f"\n  RATIONALE:")
    print(f"  {rationale}")
    
    # Print decision path
    print(f"\n📋 DECISION PATH:")
    print("-" * 40)
    for i, (level, decision) in enumerate(decisions, 1):
        print(f"  {i}. [{level}] {decision}")
    
    print("=" * 70)
    
    return {
        'recommendation': final_recommendation,
        'alternatives': alternatives,
        'decision_path': decisions,
        'confidence': confidence,
        'rationale': rationale
    }


def create_building_energy_flowchart() -> str:
    """
    Create a building energy-specific decision flowchart.
    
    Returns
    -------
    str
        ASCII flowchart for building energy clustering decisions.
    """
    
    flowchart = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║           BUILDING ENERGY CLUSTERING ALGORITHM FLOWCHART                  ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    START: Building Energy Benchmarking Analysis
    │
    ├─── Q1: Does the dataset contain categorical variables?
    │    │   (e.g., building type, region, meter type)
    │    │
    │    ├─── YES ──────────────────────────────────────────────┐
    │    │                                                      │
    │    │    ┌────────────────────────────────────────────┐    │
    │    │    │ RECOMMENDATION: K-Prototypes               │    │
    │    │    │                                            │    │
    │    │    │ • Handles mixed numerical/categorical data │    │
    │    │    │ • Produces interpretable cluster centroids │    │
    │    │    │ • Suitable for peer group identification   │    │
    │    │    └────────────────────────────────────────────┘    │
    │    │                                                      │
    │    └─── NO ───────────────────────────────────────────────┤
    │                                                           │
    │         ┌─────────────────────────────────────────────┐   │
    │         │ Continue to Q2                              │   │
    │         └─────────────────────────────────────────────┘   │
    │                                                           │
    ├─── Q2: Is outlier/anomaly detection a primary goal?       │
    │    │                                                      │
    │    ├─── YES ──────────────────────────────────────────────┤
    │    │                                                      │
    │    │    ┌────────────────────────────────────────────┐    │
    │    │    │ RECOMMENDATION: DBSCAN                     │    │
    │    │    │                                            │    │
    │    │    │ • Explicitly identifies outliers as noise  │    │
    │    │    │ • Does not force all buildings into groups │    │
    │    │    │ • Good for finding anomalous performers    │    │
    │    │    └────────────────────────────────────────────┘    │
    │    │                                                      │
    │    └─── NO ───────────────────────────────────────────────┤
    │                                                           │
    ├─── Q3: Is dataset size > 50,000 buildings?                │
    │    │                                                      │
    │    ├─── YES ──────────────────────────────────────────────┤
    │    │                                                      │
    │    │    ┌────────────────────────────────────────────┐    │
    │    │    │ RECOMMENDATION: Mini-batch K-means         │    │
    │    │    │                                            │    │
    │    │    │ • Computationally efficient for large data │    │
    │    │    │ • Processes data in manageable batches     │    │
    │    │    │ • Scalable to millions of buildings        │    │
    │    │    └────────────────────────────────────────────┘    │
    │    │                                                      │
    │    └─── NO ───────────────────────────────────────────────┤
    │                                                           │
    └─── DEFAULT                                                │
         │                                                      │
         ▼                                                      │
    ┌────────────────────────────────────────────────────────┐  │
    │ RECOMMENDATION: K-means                                │  │
    │                                                        │  │
    │ • Well-suited for balanced peer groups                 │  │
    │ • Produces interpretable cluster centroids             │  │
    │ • Efficient and well-understood                        │  │
    │ • Standard choice for energy benchmarking              │  │
    └────────────────────────────────────────────────────────┘  │
                                                                │
    ════════════════════════════════════════════════════════════╝
    
    VALIDATION REQUIREMENTS (All Algorithms):
    ─────────────────────────────────────────
    • Bootstrap stability assessment (100-200 resamples)
    • Silhouette score analysis
    • Within-cluster variance evaluation
    • Domain expert review of cluster profiles
    
    POST-CLUSTERING ANALYSIS:
    ─────────────────────────
    • Calculate Energy Use Intensity (EUI) within each cluster
    • Identify efficiency outliers relative to peer group
    • Assess cluster composition for rare categories
    • Document cluster characteristics for benchmarking
    """
    
    return flowchart


def apply_to_bdg2_dataset() -> Dict[str, Any]:
    """
    Apply the algorithm decision tree to the Building Data Genome 2 dataset
    characteristics as assessed in the data quality assessment.
    
    Returns
    -------
    dict
        Algorithm recommendation for the BDG2 dataset.
    """
    
    print("\n" + "=" * 70)
    print("APPLYING DECISION TREE TO BDG2 BUILDING ENERGY DATASET")
    print("=" * 70)
    
    # Dataset characteristics from data quality assessment
    data_characteristics = {
        'n_samples': 5902,
        'n_features': 15,
        'has_categorical': True,  # primaryspaceusage, region, country, meter
        'has_missing': True,      # 47% missing yearbuilt
        'outlier_proportion': 0.15  # ~15% outliers in total_meter_reading
    }
    
    # Domain requirements for building energy benchmarking
    domain_requirements = {
        'domain': 'building_energy',
        'outlier_detection': False,  # Outliers are efficiency targets, not noise
        'hierarchy': False,          # Peer groups, not nested hierarchy
        'peer_groups': True,         # Primary goal is peer group identification
        'interpretability': 'high'   # Need interpretable clusters for benchmarking
    }
    
    # Computational constraints
    computational_constraints = {
        'time_minutes': 60,
        'memory_gb': 8.0,
        'need_reproducibility': True
    }
    
    print("\n📊 Dataset Characteristics (from Data Quality Assessment):")
    print(f"   • Sample size: {data_characteristics['n_samples']:,}")
    print(f"   • Features: {data_characteristics['n_features']}")
    print(f"   • Contains categorical variables: {data_characteristics['has_categorical']}")
    print(f"   • Contains missing data: {data_characteristics['has_missing']}")
    print(f"   • Estimated outlier proportion: {data_characteristics['outlier_proportion']:.1%}")
    
    print("\n🏢 Domain Requirements:")
    print(f"   • Domain: {domain_requirements['domain']}")
    print(f"   • Peer group identification: {domain_requirements['peer_groups']}")
    print(f"   • Interpretability requirement: {domain_requirements['interpretability']}")
    
    print("\n")
    
    # Run decision tree
    result = algorithm_decision_tree(
        data_characteristics,
        domain_requirements,
        computational_constraints
    )
    
    return result


def print_implementation_guidance(recommendation: str) -> None:
    """
    Print implementation guidance for the recommended algorithm.
    
    Parameters
    ----------
    recommendation : str
        The recommended algorithm name.
    """
    
    print("\n" + "=" * 70)
    print(f"IMPLEMENTATION GUIDANCE: {recommendation}")
    print("=" * 70)
    
    if "K-Prototypes" in recommendation:
        guidance = """
    LIBRARY: kmodes (pip install kmodes)
    
    PREPROCESSING STEPS:
    1. Log-transform skewed numerical variables (total_meter_reading, sqm)
    2. Apply RobustScaler to numerical features
    3. Impute or exclude yearbuilt (47% missing)
    4. Consider PCA for climate variables (high multicollinearity)
    5. Optionally aggregate rare meter types into "Other"
    
    HYPERPARAMETERS:
    • n_clusters: Use elbow method or silhouette analysis (try 4-8 clusters)
    • gamma: Weight for categorical features (default=0.5, tune based on domain)
    • n_init: Number of initialisations (recommend 10-20)
    • max_iter: Maximum iterations (default 100, increase if not converging)
    
    EXAMPLE CODE:
    ```python
    from kmodes.kprototypes import KPrototypes
    from sklearn.preprocessing import RobustScaler
    import numpy as np
    
    # Identify categorical column indices
    categorical_indices = [df.columns.get_loc(col) for col in categorical_cols]
    
    # Fit K-Prototypes
    kproto = KPrototypes(
        n_clusters=5,
        init='Huang',
        n_init=10,
        max_iter=100,
        gamma=0.5,
        random_state=42
    )
    
    clusters = kproto.fit_predict(X, categorical=categorical_indices)
    ```
    
    VALIDATION:
    • Cost function convergence (kproto.cost_)
    • Cluster size distribution
    • Silhouette score (for numerical features)
    • Bootstrap stability assessment
    • Domain expert review of cluster centroids
        """
    
    elif "K-means" in recommendation:
        guidance = """
    LIBRARY: scikit-learn
    
    PREPROCESSING STEPS:
    1. Encode categorical variables (one-hot or target encoding)
    2. Log-transform skewed numerical variables
    3. Apply RobustScaler to all features
    4. Handle missing data (imputation or exclusion)
    
    HYPERPARAMETERS:
    • n_clusters: Use elbow method or silhouette analysis
    • init: 'k-means++' (default, recommended)
    • n_init: Number of initialisations (recommend 10-20)
    • max_iter: Maximum iterations (default 300)
    
    EXAMPLE CODE:
    ```python
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import RobustScaler
    
    # Scale features
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Fit K-means
    kmeans = KMeans(
        n_clusters=5,
        init='k-means++',
        n_init=20,
        max_iter=300,
        random_state=42
    )
    
    clusters = kmeans.fit_predict(X_scaled)
    ```
    
    VALIDATION:
    • Inertia (within-cluster sum of squares)
    • Silhouette score
    • Calinski-Harabasz index
    • Bootstrap stability assessment
        """
    
    elif "DBSCAN" in recommendation:
        guidance = """
    LIBRARY: scikit-learn
    
    PREPROCESSING STEPS:
    1. Scale all features (DBSCAN is distance-sensitive)
    2. Consider dimensionality reduction if many features
    
    HYPERPARAMETERS:
    • eps: Maximum distance between samples (use k-distance graph to tune)
    • min_samples: Minimum samples for core point (rule of thumb: 2 * n_features)
    
    EXAMPLE CODE:
    ```python
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Fit DBSCAN
    dbscan = DBSCAN(
        eps=0.5,
        min_samples=10
    )
    
    clusters = dbscan.fit_predict(X_scaled)
    # Note: -1 indicates outliers
    ```
    
    VALIDATION:
    • Proportion of outliers (label=-1)
    • Silhouette score (excluding outliers)
    • Visual inspection of cluster assignments
        """
    
    else:
        guidance = "No specific guidance available for this algorithm."
    
    print(guidance)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    
    # Print the building energy flowchart
    print(create_building_energy_flowchart())
    
    # Apply decision tree to BDG2 dataset
    result = apply_to_bdg2_dataset()
    
    # Print implementation guidance
    print_implementation_guidance(result['recommendation'])
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY FOR BDG2 BUILDING ENERGY DATASET")
    print("=" * 70)
    print(f"""
    RECOMMENDED ALGORITHM: {result['recommendation']}
    
    KEY REASONS:
    1. Dataset contains categorical variables (building type, region, meter type)
       that are important for peer group formation
    2. K-Prototypes handles mixed data types natively without encoding
    3. Produces interpretable cluster centroids for benchmarking
    4. Sample size (5,902) is well within computational feasibility
    
    PREPROCESSING PIPELINE:
    1. Log-transform: total_meter_reading, sqm
    2. Handle missing: Impute or exclude yearbuilt
    3. Scale numerical: RobustScaler
    4. Climate variables: PCA to 1-2 components or select representatives
    5. Rare categories: Consider aggregating rare meter types
    
    VALIDATION STRATEGY:
    1. Bootstrap stability assessment (100-200 resamples)
    2. Silhouette analysis for optimal k
    3. Within-cluster EUI variance analysis
    4. Expert review of cluster profiles
    
    CONFIDENCE: {result['confidence']}
    """)
