import math


class Coordinate():
    """
    2 Dimensional X-Y coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def calc_slope(cls, a, b):
        """
        Calculates the slope between two coordinates

        Args:
            a : Coordinate
            b : Coordinate
        Returns:
            Float: slope between c1 and c2
        """
        slope = (a.y-b.y)*1.0 / (a.x-b.x)
        return slope

    @classmethod
    def calc_dist(cls, a, b):
        """
        Calculates the distance between two coordinates

        Args:
            a : Coordinate
            b : Coordinate
        Returns:
            Float: distance between c1 and c2

        """
        dist = math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
        return dist

    @classmethod
    def rotate(cls, origin, coordinate, angle):
        """
        Rotates a coordinate around a certain point.

        Args:
            origin: Coordinate object that defines the point to rotate coordinate around
            coordinate: coordinate object to rotate
            angle: Float - degrees to rotate Coordinate.

        Returns:
            Coordinate - New rotated Profile
        """
        angle = math.radians(angle)
        ox = origin.x
        oy = origin.y
        px = coordinate.x
        py = coordinate.y

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return cls(qx, qy)

    def __str__(self):
        return "%5f, %5f" % (self.x, self.y)

    def __repr__(self):
        return "Coordinate: %5f, %5f" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __add__(self, other):
        return Coordinate(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Coordinate(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Coordinate(self.x*other.x, self.y*other.y)
        return Coordinate(self.x*other, self.y*other)


if __name__ == "__main__":
    c1 = Coordinate(0.213, 0.552)
    c2 = Coordinate(1, 2)

    print(c1)
    print(c1 == c2)
