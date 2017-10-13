import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn import svm
from processing.scaling import min_max_scaler
from scipy import stats
import numpy as np


def sample_size(length):
    if length > 20000:
        return 20000
    else:
        return length * 0.2

if __name__ == '__main__':
    df = pd.read_csv("../data/south_korea_all.csv", header=0)

    df = df.drop(["Unnamed: 0"], axis=1)
    df_p = df.drop(["id"], axis=1)
    print(df_p.shape)  # number of rows and columns
    print(df_p.describe())


    columns = ["compactness", "length"]
    features = df_p[list(columns)].values

    features = min_max_scaler(features)

    #clf = LocalOutlierFactor(n_neighbors=5000, leaf_size=300, n_jobs=5)
    clf = IsolationForest(max_samples=200,n_estimators=200)
    #clf = EllipticEnvelope()
    #clf = svm.OneClassSVM()
    #y_pred = clf.fit_predict(features)
    clf.fit(features)
    #scores_pred = clf.decision_function(features)
    y_pred = clf.predict(features)

    column = ['is_outlier']
    df_res = pd.DataFrame(y_pred, columns=column)

    df_out = pd.merge(df_p, df_res, how='left', left_index=True, right_index=True)
    print(df_out["is_outlier"].value_counts())

    import matplotlib
    from mpl_toolkits.mplot3d import Axes3D

    #plot 3d
    #fig = plt.figure()
    #ax = Axes3D(fig)
    #ax.set_xlabel("compactness")
    #ax.set_ylabel("area")
    #ax.set_zlabel("length")

    # Plot the reduced dimensionality data points
    #ax.scatter(features[:, 0], features[:, 1], zs=features[:, 2], s=4, lw=0, c="g")

    # Plot circles around the predicted outliers
    #ax.scatter(features[y_pred == -1, 0], features[y_pred == -1, 1], zs=features[y_pred == -1, 2],
     #          c="r", s=1, label="predicted outlier")

    #ax.legend()

    #plot 2d
    xx, yy = np.meshgrid(np.linspace(0.0, 1.0, 1200), np.linspace(0.0, 1.0, 1200))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    import random

    s = sample_size(len(features))
    test_idx = random.sample(range(len(features)-1), s)
    display = features[test_idx]
    p_display = y_pred[test_idx]

    plt.title("South Korea Buildings ("+str(s)+" features sample)")
    plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

    b1 = plt.scatter(display[p_display == 1, 0], display[p_display == 1, 1], c='white',
                     s=20, edgecolor='k')

    c = plt.scatter(display[p_display == -1, 0], display[p_display == -1, 1], c='red',
                    s=10, edgecolor='k')
    plt.axis('tight')
    plt.xlim((0.0, 1.0))
    plt.ylim((0.0, 0.2))
    plt.legend([b1, c],
               ["normal",
                "abnormal"],
               loc="upper left")

    plt.savefig('korea_buildings.png', dpi=1200)
    plt.show()
    #df_out.to_csv("../data/result/south_korea_houses_processed.csv", date_format='%Y-%m-%d %H:%M:%S')

