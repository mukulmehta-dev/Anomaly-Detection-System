def normalize(s):
    return (s - s.min()) / (s.max() - s.min())

def ensemble_score(df):
    df['final_score'] = (
        0.35 * normalize(df['iso_score']) +
        0.25 * normalize(df['lof_score']) +
        0.20 * normalize(df['mahalanobis']) +
        0.10 * normalize(df['z_score']) +
        0.10 * normalize(df['arima_resid'])
    )
    return df
