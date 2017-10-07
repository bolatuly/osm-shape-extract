import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial import distance
from processing.scaling import min_max_scaler
from processing.scaling import scale

class OwnKNN():
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self,X_test):
        predictions = []
        for row in X_test:
            label = self.closest(row)
            predictions.append(label)
        return predictions

    def closest(self, row):
        best_dist = euc(row, self.X_train[0])
        best_index = 0
        for i in range(1, len(self.X_train)):
            dist = euc(row, self.X_train[i])
            if dist < best_dist:
                best_dist = dist
                best_index = i
        return self.y_train[best_index]

def euc(a, b):
    return distance.euclidean(a, b)


if __name__ == '__main__':
    df = pd.read_csv("../data/south_korea_buildings.csv", header=0)

    df = df.drop(["Unnamed: 0"], axis=1)
    df = df.drop(["id"], axis=1)
    df = df[df.type != 'no']
    df = df[df.type != 'yes']
    df = df.groupby("type").filter(lambda x: len(x) > 10)

    # transform values
    mapping_type = {"type": {'school': 0, 'yes': 1, 'university': 2, 'commercial': 3
        , 'apartments': 4, 'greenhouse': 5,
                             'college': 6, 'church': 7, 'retail': 8, 'public': 9, 'roof': 10, 'office': 11,
                             'residential': 12,
                             'dormitory': 13, 'warehouse': 14, 'hospital': 15, 'civic': 16, 'supermarket': 17,
                             'train_station': 18,
                             'kindergarten': 19, 'hotel': 20, 'gate': 21, 'construction': 22, 'industrial': 23,
                             'house': 24,
                             'stadium': 25, 'garage': 26, 'manufacture': 27, 'transportation': 28, 'service': 29,
                             'shed': 30,
                             'hangar': 31, 'bunker': 32, 'terrace': 33, 'garages': 34, 'cathedral': 35, 'barn': 36,
                             'detached': 37,
                             'restaurant': 38}}
    df = df.replace(mapping_type)

    columns = ["compactness", "area", "length", "n_nodes"]
    labels = df["type"].values
    features = df[list(columns)].values

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=.01)

    # my_classifier = tree.DecisionTreeClassifier()
    # my_classifier = KNeighborsClassifier()


    #scaling

    X_train = min_max_scaler(X_train)
    X_test = min_max_scaler(X_test)

    my_classifier = OwnKNN()
    my_classifier.fit(X_train, y_train)

    predictions = my_classifier.predict(X_test)

    print(accuracy_score(y_test, predictions))



