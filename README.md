# AI-Powered Energy Consumption Forecasting System ⚡

A portfolio-ready learning project for hourly electricity-consumption forecasting. It demonstrates cleaning, feature engineering, an MLP Regressor, time-ordered evaluation, charts, model persistence, next-hour inference, and a Flask web demo.

## Dataset
If `data/energy_consumption.csv` is absent, the app generates clearly labelled **simulated** hourly usage so the project runs out of the box. To use a dataset, supply a CSV with `timestamp` and `consumption_kwh` columns. Document the dataset source, license, units, and time zone. Do not describe simulated data as real-world data.

## Windows setup (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If activation is blocked, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.

## Run
```powershell
python main.py train
python main.py predict
python main.py web
```
Open `http://127.0.0.1:5000` for the web demo.

## Outputs
- `outputs/evaluation_metrics.json`: MAE, RMSE, R², baseline MAE, dataset type
- `outputs/predictions.csv`: actual and predicted values on the chronological test set
- `outputs/energy_consumption.png`: consumption history
- `outputs/actual_vs_predicted.png`: model evaluation plot
- `models/energy_forecast_model.joblib`: saved preprocessing/model pipeline

## Architecture
CSV or simulated data → validation/cleaning → calendar and lag features → chronological 80/20 split → StandardScaler + MLP Regressor → evaluation/plots → next-hour forecast → Flask UI.

## Limitations
This is an educational prototype, not a production energy management system. Synthetic-data scores do not establish real-world forecasting performance. The model must be evaluated on a suitable public or real dataset before making performance claims.

## GitHub proof checklist
Capture training metrics, both plots, a next-hour prediction, and the Flask page. Commit source code and documentation; keep virtual environments and large/private data out of Git.
