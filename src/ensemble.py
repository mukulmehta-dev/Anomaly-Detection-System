import numpy as np

def normalize(s):
    denom = s.max() - s.min()
    if denom == 0 or np.isnan(denom):
        return s * 0.0
    return (s - s.min()) / denom

def ensemble_score(df):
    df['final_score'] = (
        0.35 * normalize(df['iso_score']) +
        0.25 * normalize(df['lof_score']) +
        0.20 * normalize(df['mahalanobis']) +
        0.10 * normalize(df['z_score']) +
        0.10 * normalize(df['arima_resid'])
    )
    df['final_score'] = df['final_score'].fillna(0.0)
    return df

