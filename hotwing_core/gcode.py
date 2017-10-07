from .gcode_formatters import GcodeFormatDebug, GenericGcode

FORMATTERS = {'generic': GenericGcode,
              'debug': GcodeFormatDebug}

DEFAULT_FORMATTER = 'generic'


class Gcode():
    """
    Object maintains gcode when it's being generated,
    then outputs the gcode in the correct format.
    
    Contains a GCodeFormatter class, to which all of the
    conversion is delegated to.
    """

    def __init__(self, formatter_name=DEFAULT_FORMATTER):
        self.commands = []
        self.set_formatter(formatter_name)

    def move(self, coords):
        self.commands.append(("MOVE", coords))

    def fast_move(self, coords):
        self.commands.append(("FAST_MOVE", coords))

    def set_formatter(self, formatter_name):
        if formatter_name == 'default':
            self.gcode_formatter = FORMATTERS[DEFAULT_FORMATTER]()
        elif formatter_name in FORMATTERS:
            self.gcode_formatter = FORMATTERS[formatter_name]()
        else:
            print("ERROR SETTING FORMATTER, FALLING BACK TO DEFAULT")
            self.gcode_formatter = FORMATTERS[DEFAULT_FORMATTER]()

    @property
    def code(self):
        """
        returns the gcode as a list
        """
        output = []
        output += self._start_commands()
        output += [self._process_command(c) for c in self.commands]
        output += self._end_commands()
        return output

    @property
    def code_as_str(self):
        return "\n".join(self.code)

    def _start_commands(self):
        return self.gcode_formatter._start_commands()

    def _end_commands(self):
        return self.gcode_formatter._end_commands()

    def _process_command(self, command):
        cmd_type = command[0]
        if cmd_type == "MOVE":
            return self._process_move(command)
        elif cmd_type == "FAST_MOVE":
            return self._process_fast_move(command)
        else:
            return ""

    def _process_move(self, command):
        # delegates to the formatter
        return self.gcode_formatter._process_move(command)

    def _process_fast_move(self, command):
        # delegates to the formatter
        return self.gcode_formatter._process_fast_move(command)

    def normalize(self):
        """
        go through the code and offset it so that min values are 0
        """

        moves = [c for c in self.commands if
                 c[0] == "MOVE" or c[0] == "FAST_MOVE"]

        min_x = min([min([m[1][0] for m in moves]),
                     min([m[1][2] for m in moves])]
                    )
        min_y = min([min([m[1][1] for m in moves]),
                     min([m[1][3] for m in moves])]
                    )

        if min_y < 0:
            offset_y = min_y
        else:
            offset_y = 0

        if min_x < 0:
            offset_x = min_x
        else:
            offset_y = 0

        new_commands = []
        for c in self.commands:
            new_commands.append((c[0],
                                 (c[1][0],
                                  c[1][1],
                                  c[1][2],
                                  c[1][3])
                                 ))

        self.commands = new_commands


if __name__ == "__main__":
    g = Gcode()
    g.move([-1, 2, 3, 4])
    g.fast_move([1, 2, 3, 4])
    g.normalize()
    print(g.code_as_str)