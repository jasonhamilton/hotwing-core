from __future__ import division
from .base import GcodeFormatterBase


class DebugGcodeFormatter(GcodeFormatterBase):
    """
    This is meant as a debugging class.  It will output the commands
    as a line of text separated by tabs.
    """
    def process_command(cls, command):
        return cls.to_text(command)

    def to_text(cls, command):
        d = command.data
        cmd_list = [command.type_]
        if 'x' in d:
            cmd_list.append("%.10f" % d['x'])
        else:
            cmd_list.append("")
        if 'y' in d:
            cmd_list.append("%.10f" % d['y'])
        else:
            cmd_list.append("")
        if 'u' in d:
            cmd_list.append("%.10f" % d['u'])
        else:
            cmd_list.append("")
        if 'v' in d:
            cmd_list.append("%.10f" % d['v'])
        else:
            cmd_list.append("")
        if 'p' in d:
            cmd_list.append("%.10f" % d['p'])
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
