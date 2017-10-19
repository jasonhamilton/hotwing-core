from __future__ import division


class GcodeFormatterBase():
    """
    Gcode Formatter's job is to convert the commands maintained
    by the Gcode class and format them into the appropriate format
    for the specification of Gcode being generated.

    You can inherit from this class to create any GcodeFormatter objects.
    On any subclass, you are expected to implement at a minimum
    the process_move and process_fast_move commands.

    The object contains an instance variable parent that provides access to the
    Gcode object.

    :ivar parent: parent gcode instance
    """
    def __init__(self, parent):
        self.parent = parent

    def process_move(cls, command):
        raise NotImplementedError

    def process_fast_move(cls, command):
        raise NotImplementedError

    def start_commands():
        return []

    def end_commands():
        return []