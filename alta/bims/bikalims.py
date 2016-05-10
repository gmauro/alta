from alta.utils import a_logger, import_from

NO_BIKALIMS_CLIENT_MESSAGE = ('The bika client is required, please install it'
                              ' - https://github.com/ratzeni/bika.client')


class BikaLims(object):
    """

    """

    def __init__(self, url, user, password, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        BC = import_from("bikaclient", "BikaClient",
                         error_msg=NO_BIKALIMS_CLIENT_MESSAGE)
        if not url.startswith(('http://', 'https://')):
            self.log.warning('Must be provided a wellformed url to the Bika '
                             'server')
        self.client = BC(host=url, username=user, password=password)
        self.log.info("Connected to {} Bika server".format(url))

    def from_bikaid_2_samplelabel(self, bid):
        """
        Given a valid Bika id, returns a dictionary filled with batch id and
        sample label

        :type bid: str
        :param bid: Bika id
        :return: a dictionary with batch's id and sample's label as
        provided from the owner otherwise None.
        """
        result = self.client.query_analysis_request(params=dict(id=bid))
        if result:
            return {'batch_id': result[0]['title'],
                    'sample_label': result[0]['ClientSampleID']}
        else:
            return None


