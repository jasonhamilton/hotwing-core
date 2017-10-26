import sys, os
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from hotwing_core import Coordinate, Surface



coordinates = [
        Coordinate(1, 0),
        Coordinate(1, 0), # Dupe
        Coordinate(0.99667, 0.00045),
        Coordinate(0.98707, 0.00195),
        Coordinate(0.97194, 0.00446),
        Coordinate(0.95169, 0.0076),
        Coordinate(0.92645, 0.01112),
        Coordinate(0.89647, 0.01506),
        Coordinate(0.86218, 0.01937),
        Coordinate(0.82405, 0.02394),
        Coordinate(0.78255, 0.02867),
        Coordinate(0.73817, 0.03344),
        Coordinate(0.6914499, 0.03811),
        Coordinate(0.6914499, 0.03811), # Dupe
        Coordinate(0.6914499, 0.03811), # Dupe
        Coordinate(0.64292, 0.04256),
        Coordinate(0.5931, 0.04666),
        Coordinate(0.54254, 0.05029),
        Coordinate(0.49178, 0.05334),
        Coordinate(0.44133, 0.0557),
        Coordinate(0.39172, 0.05727),
        Coordinate(0.34343, 0.058),
        Coordinate(0.29692, 0.0578),
        Coordinate(0.25262, 0.05666),
        Coordinate(0.21095, 0.05456),
        Coordinate(0.17226, 0.05151),
        Coordinate(0.13689, 0.04755),
        Coordinate(0.10513, 0.04275),
        Coordinate(0.07725, 0.03721),
        Coordinate(0.05344, 0.03104),
        Coordinate(0.03388, 0.02439),
        Coordinate(0.01867, 0.01744),
        Coordinate(0.00786, 0.01048),
        Coordinate(0.0015, 0.0039),
        Coordinate(0.0015, 0.0039),
        Coordinate(0, 0),
        Coordinate(0, 0) # Dupe
]

coordinates_no_dupe = [
        Coordinate(1, 0),
        Coordinate(0.99667, 0.00045),
        Coordinate(0.98707, 0.00195),
        Coordinate(0.97194, 0.00446),
        Coordinate(0.95169, 0.0076),
        Coordinate(0.92645, 0.01112),
        Coordinate(0.89647, 0.01506),
        Coordinate(0.86218, 0.01937),
        Coordinate(0.82405, 0.02394),
        Coordinate(0.78255, 0.02867),
        Coordinate(0.73817, 0.03344),
        Coordinate(0.6914499, 0.03811),
        Coordinate(0.64292, 0.04256),
        Coordinate(0.5931, 0.04666),
        Coordinate(0.54254, 0.05029),
        Coordinate(0.49178, 0.05334),
        Coordinate(0.44133, 0.0557),
        Coordinate(0.39172, 0.05727),
        Coordinate(0.34343, 0.058),
        Coordinate(0.29692, 0.0578),
        Coordinate(0.25262, 0.05666),
        Coordinate(0.21095, 0.05456),
        Coordinate(0.17226, 0.05151),
        Coordinate(0.13689, 0.04755),
        Coordinate(0.10513, 0.04275),
        Coordinate(0.07725, 0.03721),
        Coordinate(0.05344, 0.03104),
        Coordinate(0.03388, 0.02439),
        Coordinate(0.01867, 0.01744),
        Coordinate(0.00786, 0.01048),
        Coordinate(0.0015, 0.0039),
        Coordinate(0, 0)
]

short_surface = [
        Coordinate(1, 0), 
        Coordinate(0.64292, 0.04256),
        Coordinate(0.5931, 0.04666),
        Coordinate(0, 0)
]

