from ..bims import Bims
from alta.utils import import_from

NO_BIKALIMS_CLIENT_MESSAGE = ('The nglims client is required, please install it'
                              ' - https://github.com/ratzeni/bika.client')


class BikaLims(Bims):
    """

    """
    def __init__(self, host, user, password, loglevel='INFO'):
        super(BikaLims, self).__init__(host, user, password, loglevel)
        BikaClient = import_from("bikaclient", "BikaClient",
                                 error_msg=NO_BIKALIMS_CLIENT_MESSAGE)
        self.bc = BikaClient(host=host, username=user, password=password)
        self.log.info("Connected to {} Bika server".format(host))
