import pytest
import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


class TestCuttingStrategies():
    def test_cutting_strategies(self):
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

        cutting_strategy_names=["CuttingStrategy1","CuttingStrategy2"]

        for csn in cutting_strategy_names:
            # Setup Machine
            m = Machine(24, kerf=0.075, units="inches", cutting_strategy_name=csn, profile_points=300)
            # Load panel into machine
            m.load_panel(p)
            # Generate GCode
            gcode = m.generate_gcode(safe_height=3)

        # test default
        m = Machine(24, kerf=0.075, units="inches", cutting_strategy_name="default", profile_points=300)
        # Load panel into machine
        m.load_panel(p)
        # Generate GCode
        gcode = m.generate_gcode(safe_height=3)

        # test invalid
        m = Machine(24, kerf=0.075, units="inches", cutting_strategy_name="bad name", profile_points=300)
        # Load panel into machine
        m.load_panel(p)
        # Generate GCode
        gcode = m.generate_gcode(safe_height=3)
        # test invalid

    def test_not_implemented_errror(self):
        from hotwing_core.cutting_strategies import CuttingStrategyBase
        with pytest.raises(NotImplementedError):
            csb = CuttingStrategyBase("machine")
            csb.cut()




