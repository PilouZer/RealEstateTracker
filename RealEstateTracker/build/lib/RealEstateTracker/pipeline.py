from sklearn.metrics import mean_squared_log_error,  make_scorer

rmsle = make_scorer(mean_squared_log_error, greater_is_better=True, squared=False)

neg_rmsle = make_scorer(mean_squared_log_error, greater_is_better=False, squared=False)
