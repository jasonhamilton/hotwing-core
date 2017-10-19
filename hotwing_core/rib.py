from __future__ import division
from .profile import Profile
from .utils import isect_line_plane_v3
from .coordinate import Coordinate


class Rib():
    """
    A Rib can be thought of as a profile-view of a wing that's sliced vertically from front to back.  The rib contains
    attributes necessary to create the shape of the airfoil and position it in 2D space.  A Rib starts with a Profile object,
    which is manipulated to create a Rib. 

    Args:
        foil_data (Profile or object that can initialize a Profile object): this should contain X
                coordinates between 0 and 1 only.  The foil should have the front facing left.

        scale (Float): Length of the rib.  The airfoil will be scaled by this value.
        xy_offset (Coordinate): Distance to offset profile
        top_sheet (Float): Thickness of top sheet - the top of the rib will be offset inward by this 
                           amount in order to account for a sheeting allowance.  The idea is that once
                           the sheeting is applied, the final shape will be accurate to the airfoil.
        bottom_sheet (Float): Thickness of the bottom sheet - similar to the top_sheet but on the bottom
        front_stock (Float): Size of the front stock.  The rib will be cut horizontally at this diistance back 
                             from the leading edge. This will allow for stock (wood or other material) to be 
                             applied and then shaped to the shape of the airfoil.
        tail_stock (Float): Size of the tail stock.  This is similar to the front_stock, except on the tail.
        rotation (Float):   Degrees to rotate the rib for washout or washin.  A positive value will rotate the
                            rib clockwise, which will raise the front of the foil.
        rotation_pos (Float): Position to rotate the foil in terms of chord length.  A value of 50% will rotate the
                              foil around a point 50% from the tip.  A value of 0.25% will rotate the value 25% from
                              the tip.
    
    :ivar foil_definition: foil_definition
    :ivar scale: scale
    :ivar xy_offset: xy_offset
    :ivar top_sheet: top_sheet
    :ivar bottom_sheet: bottom_sheet
    :ivar front_stock: front_stock
    :ivar tail_stock: tail_stock
    :ivar rotation: rotation
    :ivar rotation_pos: rotation_pos
    """
    
    def __init__(self, foil_data, scale=None, xy_offset=None, top_sheet=0,
                 bottom_sheet=0, front_stock=0, tail_stock=0, rotation=0, rotation_pos=0.5):
        if isinstance(foil_data, Profile):
            self.foil_definition = foil_data
        else:
            self.foil_definition = Profile(foil_data)
        self.scale = scale
        self.xy_offset = xy_offset
        self.top_sheet = top_sheet
        self.bottom_sheet = bottom_sheet
        self.front_stock = front_stock
        self.tail_stock = tail_stock
        self.rotation = rotation
        self.rotation_pos = rotation_pos

    @property
    def airfoil_profile(self):
        """
        A copy of the scaled and offset airfoil before sheeting.  This represents the surface of the wing
        at the Rib's position.  This includes the entire foil and doesn't exclude the front_stock or tail_stock.
        """
        p = Profile.copy(self.foil_definition)
        if not self.scale is None:
            p = Profile.scale(p, self.scale)
        if not self.rotation == 0:
            x_bounds = p.x_bounds
            x_len = x_bounds[1] - x_bounds[0]
            mid_point = x_bounds[0] + x_len * self.rotation_pos
            p = Profile.rotate(Coordinate(mid_point, 0), p, -self.rotation)
        if self.xy_offset:
            p = Profile.translate(p, self.xy_offset)
        return p

    @property
    def profile(self):
        """
        A copy of the rib profile after scaling and offsets.  This represents the actual profile of the rib.
        This includes the entire rib surface and doesn't exclude the front_stock or tail_stock.
        """
        p = self.airfoil_profile
        if self.top_sheet or self.bottom_sheet:
            p = Profile.offset_around_profiles(
                p, -self.top_sheet, -self.bottom_sheet)
        return p

    @classmethod
    def interpolate_new_rib(cls, r1, r2, dist_between,
                            dist_interp, points=200):
        """
        Interpolate a new rib based on two others.

        Args:
            r1 (Rib): First Rib
            r2 (Rib): Second Rib
            dist_between (Float): Distance between the ribs of the panel we want to interpolate
            dist_interp (Float): Distance from the left side at which we perform the interpolation.
            points (Int): Number of points to use on each (top/bottom) surface we interpolate.
        """
        p = Profile.interpolate_new_profile(
            r1.airfoil_profile, r2.airfoil_profile, dist_between, dist_interp, points)
        rib = cls(p)
        rib.top_sheet = r1.top_sheet
        rib.bottom_sheet = r1.bottom_sheet
        rib.front_stock = r1.front_stock
        rib.tail_stock = r1.tail_stock
        return rib
