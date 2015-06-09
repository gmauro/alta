import sys

from bl.vl.kb import KnowledgeBase as KB
from alta.utils import a_logger

class BioBank(object):
    """
    """

    def __init__(self, host, user, passwd, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.log.debug('Opening connection to {} OMERO server'.format(
            host))
        try:
            self.kb = KB(driver='omero')(host, user, passwd)
        except ImportError, e:
            self.log.error("{}. Have you forgotten to load the OMERO's "
                           "libraries?".format(e))
            sys.exit()
        self.log.info('Connected to {} OMERO server'.format(host))
        self.log.info('user: {}'.format(user))