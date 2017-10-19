from __future__ import division
from .debug_formatter import DebugGcodeFormatter
from .generic import GenericGcodeFormatter
import logging
logging.getLogger(__name__)

class GcodeFormatterFactory():
    formatters = [
                    GenericGcodeFormatter,
                    DebugGcodeFormatter
                 ]
    default = GenericGcodeFormatter

    debug = DebugGcodeFormatter

    @classmethod
    def get_cls(cls, name):
        """
        Get a cutting strategy by name

        Returns:
            GcodeFormatter object
        """
        name = name.lower()
        
        if name == "default":
            return cls.default

        if name == "debug":
            return cls.debug

        for f in cls.formatters:
            f_name = f.__name__.lower()
            if f_name == name:
                return f

        logging.error("ERROR: GCODE FORMATTER NAME INCORRECT, FALLING BACK TO DEFAULT")
        return cls.default

