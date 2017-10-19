from __future__ import division
from .base import GcodeFormatterBase

class GenericGcodeFormatter(GcodeFormatterBase):
    """
    Generic Gcode (RS-274?) formatter
    Made to work with LinuxCNC
    """
    def process_move(cls, command):
        c = command.coordinates
        cmd_list = ['G1']
        if 'x' in c:
            cmd_list.append("x%.10f" % c['x'])
        if 'y' in c:
            cmd_list.append("y%.10f" % c['y'])
        if 'u' in c:
            cmd_list.append("u%.10f" % c['u'])
        if 'v' in c:
            cmd_list.append("v%.10f" % c['v'])
        return " ".join(cmd_list)

    def process_fast_move(cls, command):
        c = command.coordinates
        cmd_list = ['G0']
        if 'x' in c:
            cmd_list.append("x%.10f" % c['x'])
        if 'y' in c:
            cmd_list.append("y%.10f" % c['y'])
        if 'u' in c:
            cmd_list.append("u%.10f" % c['u'])
        if 'v' in c:
            cmd_list.append("v%.10f" % c['v'])
        return " ".join(cmd_list)

    def start_commands(self):
        out = []

        # Set feedrate
        out.append("F%s" % self.parent.feedrate)

        ## Working Plane
        out.append("G17") # is this necessary?

        # Units        
        if self.parent.units.lower() == "inches":
            out.append("G20")
        elif self.parent.units.lower() == "millimeters":
            out.append("G21")
        else:
            out.append("(Unknown units '%s' specified!)" % self.parent.units)

        ## Absolute Mode
        out.append("G90")

        # Control path mode
        # G64 - Set Blended Path Control Mode
        # Set path tolerance using P value
        if self.parent.units.lower() == "inches":
            out.append("G64 P%.6f" % (1.0/64) )
        elif self.parent.units.lower() == "millimeters":
            out.append("G64 P%.2f" % (0.5) )
        

        # Use first work offset
        out.append("G54")

        return out

    def end_commands(self):
        out = []
        # End Program
        out.append("M30")
        return out