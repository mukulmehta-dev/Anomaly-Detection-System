import numpy as np

def create_features(df):
    df['amount_log'] = np.log1p(df['amount'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.dayofweek

    df['rolling_mean'] = df['amount'].rolling(10).mean()
    df['rolling_std'] = df['amount'].rolling(10).std()

    # 🔧 Custom features
    df['amount_to_avg_ratio'] = df['amount'] / (df['rolling_mean'] + 1)
    df['odd_hour_flag'] = df['hour'].apply(lambda x: 1 if x < 6 else 0)

    df.fillna(0, inplace=True)
    return df
