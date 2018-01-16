import os
from alta.utils import a_logger, import_from
import ga4gh

NO_GA4GH_CLIENT_MESSAGE = ('The ga4gh client is required, please install it'
                              ' - https://github.com/ga4gh/ga4gh-client')


class Ga4gh(object):
    """

    """

    def __init__(self, host, loglevel='INFO'):
        self.host = host
        self.log = a_logger(self.__class__.__name__, level=loglevel)

        # GA = import_from("ga4gh", "client",
        #                  error_msg=NO_GA4GH_CLIENT_MESSAGE)

        if not host.startswith(('http://', 'https://')):
            self.log.warning('Must be provided a wellformed url to the GA4GH server')

        self.client = client.HttpClient(self.host)
