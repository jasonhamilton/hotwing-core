from .coordinate import Coordinate
from .utils import isect_line_plane_v3
import math


class Surface():
    """
    A connected group of coordinates connected by lines that make up a top or bottom
    surface of an airfoil.

    Args:
        coordinates: list of Coordinates
                        ASSUMED TO BE IN EITHER ASCENDING OR DESCENDING
                        ORDER BASED ON X VALUES
    """

    def __init__(self, coordinates=[]):
        self.coordinates = coordinates
        self._remove_duplicate_coordinates()
        self._order_coordinates()

    @property
    def min(self):
        """
        Gets the left most Coordinate

        Returns:
            Coordinate
        """
        return self.coordinates[0]

    @property
    def max(self):
        """
        Gets the right-most Coordinate

        Returns:
            Coordinate
        """
        return self.coordinates[-1]

    @property
    def bounds(self):
        """
        Gets the bounding box of the Surface

        Returns:
            (min,max) - tuple of Coordinates with the min xy and the max xy value
        """
        min_x = min([c.x for c in self.coordinates])
        min_y = min([c.y for c in self.coordinates])
        max_x = max([c.x for c in self.coordinates])
        max_y = max([c.y for c in self.coordinates])
        return (Coordinate(min_x, min_y), Coordinate(max_x, max_y))

    @property
    def length(self):
        """
        Calculates the total length around the area of the surface

        Returns:
            Float
        """
        total_len = 0
        coord_count = len(self.coordinates)
        for i in range(coord_count - 1):
            a = self.coordinates[i]
            b = self.coordinates[i + 1]
            dist = Coordinate.calc_dist(a, b)
            total_len += dist
        return total_len

    @classmethod
    def offset_around_profile(cls, surface, offset):
        """
        Offsets the surface around the current surface - evaluates relative angle at each point and
        expands/contracts the surface around these angles.

        Args:
            surface: Surface to offset
            offset: Float - distance to offset from surface - positive value offsets upwards, negative
                            value offsets downwards.

        Returns:
            Surface: new Surface with the offset applied
        """
        coordinates = surface.coordinates
        new_coords = []
        coord_count = len(coordinates)
        for i in range(coord_count):
            # get slope to use - first, last and others use different slope
            # calcs
            if i == 0:
                slope_next = Coordinate.calc_slope(
                    coordinates[i], coordinates[i + 1])
                slope = slope_next
            elif i == coord_count - 1:
                slope_prev = Coordinate.calc_slope(
                    coordinates[i - 1], coordinates[i])
                slope = slope_prev
            else:
                slope_next = Coordinate.calc_slope(
                    coordinates[i], coordinates[i + 1])
                slope_prev = Coordinate.calc_slope(
                    coordinates[i - 1], coordinates[i])
                slope = (slope_next + slope_prev) / 2
            try:
                slope_inv = -1.0 / slope
            except ZeroDivisionError:
                slope_inv = 0
            b = offset / math.sqrt(slope_inv * slope_inv + 1)
            a = slope_inv * b

            if slope_inv < 0:
                y = coordinates[i].y - a
                x = coordinates[i].x - b
            else:
                y = coordinates[i].y + a
                x = coordinates[i].x + b
            new_coords.append(Coordinate(x, y))
        return cls(new_coords)

    @classmethod
    def offset_xy(cls, surface, offset):
        """
        Offsets the surface using the x and y values in the coordinate

        Args:
            surface : Surface to offset
            offset: Coordinate object containing the x and y values to offset

        Returns:
            Surface: new Surface with the offset applied
        """
        if not isinstance(offset, Coordinate):
            raise TypeError
        new_coords = []
        for c in surface.coordinates:
            new_coords.append(c + offset)
        return cls(new_coords)

    @classmethod
    def scale_to_width(cls, surface, width):
        """
        Scales a Surface to a specified width.  The new surface will start at 0 and go to the width

        Args:
            surface : Surface to offset
            width: Float - width of new surface

        Returns:
            Surface: new Surface scaled to the new width
        """

        # offset min x to 0
        min_, max_ = surface.bounds
        s = Surface.offset_xy(surface, Coordinate(-min_.x,0))

        _, max_ = s.bounds
        scale_factor = width * 1.00 / max_.x
        new_coords = []
        for c in s.coordinates:
            new_coords.append(c * scale_factor)
        return cls(new_coords)

    @classmethod
    def trim(cls, surface, x_min=None, x_max=None):
        """
        Trims a Surface to new starting and ending x values.

        IMPORTANT - If you specify a value smaller than the min or larger than the max, by default
        those values will be interpolated and may actually make the width of the surface larger.

        Args:
            surface : Surface to trim
            x_min (optional): Float - x value to make the left cut on - if not
                                        specified, no cut will be made on this side
            x_max (optional): Float - x value to make the right cut on - if not
                                        specified, no cut will be made on this side
        Returns:
            Surface: new Surface trimmed to the min and max x values
        """
        if x_min is None and x_max is None:
            return surface

        # extract the points between the cut points
        trim_left = 0
        trim_right = len(surface.coordinates) - 1

        if not x_min is None:
            for i, c in enumerate(surface.coordinates):
                if c.x >= x_min:
                    trim_left = i
                    break

        if not x_max is None:
            for i, c in enumerate(surface.coordinates):
                if c.x >= x_max:
                    trim_right = i
                    break

        new_coords = surface.coordinates[trim_left:trim_right]

        # now we need to insert new coordinates on the left and right at the
        # cut points
        if not x_min is None and not new_coords[0].x == x_min:
            new_coords.insert(0, surface.interpolate(x_min))

        if not x_max is None and not new_coords[-1].x == x_max:
            new_coords.append(surface.interpolate(x_max))

        return cls(new_coords)

    @classmethod
    def interpolate_new_surface(
            cls, s1, s2, dist_between, dist_interp, points=200):
        """
        Creates a new Surface interpolated from two other Surfaces.

        Args:
            s1: Surface - first surface to interpolate from
            s2: Surface - second surface to interpolate from
            dist_between: Float - Distance between profiles
            dist_interp: Float - Distance from s1 where new surface should be interpolated
            points: Int - Number of points to use for interpolating the new surface

        Returns:
            Surface - New Surface interpolated from s1 and s2
        """

        def interpolate_between_points(c1, c2, dist_between, dist_interp):

            interp_plane = (dist_interp, 0, 0)
            p_no = (1, 0, 0)  # interp_plane normal -- directon of plane
            # position of ribs
            c1_3d = (0, c1.x * 1.0, c1.y * 1.0)
            c2_3d = (dist_between * 1.0, c2.x * 1.0, c2.y * 1.0)
            a = isect_line_plane_v3(c1_3d, c2_3d, interp_plane, p_no)
            return a[-2:]

        new_coords = []
        for i in range(points + 1):
            pct = i * 1.0 / points
            c1 = s1.interpolate_around_profile_dist_pct(pct)
            c2 = s2.interpolate_around_profile_dist_pct(pct)
            res = interpolate_between_points(c1, c2, 10, 5)
            new_coords.append(Coordinate(res[0], res[1]))
        return cls(new_coords)

    @classmethod
    def rotate(cls, origin, surface, angle):
        """
        Rotates a surface around a certain point.

        Args:
            origin: Coordinate object that defines the point to rotate surface around
            surface: Surface object to rotate
            angle: Float - degrees to rotate surface.

        Returns:
            Surface - New rotated Surface
        """
        new_coords = []
        for c in surface.coordinates:
            new_coords.append(Coordinate.rotate(origin, c, angle))
        return cls(new_coords)

    def interpolate(self, x):
        """
        Interpolates the Y position for a given value of X.

        Method uses linear interpolation between two points.  If the point lies outside of the
        coordinates, the line is interpolated based on the closest two points extended outwards.

        Args:
            x: Float - value of x where we want to interpolate
        Returns:
            Coordinate - (x,y) - original x value provided and solved y value
        """
        coordinates = self.coordinates
        coord_count = len(coordinates)
        row = 0

        if x >= coordinates[-1].x:
            # Get Last 2 Coordinates
            coord_a = coordinates[-2]
            coord_b = coordinates[-1]
            slope = Coordinate.calc_slope(coord_a, coord_b)
            coord = coord_b

        elif x <= coordinates[0].x:
            # Get First 2 Coordinates
            coord_a = coordinates[0]
            coord_b = coordinates[1]
            slope = Coordinate.calc_slope(coord_a, coord_b)
            coord = coord_a

        else:
            # Get Coordintes Bounding Point
            for i in range(coord_count):
                if coordinates[i].x >= x:
                    row = i - 1
                    break
            coord_a = coordinates[row]
            coord_b = coordinates[row + 1]
            slope = Coordinate.calc_slope(coord_a, coord_b)
            coord = coord_a

        change_in_x = x - coord.x
        change_in_y = slope * change_in_x

        return Coordinate(coord.x + change_in_x, coord.y + change_in_y)

    def interpolate_around_profile_dist_pct(self, pct):
        """
        Finds the x-y position along the surface of the profile at a specified PERCENTAGE value of
        the total distance around the surface of the profile, starting from the left-most coordinate.

        Args:
            pos: Float - value to find of distance around profile

        Returns:
            Coordinate - interpolated coordinate at position
        """
        return self.interpolate_around_profile_dist(self.length * pct)

    def interpolate_around_profile_dist(self, pos):
        """
        Finds the x-y position along the surface of the profile at a specified DISTANCE around the
        surface of the profile, starting from the left-most coordinate.

        Args:
            pos: Float - value to find of distance around profile

        Returns:
            Coordinate - interpolated coordinate at position
        """
        total_len = 0
        coord_count = len(self.coordinates)
        last_coord_pos = coord_count
        for i in range(coord_count - 1):
            a = self.coordinates[i]
            b = self.coordinates[i + 1]
            dist = Coordinate.calc_dist(a, b)
            # find point just to the just before going over max length
            if total_len + dist > pos:
                last_coord_pos = i
                break
            total_len += dist

        #     dist left
        #                  c2(x,y)
        #                 /|
        #                / |
        #               /  |
        #            c /   |
        #             /    |   a
        #            /     |
        #           /      |
        #          /       |
        #  c1(x,y) ---------
        #             b

        dist_remaining = pos - total_len

        if coord_count == last_coord_pos:
            # the last coordinate, so we need to treat it differently
            c1 = self.coordinates[last_coord_pos - 2]
            c2 = self.coordinates[last_coord_pos - 1]

            slope = Coordinate.calc_slope(c1, c2)

            b = dist_remaining / math.sqrt(slope * slope + 1)
            a = b * slope

            x = c2.x + b
            y = c2.y + a

        else:
            c1 = self.coordinates[last_coord_pos]
            c2 = self.coordinates[last_coord_pos + 1]

            slope = Coordinate.calc_slope(c1, c2)

            b = dist_remaining / math.sqrt(slope * slope + 1)
            a = b * slope

            x = c1.x + b
            y = c1.y + a

        return Coordinate(x, y)

    def _remove_duplicate_coordinates(self):
        """
        Removes any duplicates from the coordinates attribute
        ASSUMES DUPLICATES ARE NEXT TO EACH OTHER IN LIST!
        """
        unique = []
        for i, c in enumerate(self.coordinates):
            if i == 0:
                unique.append(c)
            else:
                if c != unique[-1]:
                    unique.append(c)
        self.coordinates = unique

    def _order_coordinates(self):
        """
        Reverses the direction of the coordinates attribute, if necessary to put the coordinates
        in ascending order.
        """
        ascending_count = 0
        descending_count = 0
        coord_count = len(self.coordinates)
        for i in range(coord_count - 1):
            c1 = self.coordinates[i]
            c2 = self.coordinates[i + 1]
            if c2.x == c1.x:
                pass
            elif c2.x > c1.x:
                ascending_count += 1
            else:
                descending_count += 1
        if descending_count > ascending_count:
            # list is descending, need to reverse
            self.coordinates = list(reversed(self.coordinates))

    def __str__(self):
        out = ""
        for c in self.coordinates:
            out += c.__str__()
            out += "\n"
        return out
