from __future__ import division
from .gcode_formatters import GcodeFormatterFactory
import logging
logging.getLogger(__name__)


DEFAULT_FEEDRATE_IN = 5
DEFAULT_FEEDRATE_MM = 125



class MachineCommand():
    """
    This represents the data for a single command for a machine move.

    Args:
        type\_ (str): type of command
        values (dict):  data to hold data related to the command
        options (list): additional options that can be read and utilized when formatting
                        or outputting gcode.

    :ivar str type\_:  type of command
    :ivar dict data: data to hold data related to the command
    """
    def __init__(self, type_, data, options=[]):
        self.type_ = type_
        self.data = data
        self._options = options

    def has_option(self, option):
        """
        Determine if value is in the options list

        Args:
            option (str): value to check

        Returns:
            Boolean
        """
        for o in self._options:
            if option in self._options:
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

    def dwell(self, time, options=[]):
        """
        time in seconds
        """
        self._commands.append(MachineCommand("DWELL", {"p":time}, options))

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
        return self.gcode_formatter.process_command(command)

    def normalize(self):
        """
        go through the code and offset it so that min values are 0
        """
        moves = []
        for c in self._commands:
            if c.type_ in ["MOVE","FAST_MOVE"] and not c.has_option("do_not_normalize"):
                moves.append(c)

        min_x = min([min([m.data['x'] for m in moves if 'x' in m.data]),
                     min([m.data['u'] for m in moves if 'u' in m.data])]
                    )
        min_y = min([min([m.data['y'] for m in moves if 'y' in m.data]),
                     min([m.data['v'] for m in moves if 'v' in m.data])]
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
            if c.type_ in ["MOVE","FAST_MOVE"] and not c.has_option("do_not_normalize"):
                if 'x' in c.data:
                    c.data['x'] = c.data['x'] - offset_x
                if 'y' in c.data:
                    c.data['y'] = c.data['y'] - offset_y
                if 'u' in c.data:
                    c.data['u'] = c.data['u'] - offset_x
                if 'v' in c.data:
                    c.data['v'] = c.data['v'] - offset_y

