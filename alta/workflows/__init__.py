from alta.utils import a_logger


class WorkflowManagementSystem(object):
    """

    """

    def __init__(self, host, api_key=None, label=None, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.host = host
        self.api_key = api_key
        self.label = label
        self.loglevel = loglevel
        self.build_result = self.build_wms()

    def build_wms(self):
        if self.label == 'galaxy':
            from .galaxy import BioBlendObject
            return BioBlendObject(self.host, self.api_key)
        return None

    def is_connected(self):
        return True if self.build_result else False
