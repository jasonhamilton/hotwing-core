from __future__ import division
from .utils import isect_line_plane_v3
from .profile import Profile
from .coordinate import Coordinate
from .gcode import Gcode
from .cutting_strategies import CuttingStrategyFactory
import logging
logging.getLogger(__name__)

DEFAULT_FEEDRATE_IN = 5
DEFAULT_FEEDRATE_MM = 125

class Machine():
    """
    The Machine class is a representation of a foam cutting machine and goes
    through the series of cuts required to create a complete cutting path.

    The machine takes a Profile object and generates the code to cut that
    profile.

    Gcode generation gets delegated to the cutting_strategy.

    Args:
        width (Float): length of the machine's hotwire cutter
        kerf (Float):
            Allowance for the hotwire's cutter.  This includes the radius of 
            the wire plus any additional allowance for melted foam from direct
            or radiant heat.
        profile_points (Int): 
            Number of points used when interpolating profiles.  This is the
            number for each (top and bottom) surface of a Profile.
        cutting_strategy_name
        gcode_formatter_name
        units
        feedrate

    :ivar width: width
    :ivar kerf: kerf
    :ivar profile_points: profile_points
    :ivar cutting_strategy_name: cutting_strategy_name
    :ivar gcode_formatter_name: gcode_formatter_name
    :ivar units: units "inches" or "millimeters"
    :ivar feedrate: feedrate on the side of the largest rib
    """
    def __init__(self, width, kerf=0.075, profile_points=200,
                 cutting_strategy_name="default",
                 gcode_formatter_name = "default",
                 units="inches", feedrate=None):
        self.width = width
        if isinstance(kerf,int) or isinstance(kerf,float):
            self.kerf = (kerf,kerf)
        elif isinstance(kerf,tuple) and len(kerf) == 2:
            self.kerf = kerf
        else:
            raise AttributeError
        self.profile_points = profile_points
        self.cutting_strategy_name = cutting_strategy_name
        self.gcode_formatter_name = gcode_formatter_name
        self.units = units
        if feedrate:
            self.feedrate = feedrate
        else:
            # feedrate not specified, set to default
            self.feedrate = DEFAULT_FEEDRATE_IN if units=="inches" else DEFAULT_FEEDRATE_MM


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

    def generate_gcode(self, safe_height=5, foam_height=2, normalize=True):
        """
        Generate the gcode to cut the panel.  You must have a panel loaded into the machine,
        otherwise it cannot cut.

        Args:
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

        self.safe_height = safe_height
        self.foam_height = foam_height
        self.gc = Gcode(formatter_name=self.gcode_formatter_name, 
                        units=self.units, 
                        feedrate=self.feedrate*self.panel.get_feedrate_multiplier() )

        cutting_strategy = CuttingStrategyFactory.get_cls(self.cutting_strategy_name)(self)
        cutting_strategy.cut()

        if normalize:
            self.gc.normalize()

        return self.gc.code_as_str

    def calculate_move(self, c1, c2):
        """
        Create the XYUV positions for the machine in order to intersect two Coordinates.

        Args:
            c1 (Coordinate):
            c2 (Coordinate):

        Returns:
            Dict: {"x":1.1,"y":1.1,"u":1.1,"v":1.1}
        """

        # create 3d coordinates and pass them to the 
        pos = self._calc_machine_position(
            (0 + self.left_offset, c1.y, c1.x),
            (self.panel.width + self.left_offset, c2.y, c2.x)
        )
        return {"x":pos[0][1],"y":pos[0][0],"u":pos[1][1],"v":pos[1][0]}

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
