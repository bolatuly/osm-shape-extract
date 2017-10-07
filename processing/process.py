import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from pandas.plotting import andrews_curves
from pandas.plotting import radviz
from sklearn import tree

if __name__ == '__main__':
    df = pd.read_csv("../data/south_korea_buildings.csv", header=0)
    print(df.head(3))
    print(df.shape)  # number of rows and columns

    print(df['type'].unique())  # list of unique values for 'type'
    print(df["type"].value_counts())  # count values for 'type'
    df = df.drop(["Unnamed: 0"], axis=1)
    df = df.drop(["id"], axis=1)
    print(df.shape)
    # print(df.describe())

    # df.boxplot()

    # df['compactness'].plot.hist(bins=50, figsize=(40,15))

    # display andrew curves
    # plt.figure()
    # andrews_curves(df, 'type')

    df = df[df.type != 'no']
    print(df.shape)
    df = df.groupby("type").filter(lambda x: len(x) > 10)
    print(df['type'].unique())
    print(df.shape)

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
    print(df['type'].unique())

    plt.show()
    print(df.head(30))

    columns = ["compactness", "area", "length", "n_nodes"]
    test_idx = [0, 50, 100, 1000, 10000, 100000, 200000]
    labels = df["type"].values
    features = df[list(columns)].values

    # training_data
    train_target = np.delete(labels, test_idx)
    train_data = np.delete(features, test_idx, axis=0)

    # testing_data
    test_target = labels[test_idx]
    test_data = features[test_idx]

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_data, train_target)

    print(test_target)
    predictions = clf.predict(test_data)
    print(predictions)

    # calculate accuracy
    from sklearn.metrics import accuracy_score

    print(accuracy_score(test_target, predictions))
    print(df.describe())

    # plt.figure()
    # radviz(df, 'type')
    # plt.show()
