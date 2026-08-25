from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def isolation_forest(df, features):
    model = IsolationForest(contamination=0.02, random_state=42)
    return -model.fit_predict(df[features])

def lof_detection(df, features):
    lof = LocalOutlierFactor(n_neighbors=20)
    return -lof.fit_predict(df[features])
