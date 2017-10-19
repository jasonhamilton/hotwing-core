import logging
logging.getLogger(__name__)


class CuttingStrategyBase():
    """
    Abstract class for strategies to implement
    """
    def __init__(self, machine):
        self.machine = machine

    def cut(self):
        """
        This is the command method that the parent object will call to
        generate the paths.
        """
        raise NotImplementedError

    def _move_to_safe_height(self):
        self.machine.gc.fast_move( {'y':self.machine.safe_height,'u':self.machine.safe_height}, ["do_not_normalize"] )