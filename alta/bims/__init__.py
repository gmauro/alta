from comoda import a_logger


class Bims(object):
    """
    Interface to handle connection to a Biobank Information
    Management System
    """

    def __init__(self, host, user, password, bims_label, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.host = host
        self.user = user
        self.password = password
        self.bims_label = bims_label
        self.loglevel = loglevel
        self.bims = self._build_bims()

    def _build_bims(self):
        if self.bims_label == 'omero.biobank':
            from .omerobiobank import BioBank
            return BioBank(host=self.host, user=self.user, password=self.password)

        if self.bims_label == 'bikalims':
            from .bikalims import BikaLims
            return BikaLims(self.host, self.user, self.password, loglevel=self.loglevel)

        return None

    def is_connected(self):
        return True if self.bims else False
