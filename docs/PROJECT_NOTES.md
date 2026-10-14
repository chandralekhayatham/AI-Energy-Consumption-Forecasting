# Project Notes

Objective: demonstrate hourly energy consumption forecasting.

Model: Scikit-learn MLPRegressor with StandardScaler, calendar features, lag-1 and lag-24 consumption, and prior 24-hour rolling mean. Uses a chronological split to respect time order.

Metrics: MAE and RMSE are in kWh; R² is also reported. A mean-prediction baseline provides context.

Data honesty: default data is synthetic. When using public data, document the source, license, units, time zone, missing-value handling, and resampling decisions.
