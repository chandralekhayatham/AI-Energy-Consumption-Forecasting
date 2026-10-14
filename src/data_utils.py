from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "energy_consumption.csv"
FEATURES = ["hour", "day_of_week", "day_of_month", "month", "is_weekend", "lag_1", "lag_24", "rolling_mean_24"]

def create_demo_dataset(days=180, seed=42):
    """Generate simulated hourly energy use for software demonstration only."""
    rng = np.random.default_rng(seed)
    ts = pd.date_range("2025-01-01", periods=days*24, freq="h")
    h, dow, doy = ts.hour.to_numpy(), ts.dayofweek.to_numpy(), ts.dayofyear.to_numpy()
    daily = 1.8 + .7*np.sin((h-7)*2*np.pi/24)
    evening = 1.3*np.exp(-((h-19)/3)**2)
    workday = np.where(dow < 5, .35, -.15)
    season = .25*np.sin(2*np.pi*doy/365)
    usage = np.maximum(.2, 2.8 + daily + evening + workday + season + rng.normal(0,.18,len(ts)))
    return pd.DataFrame({"timestamp":ts, "consumption_kwh":usage.round(3), "data_source":"simulated_demo"})

def load_data():
    DATA_PATH.parent.mkdir(exist_ok=True)
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        if not {"timestamp","consumption_kwh"}.issubset(df.columns):
            raise ValueError("CSV must contain timestamp and consumption_kwh columns.")
        df["data_source"] = "user_provided_dataset"
    else:
        df = create_demo_dataset()
        df.to_csv(DATA_PATH, index=False)
        print(f"Created simulated demo dataset: {DATA_PATH}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["consumption_kwh"] = pd.to_numeric(df["consumption_kwh"], errors="coerce")
    df = df.dropna(subset=["timestamp","consumption_kwh"])
    df = df[df["consumption_kwh"] >= 0].drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
    if len(df) < 100: raise ValueError("At least 100 valid rows are required.")
    return df

def make_features(df):
    d = df.sort_values("timestamp").copy()
    t = d["timestamp"]
    d["hour"], d["day_of_week"], d["day_of_month"], d["month"] = t.dt.hour, t.dt.dayofweek, t.dt.day, t.dt.month
    d["is_weekend"] = (t.dt.dayofweek >= 5).astype(int)
    d["lag_1"] = d["consumption_kwh"].shift(1)
    d["lag_24"] = d["consumption_kwh"].shift(24)
    d["rolling_mean_24"] = d["consumption_kwh"].shift(1).rolling(24).mean()
    return d.dropna().reset_index(drop=True)
