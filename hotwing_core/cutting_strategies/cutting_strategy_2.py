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
        profile1 = m.panel.rib1.profile
        profile2 = m.panel.rib2.profile

        # Offset profiles for Kerf Value
        profile1 = Profile.offset_around_profiles(
            profile1, m.kerf[0], m.kerf[0])
        profile2 = Profile.offset_around_profiles(
            profile2, m.kerf[1], m.kerf[1])

        self._move_to_start(profile1, profile2, m.le_offset, m.safe_height)
        self._cut_to_leading_edge_offset(profile1, profile2, m.le_offset)
        self._cut_to_leading_edge(profile1, profile2)
        self._cut_top_profile(profile1, profile2)
        self._cut_to_trailing_edge(profile1, profile2)
        self._cut_to_trailing_edge_offset(profile1, profile2, m.te_offset)
        self._cut_to_trailing_edge(profile1, profile2)
        self._cut_bottom_profile(profile1, profile2)
        self._cut_to_leading_edge(profile1, profile2)
        self._cut_to_leading_edge_offset(profile1, profile2, m.le_offset)
        self._cut_to_start(profile1, profile2, m.le_offset, m.safe_height)

        if m.panel.rib1.tail_stock:
            self._move_to_above_tail_stock(profile1, profile2, m.safe_height)
            self._cut_tail_stock(profile1, profile2, m.safe_height)
            self._move_to_above_tail_stock(profile1, profile2, m.safe_height)

        if m.panel.rib1.front_stock:
            self._move_to_above_front_stock(profile1, profile2, m.safe_height)
            self._cut_front_stock(profile1, profile2, m.safe_height)
            self._move_to_above_front_stock(profile1, profile2, m.safe_height)


    ##################
    ## machine moves #
    ##################
    def _move_to_above_tail_stock(self, profile1, profile2, safe_height):
        c1 = profile1.right_midpoint
        c2 = profile2.right_midpoint
        r1_stock = self.machine.panel.rib1.tail_stock
        r2_stock = self.machine.panel.rib2.tail_stock

        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.fast_move(
            self.machine.convert_coords_to_machine_pos(
                Coordinate(c1.x-r1_stock, min_y + safe_height),
                Coordinate(c2.x-r2_stock, min_y + safe_height)))

    def _cut_tail_stock(self, profile1, profile2, safe_height):
        c1 = profile1.right_midpoint
        c2 = profile2.right_midpoint
        r1_stock = self.machine.panel.rib1.tail_stock
        r2_stock = self.machine.panel.rib2.tail_stock

        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.fast_move(
            self.machine.convert_coords_to_machine_pos(
                Coordinate(c1.x-r1_stock, min_y ),
                Coordinate(c2.x-r2_stock, min_y )))

    def _move_to_above_front_stock(self, profile1, profile2, safe_height):
        c1 = profile1.left_midpoint
        c2 = profile2.left_midpoint
        r1_stock = self.machine.panel.rib1.front_stock
        r2_stock = self.machine.panel.rib2.front_stock

        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.fast_move(
            self.machine.convert_coords_to_machine_pos(
                Coordinate(c1.x+r1_stock, min_y + safe_height),
                Coordinate(c2.x+r2_stock, min_y + safe_height)))

    def _cut_front_stock(self, profile1, profile2, safe_height):
        c1 = profile1.left_midpoint
        c2 = profile2.left_midpoint
        r1_stock = self.machine.panel.rib1.front_stock
        r2_stock = self.machine.panel.rib2.front_stock

        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.fast_move(
            self.machine.convert_coords_to_machine_pos(
                Coordinate(c1.x+r1_stock, min_y ),
                Coordinate(c2.x+r2_stock, min_y )))

    def _move_to_start(self, profile1, profile2, le_offset, safe_height):
        # Move machine to start point, fast
        c1 = profile1.top.coordinates[0]
        c2 = profile2.top.coordinates[0]
        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.fast_move(
            self.machine.convert_coords_to_machine_pos(
                c1 + Coordinate(-le_offset, min_y + safe_height),
                c2 + Coordinate(-le_offset, min_y + safe_height)))

    def _cut_to_start(self, profile1, profile2, le_offset, safe_height):
        # Move machine to start point
        c1 = profile1.top.coordinates[0]
        c2 = profile2.top.coordinates[0]
        min_y = min(profile1.y_bounds[0], profile2.y_bounds[0])
        self.machine.gc.move(
            self.machine.convert_coords_to_machine_pos(
                c1 + Coordinate(-le_offset, min_y + safe_height),
                c2 + Coordinate(-le_offset, min_y + safe_height)))

    def _cut_to_leading_edge_offset(self, profile1, profile2, le_offset):
        start_p1 = profile1.left_midpoint
        start_p2 = profile2.left_midpoint
        self.machine.gc.move(
            self.machine.convert_coords_to_machine_pos(
                start_p1 + Coordinate(-le_offset, 0),
                start_p2 + Coordinate(-le_offset, 0)))

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
            self.machine.gc.move(self.machine.convert_coords_to_machine_pos(c1, c2))

        # cut to last point
        self.machine.gc.move(self.machine.convert_coords_to_machine_pos(profile1.top.coordinates[-1],
                                                        profile2.top.coordinates[-1]))

    def _cut_to_leading_edge(self, profile1, profile2):
        start_p1 = profile1.left_midpoint
        start_p2 = profile2.left_midpoint

        self.machine.gc.move(self.machine.convert_coords_to_machine_pos(start_p1, start_p2))

    def _cut_to_trailing_edge_offset(self, profile1, profile2, te_offset):
        # go to end point with offset
        end_p1 = profile1.right_midpoint
        end_p2 = profile2.right_midpoint

        self.machine.gc.move(
            self.machine.convert_coords_to_machine_pos(
                end_p1 + Coordinate(te_offset, 0),
                end_p2 + Coordinate(te_offset, 0)))

    def _cut_to_trailing_edge(self, profile1, profile2):
        end_p1 = profile1.right_midpoint
        end_p2 = profile2.right_midpoint

        # go to trailing edge
        self.machine.gc.move(
            self.machine.convert_coords_to_machine_pos(
                end_p1,
                end_p2))

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
            self.machine.gc.move(self.machine.convert_coords_to_machine_pos(c1, c2))
