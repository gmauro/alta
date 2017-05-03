from alta.utils import a_logger, import_from

NO_VCFMINER_CLIENT_MESSAGE = ('The vcfminer client is required, please install it'
                              ' - https://github.com/ratzeni/vcf-miner.client')


class VCFMiner(object):
    """

    """

    def __init__(self, host, user, password, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        MC = import_from("vcfminerclient", "VCFMinerClient",
                         error_msg=NO_VCFMINER_CLIENT_MESSAGE)

        if not host.startswith(('http://', 'https://')):
            self.log.warning('Must be provided a wellformed url to the VCFMiner server')

        self.client = MC(conf=dict(host=host,
                                   username=user,
                                   password=password),
                         logger=self.log)

        self.log.info("Connected to {} VCFMiner server".format(host))