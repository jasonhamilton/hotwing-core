
class GcodeFormatBase():
    """
    Gcode Formatter's job is to convert the commands maintained
    by the Gcode class and format them into the appropriate format
    for the specification of Gcode being generated.

    On any subclass, you are expected to implement at a minimum
    the _process_move and _process_fast_move commands.
    """
    def __init__(self, parent):
        self.parent = parent

    def _process_move(cls, command):
        raise NotImplementedError

    def _process_fast_move(cls, command):
        raise NotImplementedError

    def _start_commands():
        return []

    def _end_commands():
        return []


class GcodeFormatDebug(GcodeFormatBase):
    """
    This is meant as a debugging class.  It will output the commands
    as a line of text separated by tabs.
    """
    def _process_move(cls, command):
        return cls._move_to_string(command)

    def _process_fast_move(cls, command):
        return cls._move_to_string(command)

    def _move_to_string(cls, command):
        cmd_type = command[0]
        cmds_as_str = [cmd_type]
        for c in command[1]:
            type_ = type(c)
            if type_ is str:
                cmds_as_str.append(c)
            if type_ is int or type_ is float:
                cmds_as_str.append("%.10f" % c)
        return "\t".join(cmds_as_str)

    def _start_commands(self):
        out = []
        out.append("Units: " % self.parent.units)
        return out

    def _end_commands(self):
        return []


class GenericGcode(GcodeFormatBase):
    """
    Generic Gcode (RS-274?) formatter
    Made to work with LinuxCNC
    """
    def _process_move(cls, command):
        return "G1 x%.10f y%.10f u%.10f v%.10f" % command[1]

    def _process_fast_move(cls, command):
        return "G0 x%.10f y%.10f u%.10f v%.10f" % command[1]

    def _start_commands(self):
        out = []

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
        # G61 - Set Exact Path Control Mode
        # G64 - Set Blended Path Control Mode
        out.append("G61")

        # Use first work offset
        out.append("G54")

        return out

    def _end_commands(self):
        out = []
        # End Program
        out.append("M30")
        return out
