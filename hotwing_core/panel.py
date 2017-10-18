from __future__ import division
from .rib import Rib
from .profile import Profile
from .coordinate import Coordinate


class Panel():
    """
    A Panel is a representation of a wing panel and contains all of the items/objects
    necessary to define a wing.

    A Panel can be thought of as a wing facing down with rib_1 on the left and rib_2 on the right.
    If rib_1 is the root chord and rib_2 is the tip, chord the panel will represent the left part 
    of a wing.

    .. code-block:: bash

                      | ------  width ---------- |
            
                           trailing edge
                      ---------------------------
                     |                           |
             rib_1   |                           |  rib_2
                     |                           |  
                      ---------------------------
                           leading edge


    Args:
        left_rib (Rib): Rib defining the left of the wing
        right_rib (Rib): Rib defining the right of the wing
        width (Float): Width of the Panel measured from left_rib to right_rib

    :ivar left_rib: Left Rib
    :ivar right_rib: Right Rib
    :ivar width: Width

    """

    def __init__(self, left_rib, right_rib, width):
        self.left_rib = left_rib
        self.right_rib = right_rib
        self.width = width

    @classmethod
    def copy(cls, panel):
        """
        Copy a panel

        Args:
            panel (Panel): object to copy

        Returns:
            Panel: New panel
        """
        return cls(panel.left_rib, panel.right_rib, panel.width)

    @classmethod
    def reverse(cls, panel):
        """
        Reverse the ribs on the panel.  If you have a left side, it will make it a right side. The ribs
        will maintain the same direction, but just switch sides.

        Args:
            panel (Panel): object to flip

        Returns:
            Panel: New flipped panel
        """
        return cls(panel.right_rib, panel.left_rib, panel.width)

    @classmethod
    def trim(cls, panel, left=None, right=None):
        """
        Creates a new Panel by taking an existing Panel and trimming it.  
        The new panel's ribs will be interpolated to the correct shape.

        Args:
            panel (Panel): object to trim
            left (Float): distance from left rib to make the left side cut
            right (Float): distance from left rib to make the right side cut

        Returns:
            Panel: New trimmed Panel
        """
        if left is None or left == 0:
            # no need to trim left
            r1 = panel.left_rib
            left = 0
        else:
            # need to interp new left
            r1 = Rib.interpolate_new_rib(
                panel.left_rib, panel.right_rib, panel.width, left)

        if right is None or right == panel.width:
            # no need to trim right
            r2 = panel.right_rib
            right = panel.width
        else:
            r2 = Rib.interpolate_new_rib(
                panel.left_rib, panel.right_rib, panel.width, right)

        new_width = right - left

        p = cls(r1, r2, new_width)
        return p

    def __getitem__(self, key):
        """
        Trim Panel using the slice functionality.

        Ex: panel_obj[2:5], trims from 2 to 5
        """
        if isinstance(key, slice):
            return Panel.trim(self,key.start,key.stop)
        raise NotImplementedError