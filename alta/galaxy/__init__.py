from alta.utils import a_logger, import_from
try:
    import nglimsclient
except ImportError:
    nglimsclient = None

NO_NGLIMS_CLIENT_MESSAGE = ('The nglims client is required, please install it -'
                            ' https://bitbucket.org/crs4/nglimsclient.git')


class BioBlendObject(object):
    """
    """

    def __init__(self, galaxy_host, api_key, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        GI = import_from('bioblend.galaxy.objects', 'GalaxyInstance')
        self.gi = GI(galaxy_host, api_key)
        self.log.info("Connected to {}".format(galaxy_host))


class NGLims(BioBlendObject):
    """
    """

    def __init__(self, galaxy_host, api_key):
        super(NGLims, self).__init__(galaxy_host, api_key)
        assert nglimsclient is not None, NO_NGLIMS_CLIENT_MESSAGE
        nglimsclient.setupObj(self.gi)