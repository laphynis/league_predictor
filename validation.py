from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import numpy

def forest_val_split(df, y):
    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.3, random_state=0)
    model = RandomForestRegressor(max_depth=4, n_estimators=500, random_state=0)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    # calculate the mean squared error between our predictions and their ture values
    mse = mean_squared_error(y_test, predictions)

    # square root the mean squared error to get the standard error
    rmse = numpy.sqrt(mse)

    return rmse

def forest_cross_val(df, y, folds=5, score="neg_mean_absolute_error"):
    model = RandomForestRegressor(max_depth=4, n_estimators=500, random_state=0)
    scores = cross_val_score(model, df, y, cv=folds, scoring=score)

    # cross_val_score returns an array of values so we find the mean
    return sum(scores) / len(scores)
