import os
from comoda import a_logger, import_from

NO_VCFMINER_CLIENT_MESSAGE = ('The vcfminer client is required, please install it'
                              ' - https://github.com/ratzeni/vcf-miner.client')


class VCFMiner(object):
    """

    """

    def __init__(self, host, user, password, server_host, server_user, loglevel='INFO'):
        self.host = host
        self.username = user
        self.password = password
        self.server_host = server_host
        self.server_user = server_user

        self.log = a_logger(self.__class__.__name__, level=loglevel)
        MC = import_from("vcfminerclient", "VCFMinerClient",
                         error_msg=NO_VCFMINER_CLIENT_MESSAGE)

        if not host.startswith(('http://', 'https://')):
            self.log.warning('Must be provided a wellformed url to the VCFMiner server')

        self.client = MC(conf=dict(host=self.host,
                                   username=self.username,
                                   password=self.password,
                                   server_host=self.server_host,
                                   server_user=self.server_user),
                         logger=self.log)

        self.is_connected = self.client and self.client.is_authenticate

        if not self.is_connected:
            self.log.warning("{} VCFMiner server connection failed".format(host))

        else:
            self.log.info("Connected to {} VCFMiner server".format(host))

    def add_user(self, username, password):
        """
        Given a valid username and password, create a new user in vcf-miner server

        :type username: str
        :type password: str
        :param username: nickname for new user - MANDATORY
        :param password: valid password for new user - MANDATORY
        :return: True if new user correctly created, False if no
        """
        if not username or not password:
            self.log.warning('User and Password are mandatory parameters')
            return False

        if username and self.client.user_exists(username=username):
            self.log.warning('User {} already exists in {}'.format(username, self.host))
            return False

        response = self.client.create_user(username, password)
        self.show_response(response)
        if not response.get('success'):
            return False
        return True

    def upload_vcf(self, vcfpath, vcfname=None, username=None, groupname=None, create_group=False):
        """
        Given a valid vcf file path,  upload it on vcf-miner server

        :type vcfpath: str
        :type vcfname: str
        :type username: str
        :type groupname: str
        :type create_group: bool
        :param vcfpath: VCF to upload on server
        :param vcfname: vcf  alias name (basename if not given)
        :param username: user to whom VCF will be assigned (if given)
        :param groupname: group to whom VCF will be assigned (if given)
        :param create_group: Force to create group if it doesn't exist
        :return: True if new user correctly created, False if no
        """
        vcfname = vcfname if vcfname else os.path.basename(vcfpath)

        if not os.path.exists(vcfpath):
            self.log.warning('VCF file {} not found'.format(vcfpath))
            return False

        if username and not self.client.user_exists(username=username):
            self.log.warning('User {} not found in {}'.format(username, self.host))
            return False

        if groupname and not self.client.group_exists(groupname=groupname):
            self.log.warning('Group {} not found in {}'.format(groupname, self.host))
            if not create_group:
                return False

            self.log.info('Creating group {}'.format(groupname))
            response = self.client.create_group(groupname=groupname)
            self.show_response(response)
            if not response.get('success'):
                return False

            self.log.info('Adding user Admin to group {}'.format(groupname))
            response = self.client.add_user_to_group(username=self.username, groupname=groupname)
            self.show_response(response)
            if not response.get('success'):
                return False

        if groupname and not self.client.group_exists(username=username, groupname=groupname):
            self.log.info('Adding user {} to group {}'.format(username, groupname))
            response = self.client.add_user_to_group(username=username, groupname=groupname)
            self.show_response(response)
            if not response.get('success'):
                return False

        self.log.info('Uploading vcf {}'.format(vcfname))
        vcfname = vcfname if vcfname else os.path.basename(vcfpath)
        response = self.client.upload_vcf(vcfpath=vcfpath, vcfname=vcfname)
        self.show_response(response)

        if response.get('success'):
            self.log.info('Adding vcf {} to Admin user'.format(vcfname))
            rsp = self.client.add_vcf_to_user(vcfname=vcfname, username=self.username)
            self.show_response(rsp)

            if groupname:
                self.log.info('Adding vcf {} to group {}'.format(vcfname, groupname))
                rsp = self.client.add_vcf_to_group(vcfname=vcfname, groupname=groupname)
                self.show_response(rsp)

            if username:
                self.log.info('Adding vcf {} to user {}'.format(vcfname, username))
                rsp = self.client.add_vcf_to_user(vcfname=vcfname, username=username)
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