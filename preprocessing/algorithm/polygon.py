import math

from preprocessing.algorithm.shape import Shape
from preprocessing.algorithm.mbr import MBR


class Polygon(object):

    @classmethod
    def compute(cls, polygon):

        cls.rectangles_list = []
        cls.triangles_list = []

        cls.area = 0.0
        cls.centroid = []
        cls.ig = 0.0

        coordinates = cls.translate_and_scale(polygon)

        for i in range(len(coordinates)-1):
            coordinate_one = coordinates[i]
            coordinate_two = coordinates[i + 1]

            cls.add_triangle(first=coordinate_one, second=coordinate_two)
            cls.add_rect(first=coordinate_one, second=coordinate_two)

        cls.set_area(coordinates)
        if cls.area < 0:
            cls.fix_negative_area(coordinates)
        cls.set_centroid(coordinates)
        cls.set_ig(coordinates)
        return cls.area * cls.area / (2 * math.pi * cls.ig)

    @classmethod
    def fix_negative_area(cls, coordinates):
        for i in range(len(coordinates)-1):
            cls.triangles_list[i].area *= -1;
            cls.triangles_list[i].ig *= -1;
            cls.rectangles_list[i].area *= -1;
            cls.rectangles_list[i].ig *= -1;
        cls.area *= -1;

    @classmethod
    def translate_and_scale(cls, polygon):

        coordinates = list(polygon.exterior.coords)
        mbr = MBR()
        mbr.calc(coordinates)

        east = math.radians(mbr.east)
        west = math.radians(mbr.west)
        north = math.radians(mbr.north)
        south = math.radians(mbr.south)

        coordinates = cls.degree_to_rad(coordinates)

        height = 1000.0
        width = 1000.0 * (east - west) / (north - south)

        y_min = cls.merc_y(south)
        y_max = cls.merc_y(north)
        x_factor = width / (east - west)
        y_factor = height / (y_max - y_min)

        for i in range(len(coordinates)):
            x = (coordinates[i][0] - west) * x_factor
            y = cls.merc_y(coordinates[i][1])
            y = (y_max - y) * y_factor

            temp = list(coordinates[i])
            temp[0] = x
            temp[1] = y
            coordinates[i] = tuple(temp)

        return tuple(coordinates)

    @classmethod
    def merc_y(cls, lat):
        half_lat = lat/2
        tangent = math.tan(half_lat + math.pi/4)
        return math.log(tangent)

    @classmethod
    def degree_to_rad(cls, coordinates):
        for i in range(len(coordinates)):
            temp = list(coordinates[i])
            temp[0] = math.radians(temp[0])
            temp[1] = math.radians(temp[1])
            coordinates[i] = tuple(temp)
        return coordinates

    @classmethod
    def set_ig(cls, coordinates):
        ig = 0.0
        for i in range(len(coordinates)-1):
            ig += cls.triangles_list[i].ig

            ig += cls.square_distance(start=(cls.center_point[0], cls.center_point[1]),
                                      end=(list(map(float, cls.triangles_list[i].center_point[0]))[0],
                                           list(map(float, cls.triangles_list[i].center_point[1]))[0])) * \
                  cls.triangles_list[i].area
            ig += cls.rectangles_list[i].ig
            ig += cls.square_distance(start=(cls.center_point[0], cls.center_point[1]),
                                      end=(list(map(float, cls.rectangles_list[i].center_point[0]))[0],
                                           list(map(float, cls.rectangles_list[i].center_point[1]))[0])) * \
                  cls.rectangles_list[i].area

        cls.ig = ig

    @classmethod
    def set_centroid(cls, coordinates):
        x = 0.0
        y = 0.0
        for i in range(len(coordinates)-1):
            x += list(map(float, cls.rectangles_list[i].center_point[0]))[0] * cls.rectangles_list[i].area
            x += list(map(float, cls.triangles_list[i].center_point[0]))[0] * cls.triangles_list[i].area
            y += list(map(float, cls.rectangles_list[i].center_point[1]))[0] * cls.rectangles_list[i].area
            y += list(map(float, cls.triangles_list[i].center_point[1]))[0] * cls.triangles_list[i].area

        x /= cls.area
        y /= cls.area
        cls.center_point = [x, y]

    @classmethod
    def set_area(cls, coordinates):
        area = 0.0
        for i in range(len(coordinates)-1):
            area += cls.triangles_list[i].area + cls.rectangles_list[i].area
        cls.area = area

    @classmethod
    def add_triangle(cls, first, second):
        center = [[(first[0] + 2 * second[0]) / 3], [(2 * first[1] + second[1]) / 3]]
        area = (second[0] - first[0]) * (second[1] - first[1]) / 2
        ig = area * cls.square_distance(first, second) / 18

        tr = Shape(area=area, center_point=center, ig=ig)
        cls.triangles_list.append(tr)

    @classmethod
    def add_rect(cls, first, second):
        area = (second[0] - first[0]) * first[1]
        center = [[(first[0] + second[0]) / 2], [first[1] / 2]]
        ig = area * (math.pow(second[0] - first[0], 2) + math.pow(first[1], 2)) / 12

        rect = Shape(area=area, center_point=center, ig=ig)
        cls.rectangles_list.append(rect)

    @classmethod
    def square_distance(cls, start, end):
        return math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2)

