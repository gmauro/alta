import nglimsclient

from bioblend.galaxy.objects import GalaxyInstance
from yclient.utils import a_logger


class BioBlendObject(object):
    """
    """

    def __init__(self, galaxy_host, api_key, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        self.gi = GalaxyInstance(galaxy_host, api_key)
        self.log.info("Connected to {}".format(galaxy_host))

class NGLims(BioBlendObject):
    """
    """

    def __init__(self, galaxy_host, api_key):
        super(NGLims, self).__init__(galaxy_host, api_key)
        nglimsclient.setupObj(self.gi)