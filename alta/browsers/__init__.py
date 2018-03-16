from comoda import a_logger


class Browsers(object):
    """
    Interface to handle connection to a Genomic Browser
    """

    def __init__(self, host, user='username', password='******', browsers_label='',
                 server_host=None, server_user=None,
                 loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.host = host
        self.user = user
        self.password = password
        self.server_host = server_host
        self.server_user = server_user
        self.browsers_label = browsers_label
        self.loglevel = loglevel
        self.browsers = self._build_browsers()

    def _build_browsers(self):
        if self.browsers_label == 'vcfminer':
            from .vcfminer import VCFMiner
            return VCFMiner(host=self.host, user=self.user, password=self.password,
                            server_host=self.server_host, server_user=self.server_user)

        return None

    def is_connected(self):
        return True if self.browsers else False
