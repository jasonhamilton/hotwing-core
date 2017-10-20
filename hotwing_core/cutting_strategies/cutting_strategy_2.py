from __future__ import division
from ..profile import Profile
from ..coordinate import Coordinate
from .base import CuttingStrategyBase
import logging
logging.getLogger(__name__)


class CuttingStrategy2(CuttingStrategyBase):
    """
    The first cutting strategy
    """
    def cut(self):
        m = self.machine

        # sheet profile
        profile1 = m.panel.left_rib.profile
        profile2 = m.panel.right_rib.profile

        # Offset profiles for Kerf Value
        profile1 = Profile.offset_around_profiles(
            profile1, m.kerf[0], m.kerf[0])
        profile2 = Profile.offset_around_profiles(
            profile2, m.kerf[1], m.kerf[1])

        le_offset = 1
        te_offset = 1

        # MOVE TO SAFE HEIGHT
        self._move_to_safe_height()

        # calc le offset pos
        pos = self.machine.calculate_move(
                profile1.left_midpoint - Coordinate(le_offset, 0),
                profile2.left_midpoint- Coordinate(le_offset, 0))

        ## MOVE FAST HORIZONTALLY TO SPOT ABOVE LE OFFSET
        self.machine.gc.fast_move( {'x':pos['x'],'u':pos['u']} )

        ## MOVE DOWN TO JUST ABOVE FOAM
        self.machine.gc.fast_move( {'y':m.foam_height*1.1,'v':m.foam_height*1.1}, ["do_not_normalize"] )

        # CUT DOWN TO LEADING EDGE OFFSET
        self.machine.gc.move(pos)

        # CUT INWARDS TO LEADING EDGE
        self.machine.gc.move(self.machine.calculate_move(profile1.left_midpoint, profile2.left_midpoint))

        # CUT THE TOP PROFILE
        self._cut_top_profile(profile1, profile2)

        # CUT TO TRAILING EDGE AT MIDDLE OF PROFILE
        self.machine.gc.move(
            self.machine.calculate_move(
                profile1.right_midpoint,
                profile2.right_midpoint)
        )

        # CUT TO TRAILING EDGE OFFSET
        self.machine.gc.move(
            self.machine.calculate_move(
                profile1.right_midpoint + Coordinate(te_offset,0),
                profile2.right_midpoint + Coordinate(te_offset,0))
        )

        # CUT TO TRAILING EDGE AT MIDDLE OF PROFILE
        self.machine.gc.move(
            self.machine.calculate_move(
                profile1.right_midpoint,
                profile2.right_midpoint)
        )

        # CUT BOTTOM PROFILE
        self._cut_bottom_profile(profile1, profile2)

        # CUT TO LEADING EDGE
        self.machine.gc.move(self.machine.calculate_move(profile1.left_midpoint, profile2.left_midpoint))

        # CUT TO LEADING EDGE OFFSET
        self.machine.gc.move(
            self.machine.calculate_move(
                profile1.left_midpoint - Coordinate(le_offset,0),
                profile2.left_midpoint - Coordinate(le_offset,0))
        )

        # CUT UPWARD TO JUST ABOVE FOAM
        self.machine.gc.move( {'y':m.foam_height*1.1,'v':m.foam_height*1.1}, ["do_not_normalize"] )

        # MOVE TO SAFE HEIGHT
        self._move_to_safe_height()

        if m.panel.left_rib.tail_stock:
            # calculate position above tail stock
            r1_stock = m.panel.left_rib.tail_stock
            r2_stock = m.panel.right_rib.tail_stock
            min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
            
            ts_pos = self.machine.calculate_move(
                Coordinate(profile1.right_midpoint.x - r1_stock + self.machine.kerf[0],0),
                Coordinate(profile2.right_midpoint.x - r2_stock + self.machine.kerf[1],0)
            )

            # MOVE TO ABOVE TAIL STOCK
            self.machine.gc.fast_move({'x':ts_pos['x'],'u':ts_pos['u']} )

            # MOVE DOWN TO JUST ABOVE FOAM
            self.machine.gc.fast_move( {'y':m.foam_height*1.1,'v':m.foam_height*1.1}, ["do_not_normalize"] )

            # CUT DOWN TO 0 HEIGHT
            self.machine.gc.move( {'y':0,'v':0}, ["do_not_normalize"] )

            # CUT UP TO JUST ABOVE FOAM
            self.machine.gc.move( {'y':m.foam_height*1.1,'v':m.foam_height*1.1}, ["do_not_normalize"] )

            # MOVE TO SAFE HEIGHT
            self._move_to_safe_height()


        if m.panel.left_rib.front_stock:
            self._move_to_above_front_stock(profile1, profile2, m.safe_height)
            self._cut_front_stock(profile1, profile2, m.safe_height)
            self._move_to_above_front_stock(profile1, profile2, m.safe_height)


    ##################
    ## machine moves #
    ##################


    def _move_to_above_front_stock(self, profile1, profile2, safe_height):
        c1 = profile1.left_midpoint
        c2 = profile2.left_midpoint
        r1_stock = self.machine.panel.left_rib.front_stock
        r2_stock = self.machine.panel.right_rib.front_stock

        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.fast_move(
            self.machine.calculate_move(
                Coordinate(c1.x+r1_stock-self.machine.kerf[0], min_y + safe_height),
                Coordinate(c2.x+r2_stock-self.machine.kerf[1], min_y + safe_height)))

    def _cut_front_stock(self, profile1, profile2, safe_height):
        c1 = profile1.left_midpoint
        c2 = profile2.left_midpoint
        r1_stock = self.machine.panel.left_rib.front_stock
        r2_stock = self.machine.panel.right_rib.front_stock

        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.move(
            self.machine.calculate_move(
                Coordinate(c1.x+r1_stock-self.machine.kerf[0], min_y ),
                Coordinate(c2.x+r2_stock-self.machine.kerf[1], min_y )))




    def _cut_top_profile(self, profile1, profile2):
        # cut top profile
        c1 = profile1.top.coordinates[0]
        c2 = profile2.top.coordinates[0]

        a_bounds_min, a_bounds_max = profile1.top.bounds
        b_bounds_min, b_bounds_max = profile2.top.bounds
        a_width = a_bounds_max.x - a_bounds_min.x
        b_width = b_bounds_max.x - b_bounds_min.x

        for i in range(self.machine.profile_points):
            pct = i / self.machine.profile_points
            c1 = profile1.top.interpolate_around_profile_dist_pct(pct)
            c2 = profile2.top.interpolate_around_profile_dist_pct(pct)
            self.machine.gc.move(self.machine.calculate_move(c1, c2))

        # cut to last point
        self.machine.gc.move(self.machine.calculate_move(profile1.top.coordinates[-1],
                                                        profile2.top.coordinates[-1]))


    def _cut_bottom_profile(self, profile1, profile2):
        # cutting profile from right to left
        c1 = profile1.top.coordinates[-1]
        c2 = profile2.top.coordinates[-1]
        # cut bottom profile
        a_bounds_min, a_bounds_max = profile1.bottom.bounds
        b_bounds_min, b_bounds_max = profile2.bottom.bounds
        a_width = a_bounds_max.x - a_bounds_min.x
        b_width = b_bounds_max.x - b_bounds_min.x

        for i in range(self.machine.profile_points, 0 - 1, -1):
            pct = i / self.machine.profile_points
            c1 = profile1.bottom.interpolate_around_profile_dist_pct(pct)
            c2 = profile2.bottom.interpolate_around_profile_dist_pct(pct)
            self.machine.gc.move(self.machine.calculate_move(c1, c2))
