def dynamic_threshold(df):
    return df['final_score'].quantile(0.98)

def generate_alerts(df):
    threshold = dynamic_threshold(df)
    df['alert'] = df['final_score'] > threshold

    df['priority'] = df['final_score'].apply(
        lambda x: "HIGH" if x > 0.9 else "MEDIUM" if x > threshold else "LOW"
    )

    # False-positive reduction: suppress alerts for small amounts unless score is very high
    suppress_mask = (df['amount'] < 100) & (df['final_score'] < 0.85)
    df.loc[suppress_mask, 'alert'] = False
    df.loc[suppress_mask, 'priority'] = 'LOW'
    return df

