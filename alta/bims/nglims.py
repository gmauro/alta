from ..galaxy import BioBlendObject

try:
    import nglimsclient
except ImportError:
    nglimsclient = None

NO_NGLIMS_CLIENT_MESSAGE = ('The nglims client is required, please install it -'
                            ' https://bitbucket.org/crs4/nglimsclient.git')


class NGLims(BioBlendObject):
    """
    """

    def __init__(self, galaxy_host, api_key):
        super(NGLims, self).__init__(galaxy_host, api_key)
        assert nglimsclient is not None, NO_NGLIMS_CLIENT_MESSAGE
        nglimsclient.setupObj(self.gi)
