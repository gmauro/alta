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
        self.client = BC(host=host, username=user, password=password)
        self.log.info("Connected to {} Bika server".format(host))

    def from_bikaid_2_samplelabel(self, bid):
        """
        Given a valid Bika id, returns the corresponding sample label

        :type bid: str
        :param bid: Bika id
        :return: an array of labels as provided from the owner otherwise None.
        """
        result = self.client.query_analysis_request(params=dict(id=bid))
        return result[0]['ClientSampleID'] if result else None

