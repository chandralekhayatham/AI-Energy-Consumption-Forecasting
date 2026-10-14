import joblib, pandas as pd
from data_utils import ROOT, FEATURES, load_data

def predict_next_hour():
    path = ROOT/"models/energy_forecast_model.joblib"
    if not path.exists(): raise FileNotFoundError("Run `python main.py train` first.")
    bundle = joblib.load(path); df = load_data().sort_values("timestamp").reset_index(drop=True)
    latest = df.iloc[-1]; ts = pd.Timestamp(latest.timestamp)+pd.Timedelta(hours=1); usage = df.consumption_kwh
    row = {"hour":ts.hour,"day_of_week":ts.dayofweek,"day_of_month":ts.day,"month":ts.month,"is_weekend":int(ts.dayofweek>=5),
           "lag_1":float(usage.iloc[-1]),"lag_24":float(usage.iloc[-24]),"rolling_mean_24":float(usage.tail(24).mean())}
    value = max(0,float(bundle["model"].predict(pd.DataFrame([row])[FEATURES])[0]))
    return {"forecast_for":ts.isoformat(),"predicted_consumption_kwh":round(value,3)}

if __name__=="__main__": print(predict_next_hour())
