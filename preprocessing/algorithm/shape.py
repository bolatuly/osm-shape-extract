class Shape(object):

    @property
    def center_point(self):
        return self._center_point

    @property
    def area(self):
        return self._area

    # This allows the property to be set
    @area.setter
    def area(self, area):
        self._area = area

    @property
    def ig(self):
        return self._ig

    # This allows the property to be set
    @ig.setter
    def ig(self, ig):
        self._ig = ig

    def __init__(self, center_point, area):
        self._area = area
        self._center_point = center_point

    def __init__(self, center_point, area, ig):
        self._area = area
        self._center_point = center_point
        self._ig = ig