import pytest
import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class TestGcodeFormatters():
    def test_gcode_no_params(self):
        from hotwing_core import Gcode
        gc = Gcode()
        