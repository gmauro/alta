from alta.utils import a_logger


class Browsers(object):
    """
    Interface to handle connection to a Genomic Browser
    """

    def __init__(self, host, user, password, browsers_label, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.host = host
        self.user = user
        self.password = password
        self.browsers_label = browsers_label
        self.loglevel = loglevel
        self.browsers = self._build_browsers()

    def _build_browsers(self):
        if self.browsers_label == 'vcfminer':
            from .vcfminer import VCFMiner
            return VCFMiner(host=self.host, user=self.user, password=self.password)

        return None

    def is_connected(self):
        return True if self.browsers else False
