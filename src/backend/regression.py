import pickle
import os
from sklearn.linear_model import LinearRegression


def get_dataset():
    return list(), list()


def predict(x_values):
    exists = os.path.isfile('src/backend/regressor_data.pkl')

    regressor = None

    if exists:
        with open('regressor_data.pkl', 'rb') as inp:
            regressor = pickle.load(inp)
    else:
        x_train, y_train = get_dataset()
        regressor = LinearRegression()
        regressor.fit(x_train, y_train)
        with open('regressor_data.pkl', 'wb') as output:
            pickle.dump(regressor, output, pickle.HIGHEST_PROTOCOL)
    
    return regressor.predict(x_values)
