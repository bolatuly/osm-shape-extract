class MBR(object):

    @property
    def east(self):
        return self._east

    @property
    def north(self):
        return self._north

    @property
    def west(self):
        return self._west

    @property
    def south(self):
        return self._south

    # This allows the property to be set
    @east.setter
    def east(self, east):
        self._east = east

    @north.setter
    def north(self, north):
        self._north = north

    @west.setter
    def west(self, west):
        self._west = west

    @south.setter
    def south(self, south):
        self._south = south

    def calc(self, coordinates):
        for i in range(len(coordinates)-1):
            if coordinates[i][0] < float(self.west):
                self._west = coordinates[i][0]
            if coordinates[i][0] > float(self.east):
                self._east = coordinates[i][0]
            if coordinates[i][1] < float(self.south):
                self._south = coordinates[i][1]
            if coordinates[i][1] > float(self.north):
                self._north = coordinates[i][1]

    def __init__(self):
        self._east = -180
        self._north = -180
        self._west = 180
        self._south = 180
