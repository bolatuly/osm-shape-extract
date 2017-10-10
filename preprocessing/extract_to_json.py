import osmium
import shapely.wkb as wkblib
from preprocessing.algorithm.polygon import Polygon
from geojson import FeatureCollection
import pandas as pd
import geojson

wkbfab = osmium.geom.WKBFactory()


class BuildingHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.buildings = []
        self.exception_counter = 0

    def area(self, a):
        if 'building' in a.tags:
            #if a.tags['building'] == 'apartments':
                try:
                    wkb = wkbfab.create_multipolygon(a)
                    poly = wkblib.loads(wkb, hex=True)
                    g2= geojson.Feature(id=a.id, geometry=poly, properties={})
                    self.buildings.append(g2)
                except:
                    self.exception_counter += 1


if __name__ == '__main__':
    h = BuildingHandler()
    h.apply_file("../data/south-korea-latest.osm.pbf")
    feature_collection = FeatureCollection(h.buildings)
    print("Objects with broken geometry: " + str(h.exception_counter))
    import json
    with open('../data/result/south_korea_all_geojson.json', 'w') as f:
        json.dump(feature_collection, f, ensure_ascii=False)
