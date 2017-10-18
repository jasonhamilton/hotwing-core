from __future__ import division
from .cutting_strategy_1 import CuttingStrategy1
from .cutting_strategy_2 import CuttingStrategy2

import logging
logging.getLogger(__name__)

class CuttingStrategyFactory():
    strategies = [
                    CuttingStrategy1,
                    CuttingStrategy2
                 ]
    default = CuttingStrategy2

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

        for s in cls.strategies:
            s_name = s.__class__.__name__.lower()
            if f_name == name:
                return s

        logging.error("ERROR: CUTTING STRATEGY FACTORY - NAME INCORRECT, FALLING BACK TO DEFAULT")
        return cls.default