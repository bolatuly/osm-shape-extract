import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor

if __name__ == '__main__':
    df = pd.read_csv("../data/south_korea_houses.csv", header=0)

    df = df.drop(["Unnamed: 0"], axis=1)
    df_p = df.drop(["id"], axis=1)
    print(df_p.shape)  # number of rows and columns
    print(df_p.describe())

    columns = ["compactness", "area", "length", "n_nodes"]
    features = df_p[list(columns)].values

    from processing.scaling import min_max_scaler

    features = min_max_scaler(features)

    clf = LocalOutlierFactor(n_neighbors=5000, leaf_size=300, n_jobs=5)
    y_pred = clf.fit_predict(features)

    column = ['is_outlier']
    df_res = pd.DataFrame(y_pred, columns=column)

    df_out = pd.merge(df, df_res, how='left', left_index=True, right_index=True)
    print(df_out["is_outlier"].value_counts())
    df_out.to_csv("../data/result/south_korea_buildings_processed.csv", date_format='%Y-%m-%d %H:%M:%S')