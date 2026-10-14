import json, joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from data_utils import ROOT, FEATURES, load_data, make_features

def main():
    (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"models").mkdir(exist_ok=True)
    raw = load_data(); data = make_features(raw)
    cut = int(len(data)*.8); train, test = data.iloc[:cut], data.iloc[cut:]
    model = Pipeline([("scale",StandardScaler()),("mlp",MLPRegressor(hidden_layer_sizes=(64,32),max_iter=700,early_stopping=True,random_state=42,n_iter_no_change=25))])
    model.fit(train[FEATURES],train.consumption_kwh)
    pred = model.predict(test[FEATURES]); actual = test.consumption_kwh
    baseline = DummyRegressor(strategy="mean").fit(np.zeros((len(train),1)),train.consumption_kwh)
    base_pred = baseline.predict(np.zeros((len(test),1)))
    metrics = {"dataset_type":str(raw.data_source.iloc[0]),"raw_rows":int(len(raw)),"train_rows":int(len(train)),"test_rows":int(len(test)),
      "mae_kwh":float(mean_absolute_error(actual,pred)),"rmse_kwh":float(np.sqrt(mean_squared_error(actual,pred))),
      "r2":float(r2_score(actual,pred)),"baseline_mean_mae_kwh":float(mean_absolute_error(actual,base_pred)),
      "note":"Synthetic demo data is used unless data/energy_consumption.csv is supplied."}
    (ROOT/"outputs/evaluation_metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    result = test[["timestamp","consumption_kwh"]].copy(); result["predicted_kwh"] = pred
    result.to_csv(ROOT/"outputs/predictions.csv",index=False)
    plt.figure(figsize=(12,5)); plt.plot(raw.timestamp,raw.consumption_kwh,lw=.8); plt.title("Hourly Energy Consumption"); plt.xlabel("Time"); plt.ylabel("kWh"); plt.tight_layout(); plt.savefig(ROOT/"outputs/energy_consumption.png",dpi=150); plt.close()
    plt.figure(figsize=(12,5)); plt.plot(result.timestamp,result.consumption_kwh,label="Actual"); plt.plot(result.timestamp,result.predicted_kwh,label="Predicted"); plt.title("Actual vs Predicted (chronological test set)"); plt.xlabel("Time"); plt.ylabel("kWh"); plt.legend(); plt.tight_layout(); plt.savefig(ROOT/"outputs/actual_vs_predicted.png",dpi=150); plt.close()
    joblib.dump({"model":model,"features":FEATURES},ROOT/"models/energy_forecast_model.joblib")
    print("Training completed. Metrics:\n"+json.dumps(metrics,indent=2))
    print("Saved model, predictions, metrics and charts.")

if __name__=="__main__": main()
