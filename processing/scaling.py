from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import scale


def min_max_scaler(features):
    min_max = MinMaxScaler()
    return min_max.fit_transform(features)


def standardizing(features):
    return scale(features)
