import os
from alta.utils import a_logger, import_from

NO_VCFMINER_CLIENT_MESSAGE = ('The vcfminer client is required, please install it'
                              ' - https://github.com/ratzeni/vcf-miner.client')


class VCFMiner(object):
    """

    """

    def __init__(self, host, user, password, loglevel='INFO'):
        self.host = host
        self.username = user

        self.log = a_logger(self.__class__.__name__, level=loglevel)
        MC = import_from("vcfminerclient", "VCFMinerClient",
                         error_msg=NO_VCFMINER_CLIENT_MESSAGE)

        if not host.startswith(('http://', 'https://')):
            self.log.warning('Must be provided a wellformed url to the VCFMiner server')

        self.client = MC(conf=dict(host=host,
                                   username=user,
                                   password=password),
                         logger=self.log)

        self.is_connected = self.client and self.client.is_authenticate

        if not self.is_connectd:
            self.log.warning("{} VCFMiner server connection failed".format(host))

        else:
            self.log.info("Connected to {} VCFMiner server".format(host))

    def create_user(self, new_user, new_password='CHANGEME'):
        return True

    def upload_vcf(self, vcfpath, vcfname=None, user_id=None, group_id=None, force_group=False):

        if user_id and not self.client.user_exists(username=user_id):
            self.log.warning('User {} not found in {}'.format(user_id, self.host))
            return False

        if group_id and not self.client.group_exists(groupname=group_id):
            self.log.warning('Group {} not found in {}'.format(group_id, self.host))
            if not force_group:
                return False

            self.log.info('Creating group {}'.format(group_id))
            response = self.create_group(groupname=group_id)
            self.show_response(response)
            if not response.get('success'):
                return False

        vcfname = vcfname if vcfname else os.path.basename(vcfpath)
        response = self.client.upload_vcf(vcfpath=vcfpath, vcfname=vcfname)
        self.show_response(response)

        if response.get('success'):

            if group_id:
                rsp = add_vcf_to_group(vcfname, groupname)
                self.show_response(rsp)

            if user_id:
                rsp = add_vcf_to_user(vcfname, username)
                self.show_response(rsp)

            return True

        return False

    def show_response(self, response):

        if response.get('result') and len(response.get('result')) > 0:
            self.log.info(response.get('result'))

        if response.get('warnings') and len(response.get('warnings')) > 0:
            self.log.warning(response.get('warnings'))

        if response.get('errors') and len(response.get('errors')) > 0:
            self.log.error(response.get('errors'))