from __future__ import division
from .gcode_formatters import GcodeFormatterFactory
import logging
logging.getLogger(__name__)


DEFAULT_FEEDRATE_IN = 5
DEFAULT_FEEDRATE_MM = 125



class MachineCommand():
    def __init__(self, type_, coordinates, options=[]):
        self.type_ = type_
        self.coordinates = coordinates
        self.options = options

    def has_option(self, option):
        for o in self.options:
            if option in self.options:
                return True
        return False



class Gcode():
    """
    The Gcode object maintains a list of gcode commands and allows you
    to add commands easily.  
    
    Contains a GCodeFormatter class, to which all of the formatting is 
    delegated to.

    :ivar units: units - "inches" or "millimeters"
    :ivar feedrate: feedrate - units per min (default 5 for inch units, 125 for mm units)
    """

    def __init__(self, formatter_name=None, units="inches", feedrate=None):
        self._commands = []
        self.units = units
        if feedrate:
            self.feedrate = feedrate
        else:
            # feedrate not specified, set to default
            self.feedrate = DEFAULT_FEEDRATE_IN if units=="inches" else DEFAULT_FEEDRATE_MM
        self.set_formatter(formatter_name)

    def move(self, coords, options=[]):
        self._commands.append(MachineCommand("MOVE", coords, options))

    def fast_move(self, coords, options=[]):
        self._commands.append(MachineCommand("FAST_MOVE", coords, options))

    def set_formatter(self, formatter_name):
        formatter_cls = GcodeFormatterFactory.get_cls(formatter_name)
        self.gcode_formatter = formatter_cls(self)
            
    @property
    def code(self):
        """
        returns the gcode as a list
        """
        output = []
        output += self._start_commands()
        output += [self._process_command(c) for c in self._commands]
        output += self._end_commands()
        return output

    @property
    def code_as_str(self):
        return "\n".join(self.code)

    def _start_commands(self):
        return self.gcode_formatter.start_commands()

    def _end_commands(self):
        return self.gcode_formatter.end_commands()

    def _process_command(self, command):
        cmd_type = command.type_
        if cmd_type == "MOVE":
            return self._process_move(command)
        elif cmd_type == "FAST_MOVE":
            return self._process_fast_move(command)
        else:
            return ""

    def _process_move(self, command):
        # delegates to the formatter
        return self.gcode_formatter.process_move(command)

    def _process_fast_move(self, command):
        # delegates to the formatter
        return self.gcode_formatter.process_fast_move(command)

    def normalize(self):
        """
        go through the code and offset it so that min values are 0
        """
        moves = []
        for c in self._commands:
            if not c.has_option("do_not_normalize"):
                moves.append(c)

        min_x = min([min([m.coordinates['x'] for m in moves if 'x' in m.coordinates]),
                     min([m.coordinates['u'] for m in moves if 'u' in m.coordinates])]
                    )
        min_y = min([min([m.coordinates['y'] for m in moves if 'y' in m.coordinates]),
                     min([m.coordinates['v'] for m in moves if 'v' in m.coordinates])]
                    )

        if min_y < 0:
            offset_y = min_y
        else:
            offset_y = 0

        if min_x < 0:
            offset_x = min_x
        else:
            offset_x = 0

        new_commands = []
        for c in self._commands:
            if not c.has_option("do_not_normalize"):
                if 'x' in c.coordinates:
                    c.coordinates['x'] = c.coordinates['x'] - offset_x
                if 'y' in c.coordinates:
                    c.coordinates['y'] = c.coordinates['y'] - offset_y
                if 'u' in c.coordinates:
                    c.coordinates['u'] = c.coordinates['u'] - offset_x
                if 'v' in c.coordinates:
                    c.coordinates['v'] = c.coordinates['v'] - offset_y

