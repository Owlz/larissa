import logging
logger = logging.getLogger("larissa.State.plugins.memory")

from . import PluginBase


class Memory(PluginBase):

    def __init__(self, state, *args, **kwargs):

        self.state = state
        self._page_size = 4096
        self.pages = {}

    def __getitem__(self, item):
        if type(item) in [int, long]:
            return self.state.se.Byte(item)

        elif type(item) is not slice:
            logger.error("Unknown getitem type for memory of {0}".format(type(item)))
            return

        if item.start is None:
            logger.error("Must specify starting address for memory.")
            return

        if item.stop is None:
            logger.error("Must specify stopping address for memory.")
            return

        if item.step is not None:
            logger.error("Not handling stride.")
            return

        return self.state.se.Bytes(address=item.start, length=item.stop - item.start)

    ############
    # Property #
    ############

    @property
    def pages(self):
        """Dictionary of page objects. Dictionary index is the page. For instance, page 6 would be memory.page[5]."""
        return self.__pages

    @pages.setter
    def pages(self, pages):
        if type(pages) is not dict:
            logger.error("Invalid type for pages of {0}".format(type(pages)))
            return

        self.__pages = pages

class Page(object):
    """Simple object abstracting a memory page."""
    
    PROT_READ  = 0x1
    PROT_WRITE = 0x2
    PROT_EXEC  = 0x3
    PROT_NONE  = 0x0

    def __init__(self, prot):

        self.prot = prot

    @property
    def read(self):
        """Boolean does page have read permission."""
        return self.prot & self.PROT_READ > 0

    @property
    def write(self):
        """Boolean does page have write permission."""
        return self.prot & self.PROT_WRITE > 0

    @property
    def execute(self):
        """Boolean does page have execute permission."""
        return self.prot & self.PROT_EXEC > 0

    @property
    def prot(self):
        """Protection (int)."""
        return self.__prot

    @prot.setter
    def prot(self, prot):
        if type(prot) not in [int, long]:
            logger.error("Invalid type for prot of {0}".format(type(prot)))
            return

        if prot > 7 or prot < 0:
            logger.error("Invalid prot value of {0}".format(prot))
            return

        self.__prot = int(prot)

