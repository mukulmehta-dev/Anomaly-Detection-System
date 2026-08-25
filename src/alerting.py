def dynamic_threshold(df):
    return df['final_score'].quantile(0.98)

def generate_alerts(df):
    threshold = dynamic_threshold(df)
    df['alert'] = df['final_score'] > threshold

    df['priority'] = df['final_score'].apply(
        lambda x: "HIGH" if x > 0.9 else "MEDIUM" if x > threshold else "LOW"
    )

    # False-positive reduction
    df = df[~((df['amount'] < 100) & (df['final_score'] < 0.85))]
    return df
