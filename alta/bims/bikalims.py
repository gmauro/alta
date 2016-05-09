from alta.utils import a_logger, import_from

NO_BIKALIMS_CLIENT_MESSAGE = ('The bika client is required, please install it'
                              ' - https://github.com/ratzeni/bika.client')


class BikaLims(object):
    """

    """
    def __init__(self, host, user, password, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        BC = import_from("bikaclient", "BikaClient",
                         error_msg=NO_BIKALIMS_CLIENT_MESSAGE)
        self.bc = BC(host=host, username=user, password=password)
        self.log.info("Connected to {} Bika server".format(host))
