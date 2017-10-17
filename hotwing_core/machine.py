from __future__ import division
from .utils import isect_line_plane_v3
from .profile import Profile
from .coordinate import Coordinate
from .gcode import Gcode
from .cutting_strategies import *
import logging
logging.getLogger(__name__)

class Machine():
    """
    The Machine class is a representation of a foam cutting machine and goes
    through the series of cuts required to create a complete cutting path.

    The machine takes a Profile object and generates the code to cut that
    profile.

    Args:
        width (Float): length of the machine's hotwire cutter
        kerf (Float):
            Allowance for the hotwire's cutter.  This includes the radius of 
            the wire plus any additional allowance for melted foam from direct
            or radiant heat.
        profile_points (Int): 
            Number of points used when interpolating profiles.  This is the
            number for each (top and bottom) surface of a Profile.
        output_profile_images (Boolean): 
            If true, images of the profiles during the manipulation process 
            will be created.  Used is for debugging purposes.
    """
    def __init__(self, width, kerf=0.075, profile_points=200,
                 output_profile_images=False, cutting_strategy=CuttingStrategy1):
        self.width = width
        if isinstance(width,int) or isinstance(width,float):
            self.kerf = (kerf,kerf)
        elif isinstance(width,tuple) and len(width) == 2:
            self.kerf = kerf
        else:
            raise AttributeError
        self.profile_points = profile_points
        self.gcode_formatter_name = "default"
        self.output_profile_images = output_profile_images
        self.cutting_strategy_cls = cutting_strategy

    def _draw_profile(self, profile, filename):
        """
        Save the profile as an image.

        Args:
            profile (Profile): object - profile to create image from
            filename (String): string-like object - path of filename to write

        Returns:
            None
        """
        if self.output_profile_images:
            profile.draw(filename)

    def load_panel(self, panel, left_offset=None):
        """
        Load a Panel object into the machine.

        Args:
            panel (Panel): panel to use
            left_offset (Float): How far from the left hotwire post to place
                         the panel.  If the panel is 24 inches and the machine is 30
                         inches, a value of 3 ([30-24]/2) will place the panel centered
                         between the CNC's cutting posts.
        Returns:
            None
        """
        if left_offset is None:
            # if offset is not specified, center
            self.left_offset = (self.width - panel.width) / 2
        else:
            self.left_offset = left_offset
        self.panel = panel

    def generate_gcode(self, le_offset=2.0, te_offset=2.0,
                       safe_height=5, normalize=True, 
                       units="inches", feedrate=None):
        """
        Generate the gcode to cut the panel.  You must have a panel loaded into the machine,
        otherwise it cannot cut.

        Args:
            le_offset (Float): Distance in front of the leading edge the hotwire should extend out
                               and cut to.  If you want to make sure your foam block is cut in half,
                               make sure this value is long enough to reach the front edge of
                               your block.
            te_offset (Float): Distance behind the leading the hotwire should cut to. Similar to
                               the le_offset, except from the trailing edge towards the outside of
                               the foam block you are cutting.
            safe_height (Float): The height where the machine can move freely without hitting anything.
                                 Make sure this value is greater than the height of your foam block.
            normalize (Boolean): When generating the machine path, the x and y values may be < 0.  Setting
                                 this to True translates the values so that all x and y values are >= 0.

        Returns:
            String: Gcode commands separated by newlines.
        """
        if not hasattr(self, "panel"):
            logging.error("No panel loaded into machine.  Load a panel before generating g_code")
            return []

        self.le_offset = le_offset
        self.te_offset = te_offset
        self.safe_height = safe_height
        self.units = units
        self.feedrate = feedrate
        self.gc = Gcode(formatter_name=self.gcode_formatter_name,units=units, feedrate=feedrate)

        cutting_strategy = self.cutting_strategy_cls(self)
        cutting_strategy.cut()

        if normalize:
            self.gc.normalize()

        return self.gc.code_as_str

    def convert_coords_to_machine_pos(self, c1, c2):
        """
        Create the XYUV positions for the machine in order to intersect two Coordinates.

        Args:
            c1 (Coordinate):
            c2 (Coordinate):

        Returns:
            Tuple of Floats: (x, y, u, v)
        """

        # create 3d coordinates and pass them to the 
        pos = self._calc_machine_position(
            (0 + self.left_offset, c1.y, c1.x),
            (self.panel.width + self.left_offset, c2.y, c2.x)
        )
        return (pos[0][1], pos[0][0], pos[1][1], pos[1][0])

    def _calc_machine_position(self, c1_3d, c2_3d):
        """
        Takes 2 3D coordinates - one from left rib, one for right - and calculates
        the machine position based on that.

        Uses the point plane intersect function.

        Args:
            c1_3d (Tuple of Tuples): Tuple with 3 coordinates in 3d space (x,y,z)
            c2_3d (Tuple of Tuples): Tuple with 3 coordinates in 3d space (x,y,z)

        Returns:
            Tuple of Tuples of Floats: ((y1,x1) (y2,x2))
        """
        pillar_a = (0, 0, 0)
        pillar_b = (self.width, 0, 0)
        p_no = (1, 0, 0) # direction/normal of pillar

        c1_3d = (c1_3d[0], c1_3d[1], c1_3d[2])
        c2_3d = (c2_3d[0], c2_3d[1], c2_3d[2])

        a = isect_line_plane_v3(c1_3d, c2_3d, pillar_a, p_no)
        b = isect_line_plane_v3(c1_3d, c2_3d, pillar_b, p_no)
        return a[-2:], b[-2:]

    # ##################
    # ## machine moves #
    # ##################

    # def _move_to_start(self, profile1, profile2, le_offset, safe_height):
    #     # Move machine to start point, fast
    #     c1 = profile1.top.coordinates[0]
    #     c2 = profile2.top.coordinates[0]
    #     min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
    #     self.gc.fast_move(
    #         self.convert_coords_to_machine_pos(
    #             c1 + Coordinate(-le_offset, min_y + safe_height),
    #             c2 + Coordinate(-le_offset, min_y + safe_height)))

    # def _cut_to_start(self, profile1, profile2, le_offset, safe_height):
    #     # Move machine to start point
    #     c1 = profile1.top.coordinates[0]
    #     c2 = profile2.top.coordinates[0]
    #     min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
    #     self.gc.move(
    #         self.convert_coords_to_machine_pos(
    #             c1 + Coordinate(-le_offset, min_y + safe_height),
    #             c2 + Coordinate(-le_offset, min_y + safe_height)))

    # def _cut_to_leading_edge_offset(self, profile1, profile2, le_offset):
    #     start_p1 = profile1.left_midpoint
    #     start_p2 = profile2.left_midpoint
    #     self.gc.move(
    #         self.convert_coords_to_machine_pos(
    #             start_p1 + Coordinate(-le_offset, 0),
    #             start_p2 + Coordinate(-le_offset, 0)))

    # def _cut_top_profile(self, profile1, profile2):
    #     # cut top profile
    #     c1 = profile1.top.coordinates[0]
    #     c2 = profile2.top.coordinates[0]

    #     a_bounds_min, a_bounds_max = profile1.top.bounds
    #     b_bounds_min, b_bounds_max = profile2.top.bounds
    #     a_width = a_bounds_max.x - a_bounds_min.x
    #     b_width = b_bounds_max.x - b_bounds_min.x

    #     for i in range(self.profile_points):
    #         pct = i / self.profile_points
    #         c1 = profile1.top.interpolate_around_profile_dist_pct(pct)
    #         c2 = profile2.top.interpolate_around_profile_dist_pct(pct)
    #         self.gc.move(self.convert_coords_to_machine_pos(c1, c2))

    #     # cut to last point
    #     self.gc.move(self.convert_coords_to_machine_pos(profile1.top.coordinates[-1],
    #                                                     profile2.top.coordinates[-1]))

    # def _cut_to_leading_edge(self, profile1, profile2):
    #     start_p1 = profile1.left_midpoint
    #     start_p2 = profile2.left_midpoint

    #     self.gc.move(self.convert_coords_to_machine_pos(start_p1, start_p2))

    # def _cut_to_trailing_edge_offset(self, profile1, profile2, te_offset):
    #     # go to end point with offset
    #     end_p1 = profile1.right_midpoint
    #     end_p2 = profile2.right_midpoint

    #     self.gc.move(
    #         self.convert_coords_to_machine_pos(
    #             end_p1 + Coordinate(te_offset, 0),
    #             end_p2 + Coordinate(te_offset, 0)))

    # def _cut_to_trailing_edge(self, profile1, profile2):
    #     end_p1 = profile1.right_midpoint
    #     end_p2 = profile2.right_midpoint

    #     # go to trailing edge
    #     self.gc.move(
    #         self.convert_coords_to_machine_pos(
    #             end_p1,
    #             end_p2))

    # def _cut_bottom_profile(self, profile1, profile2):
    #     # cutting profile from right to left
    #     c1 = profile1.top.coordinates[-1]
    #     c2 = profile2.top.coordinates[-1]
    #     # cut bottom profile
    #     a_bounds_min, a_bounds_max = profile1.bottom.bounds
    #     b_bounds_min, b_bounds_max = profile2.bottom.bounds
    #     a_width = a_bounds_max.x - a_bounds_min.x
    #     b_width = b_bounds_max.x - b_bounds_min.x

    #     for i in range(self.profile_points, 0 - 1, -1):
    #         pct = i / self.profile_points
    #         c1 = profile1.bottom.interpolate_around_profile_dist_pct(pct)
    #         c2 = profile2.bottom.interpolate_around_profile_dist_pct(pct)
    #         self.gc.move(self.convert_coords_to_machine_pos(c1, c2))
