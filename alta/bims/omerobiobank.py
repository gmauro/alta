import sys
from alta.utils import a_logger, import_from


class BioBank(object):
    """
    """

    def __init__(self, host, user, password, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.log.debug('Opening connection to {} OMERO server'.format(
            host))

        KB = import_from("bl.vl.kb", "KnowledgeBase")

        try:
            self.kb = KB(driver='omero')(host, user, password)
        except ImportError, e:
            self.log.error("{}. Have you forgotten to load the OMERO's "
                           "libraries?".format(e))
            sys.exit()
        self.log.info('Connected to {} OMERO server'.format(host))
        self.log.info('user: {}'.format(user))