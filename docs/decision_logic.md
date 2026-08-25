## Decision Logic

A transaction is flagged based on:
- Isolation Forest global deviation
- Local Outlier Factor neighborhood deviation
- Mahalanobis multivariate distance
- Time-series residual deviation
- Behavioral anomalies (odd hour, amount ratio)

Weights and thresholds were customized to reduce false positives
and align with real-world fraud constraints.
