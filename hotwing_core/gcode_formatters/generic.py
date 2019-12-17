from __future__ import division
from .base import GcodeFormatterBase
import logging
logging.getLogger(__name__)

class GenericGcodeFormatter(GcodeFormatterBase):
    """
    Generic Gcode (RS-274?) formatter
    Made to work with LinuxCNC
    """
    def process_command(self, command):
        c = command.data
        if command.type_ == "MOVE":
            return self.process_move(command)
        elif command.type_ == "FAST_MOVE":
            return self.process_fast_move(command)
        elif command.type_ == "DWELL":
            return self.process_dwell(command)
        else:
            self._log_unrecognized_command(command)
            return ""

    def process_dwell(self, command):
        return "G4 P%.4f" % command.data['p']

    def process_move(self,command):
        cmd_list = ['G1']
        return self._make_command(command, cmd_list)

    def process_fast_move(self, command):
        cmd_list = ['G0']
        return self._make_command(command, cmd_list)

        

    def _make_command(self, command, cmd_list):
        d = command.data

        if 'x' in d:
            cmd_list.append("x%.10f" % d['x'])
            self.last_command['x'] = d['x']
        else:
            cmd_list.append("x%.10f" % self.last_command['x'])

        if 'y' in d:
            cmd_list.append("y%.10f" % d['y'])
            self.last_command['y'] = d['y']
        else:
            cmd_list.append("y%.10f" % self.last_command['y'])

        if 'u' in d:
            cmd_list.append("u%.10f" % d['u'])
            self.last_command['u'] = d['u']
        else:
            cmd_list.append("u%.10f" % self.last_command['u'])

        if 'v' in d:
            cmd_list.append("v%.10f" % d['v'])
            self.last_command['v'] = d['v']
        else:
            cmd_list.append("v%.10f" % self.last_command['v'])


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
        self.last_command = {'x':0,'y':0,'u':0,'v':0}


        return out

    def end_commands(self):
        out = []
        # End Program
        out.append("M30")
        return out