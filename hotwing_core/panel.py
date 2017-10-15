from __future__ import division
from .rib import Rib
from .profile import Profile
from .coordinate import Coordinate


class Panel():
    """
    A Panel is a representation of a wing panel and contains all of the items/objects
    necessary to define the attributes of the wing.

    Args:
        rib1 (Rib): object
        rib2 (Rib): object
        width (Float): width of the total wing panel from rib to rib
    """
    def __init__(self, rib1, rib2, width):
        self.rib1 = rib1
        self.rib2 = rib2
        self.width = width

    @classmethod
    def trim_panel(cls, panel, left=None, right=None):
        """
        Creates a new Panel by taking an existing Panel and trimming off an amount from each 
        side to make it shorter.  The new panel's ribs will be interpolated to the correct shape.

        Args:
            panel (Panel): object to trim
            left (Float): amount to trim from the left side of the panel
            right (Float): amount to trim from the right side of the panel

        Returns:
            Panel: New trimmed Panel
        """
        if left is None or left == 0:
            # no need to trim left
            r1 = panel.rib1
            left = 0
        else:
            # need to interp new left
            r1 = Rib.interpolate_new_rib(
                panel.rib1, panel.rib2, panel.width, left)

        if right is None or right == panel.width:
            # no need to trim right
            r2 = panel.rib2
            right = panel.width
        else:
            r2 = Rib.interpolate_new_rib(
                panel.rib1, panel.rib2, panel.width, right)

        new_width = right - left

        p = cls(r1, r2, new_width)
        return p
