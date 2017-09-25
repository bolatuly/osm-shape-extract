import numpy as np
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("../data/south_korea_buildings.csv", header = 0)

    print(df.head(3))
    print(df.shape) #number of rows and columns

    print(df['type'].unique()) #list of unique values for 'type'
    print(df["type"].value_counts()) #count values for 'type'