class TestSurface():
    def test_small_surface(self):
        s = Surface(short_surface)

    def test_remove_duplicate_coordinates(self):
        # make sure same number of coordinates after creation
        # from a list of Coordinates with no duplicates
        s = Surface(coordinates_no_dupe)
        assert len(s.coordinates) == len(coordinates_no_dupe)
        s = Surface(reversed(coordinates_no_dupe))
        assert len(s.coordinates) == len(coordinates_no_dupe)


        # Make sure the duplicates are removed
        s = Surface(coordinates)
        assert len(s.coordinates) == len(coordinates_no_dupe)
        assert s.coordinates == list(reversed(coordinates_no_dupe))
        s = Surface(reversed(coordinates))
        assert len(s.coordinates) == len(coordinates_no_dupe)
        assert s.coordinates == list(reversed(coordinates_no_dupe))

    def test_order_coordinates(self):
        # Make sure the duplicates are removed
        s = Surface(coordinates)
        assert s.coordinates == list(reversed(coordinates_no_dupe))
        s = Surface(reversed(coordinates))
        assert s.coordinates == list(reversed(coordinates_no_dupe))

    def test_left_right_bounds(self):
        coords = [
            Coordinate(0.6, 0  ), 
            Coordinate(0.4, 0.2),
            Coordinate(0.2, 0.3),
            Coordinate(0.1, 0.1)
        ]
        s = Surface(coords)
        assert s.right == coords[0]
        assert s.left == coords[-1]
        assert s.bounds == (Coordinate(0.1,0),Coordinate(0.6,0.3))

        # reverse coords and try again
        s = Surface(list(reversed(coords)))
        assert s.right == coords[0]
        assert s.left == coords[-1]
        assert s.bounds == (Coordinate(0.1,0),Coordinate(0.6,0.3))

    def test_length(self):
        coords = [
            Coordinate(0.1, 0), 
            Coordinate(0.3, 0),
            Coordinate(0.7, 0),
            Coordinate(0.9, 0)
        ]
        s = Surface(coords)
        assert s.length == 0.8

        coords = [
            Coordinate(0,0.1), 
            Coordinate(0,0.3),
            Coordinate(0,0.7),
            Coordinate(0,0.9)
        ]
        s = Surface(coords)
        assert s.length == 0.8

        coords = [
            Coordinate(0.0,0.0),
            Coordinate(0.4,0.3), 
            Coordinate(0.8,0.6),
            Coordinate(1.2,0.9),

        ]
        s = Surface(coords)
        assert s.length == 3*0.5

    def test_offset_around_profile(self):
        pass

    def test_translate(self):
        offset_x = 5
        offset_y = 11
        offset_coord = Coordinate(5,11)
        coords = [
            Coordinate(0.0,0.0),
            Coordinate(0.4,0.3), 
            Coordinate(0.8,0.6),
            Coordinate(1.2,0.9),

        ]
        s1 = Surface(coords)
        s2 = Surface.translate(s1, offset_coord)
        for i in range(len(s2.coordinates)):
            orig_coord = coords[i]
            surface_coord = s2.coordinates[i]
            assert orig_coord.x+offset_x == surface_coord.x
            assert orig_coord.y+offset_y == surface_coord.y

        #test offset with invalid object
        with pytest.raises(TypeError):
            Surface.translate(s2, 1)

        # try using +/- operators
        s3 = s1+offset_coord
        assert s2 == s3

        s4 = s3-offset_coord
        assert s1 == s4


    def test_scale(self):
        coords = [
            Coordinate(0.0,0.1),
            Coordinate(0.4,0.2), 
            Coordinate(0.8,0.4),
            Coordinate(1.2,0.6),
        ]
        scale = 5
        s = Surface(coords)
        s1 = Surface.scale(s,scale)
        s2 = s*5

        # scaling by method or multiplying should yield same values
        for i in range(len(s.coordinates)):
            assert s1.coordinates[i] == s2.coordinates[i]

        # validate coordinates scaled correctly
        for i in range(len(s.coordinates)):
            c_x = coords[i].x
            c_y = coords[i].y
            s1.coordinates[i] == Coordinate(c_x*scale,c_y*scale)

    def trim_surface(self,coords,l,r,type_="method"):
        s = Surface(coords)
        if type_ == "method":
            t = Surface.trim(s,l,r)
        elif type_ == "slice":
            t = s[l:r]
        if l:
            assert t.left.x == l
        else:
            assert t.left.x == s.left.x
        if r:
            assert t.right.x == r
        else:
            assert t.right.x == s.right.x

    def test_trim(self):
        # trim both sides
        self.trim_surface(coordinates, 0.25, 0.75)
        self.trim_surface(coordinates, 0.25, 0.75, "slice")

        # trim right side only
        self.trim_surface(coordinates, None, 0.75)
        self.trim_surface(coordinates, None, 0.75, "slice")

        # trim left side only
        self.trim_surface(coordinates, 0.25, None)
        self.trim_surface(coordinates, 0.25, None, "slice")

        # don't trim either
        self.trim_surface(coordinates, None, None)
        self.trim_surface(coordinates, None, None, "slice")

        s = Surface(coordinates)
        with pytest.raises(NotImplementedError):
            s[1]

    def test_equality(self):
        coords1 = [
            Coordinate(0.0,0.0),
            Coordinate(0.4,0.4), 
            Coordinate(0.8,0.8),
            Coordinate(1.2,1.2),
        ]
        coords2 = [
            Coordinate(0.0,0.0),
            Coordinate(0.5,0.1), 
            Coordinate(0.8,0.8),
            Coordinate(1.2,1.2),
        ]

        s1 = Surface(coordinates)
        s2 = Surface(coordinates_no_dupe)
        s3 = Surface(short_surface)
        # same length different coords
        s4 = Surface(coords1)
        s5 = Surface(coords2)

        assert s1 == s2
        assert s1 != s3
        assert not s1 == s3
        assert not s4 == s5
        with pytest.raises(NotImplementedError):
            s1 == 1
        with pytest.raises(NotImplementedError):
            s2 != "s"
        
    def test_interpolate(self):
        # Straignt line x=y
        coords = [
            Coordinate(0.0,0.0),
            Coordinate(0.4,0.4), 
            Coordinate(0.8,0.8),
            Coordinate(1.2,1.2),
        ]
        s = Surface(coords)
        for i in range(100):
            val = i/100.0
            result = s.interpolate(val)
            assert result == Coordinate(val,val)

        # horizontal line y=0.5
        coords = [
            Coordinate(0.0,0.5),
            Coordinate(0.4,0.5), 
            Coordinate(0.8,0.5),
            Coordinate(1.2,0.5),
        ]
        s = Surface(coords)
        for i in range(100):
            val = i/100.0
            result = s.interpolate(val)
            assert result == Coordinate(val,0.5)
        
    def test_rotate(self):
        coords = [
            Coordinate(0.0,0.0),
            Coordinate(0.4,0.2), 
            Coordinate(0.8,0.4),
            Coordinate(1.2,0.6),
        ]

        s = Surface(coords)
        o = Coordinate(0,0)
        a = 90
        r = Surface.rotate(o,s,a)
        r.coordinates[0] == Coordinate(0,0)
        r.coordinates[1] == Coordinate(-0.2,0.4)
        r.coordinates[2] == Coordinate(-0.8,-0.4),
        r.coordinates[3] == Coordinate(0.6,-1.2)

    def test_interpolate_new_surface(self):
        coords = [
            Coordinate(0.0,0.0),
            Coordinate(0.4,0.2), 
            Coordinate(0.8,0.4),
            Coordinate(1.2,0.6),
        ]
        # make same surface
        s1 = Surface(coords)
        s2 = Surface(coords)
        length = 500
        s3 = Surface.interpolate_new_surface(s1,s2,10,3, length)

        assert len(s3.coordinates) == length

        # test each original coordinate to see if it's the same
        # doesn't validate correctly on an interpolated foil but
        # works on our linear example
        for c in s1.coordinates:
            assert c == s3.interpolate(c.x)
        # also only works on our contrived example
        for i in range(len(s1.coordinates)-1):
            c1 = coords[i]
            c2 = coords[i+1]
            c3 = c1+c2
            c3 = c3*0.5
            assert s1.interpolate(c3.x) == s3.interpolate(c3.x)

    def test_offset(self):
        ## test for 0 slope
        coords = [
            Coordinate(0.2,0.0),
            Coordinate(0.4,0.0), 
            Coordinate(0.6,0.0),
            Coordinate(1.2,0.6),
        ]
        s1 = Surface(coords)
        offset = 1.125
        s2 = Surface.offset_around_surface(s1,offset)

    def test_write_file(self):
        filename="my_test_output_file.txt"
        s = Surface(coordinates)
        if os.path.isfile(filename):
                os.remove(filename)

        s.to_file(filename)
        assert os.path.isfile(filename)
        os.remove(filename)

    def test_str(self):
        s = Surface(coordinates)
        assert len(str(s)) > 0

    def test_add_sub(self):
        s = Surface(coordinates)
        with pytest.raises(NotImplementedError):
            s + 1
        with pytest.raises(NotImplementedError):
            s - 1
