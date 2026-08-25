from statsmodels.tsa.arima.model import ARIMA

def arima_residuals(series):
    model = ARIMA(series, order=(1,1,1))
    result = model.fit()
    return abs(result.resid)
