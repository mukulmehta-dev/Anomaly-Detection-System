import numpy as np
from scipy.stats import zscore
from scipy.spatial.distance import mahalanobis

def z_score_detection(df, col):
    return abs(zscore(df[col]))

def modified_z_score(df, col):
    median = np.median(df[col])
    mad = np.median(np.abs(df[col] - median))
    return 0.6745 * (df[col] - median) / mad

def mahalanobis_distance(df, features):
    cov = np.cov(df[features].values.T)
    inv_cov = np.linalg.inv(cov)
    mean = df[features].mean().values

    return [
        mahalanobis(row, mean, inv_cov)
        for row in df[features].values
    ]
