import osmium
import shapely.wkb as wkblib
from preprocessing.algorithm.polygon import Polygon
import pandas as pd

wkbfab = osmium.geom.WKBFactory()


class BuildingHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.buildings = []
        self.counter = 0
        self.exception_counter = 0

    def print_counter(self):
        if self.counter % 10000 == 0:
            print(self.counter)

    def area(self, a):
        if 'building' in a.tags:
            if a.tags['building'] == 'apartments':
                try:
                    wkb = wkbfab.create_multipolygon(a)
                    poly = wkblib.loads(wkb, hex=True)
                    polygon_type = Polygon
                    for polygon in poly:
                        mon = polygon_type.compute(polygon=polygon)
                    self.buildings.append([a.id, mon, polygon.area, polygon.length, len(polygon.exterior.coords)])
                    self.counter += 1
                    self.print_counter()
                except:
                    self.exception_counter += 1;


if __name__ == '__main__':
    h = BuildingHandler()
    h.apply_file("../data/south-korea-latest.osm.pbf")
    colnames = ['id', 'compactness', 'area', 'length', 'n_nodes']
    elements = pd.DataFrame(h.buildings, columns=colnames)
    elements.to_csv("../data/south_korea_apartments.csv", date_format='%Y-%m-%d %H:%M:%S')
    print(elements.head(10))
    print("Total objects: " + str(h.counter))
    print("Objects with broken geometry: " + str(h.exception_counter))
