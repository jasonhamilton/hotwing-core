from __future__ import division
from .base import GcodeFormatterBase


class DebugGcodeFormatter(GcodeFormatterBase):
    """
    This is meant as a debugging class.  It will output the commands
    as a line of text separated by tabs.
    """
    def process_move(cls, command):
        return cls.to_text(command)


    def process_fast_move(cls, command):
        return cls.to_text(command)


    def to_text(cls, command):
        c = command.coordinates
        cmd_list = [command.type_]
        if 'x' in c:
            cmd_list.append("%.10f" % c['x'])
        else:
            cmd_list.append("")
        if 'y' in c:
            cmd_list.append("%.10f" % c['y'])
        else:
            cmd_list.append("")
        if 'u' in c:
            cmd_list.append("%.10f" % c['u'])
        else:
            cmd_list.append("")
        if 'v' in c:
            cmd_list.append("%.10f" % c['v'])
        else:
            cmd_list.append("")
        return "\t".join(cmd_list)

    def start_commands(self):
        out = []
        out.append("Units: %s" % self.parent.units)
        out.append("Feedrate: %s" % self.parent.feedrate)
        return out

    def end_commands(self):
        return []
