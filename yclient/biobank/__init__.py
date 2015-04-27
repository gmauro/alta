from bl.vl.kb import KnowledgeBase as KB
from yclient.utils import a_logger

class BioBank(object):
    """
    """

    def __init__(self, host, user, passwd, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.log.debug('Opening connection to {} OMERO server'.format(
            host))
        self.kb = KB(driver='omero')(host, user, passwd)
        self.log.info('Connected to {} OMERO server'.format(host))
        self.log.info('user: {}'.format(user))