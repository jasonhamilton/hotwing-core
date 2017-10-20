import pytest
import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class TestGcodeFormatters():
    def test_gcode_formatters(self):
        from hotwing_core import Profile
        from hotwing_core import Rib
        from hotwing_core import Machine
        from hotwing_core import Panel
        from hotwing_core import Coordinate

        ## Setup Rib
        r1 = Rib("http://m-selig.ae.illinois.edu/ads/coord/ah83159.dat",
                 scale=10,
                 xy_offset=None,
                 top_sheet=0.0625,
                 bottom_sheet=0.0625,
                 front_stock=0.5,
                 tail_stock=1.25 )
                 
        r2 = Rib("http://m-selig.ae.illinois.edu/ads/coord/rg14.dat",
                 scale=10,
                 xy_offset=Coordinate(0, 0),
                 top_sheet=0.0625,
                 bottom_sheet=0.0625,
                 front_stock=0.5,
                 tail_stock=1.25 )

        # Setup Panel
        p = Panel(r1, r2, 24)

        gcode_formatter_names=["GenericGcodeFormatter","DebugGcodeFormatter","default"]

        for gfn in gcode_formatter_names:
            # Setup Machine
            m = Machine(24, kerf=0.075, units="inches", gcode_formatter_name=gfn, profile_points=300)
            # Load panel into machine
            m.load_panel(p)
            # Generate GCode
            gcode = m.generate_gcode(safe_height=3)

    # def test_gcode_formatter_base(self):
    #     from hotwing_core.gcode_formatters import GcodeFormatterBase
    #     with pytest.raises(NotImplementedError):
    #         GcodeFormatterBase.process_move("obj")
    #     with pytest.raises(NotImplementedError):
    #         GcodeFormatterBase.move("obj")