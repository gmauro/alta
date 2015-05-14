import irods
from yclient.utils import a_logger


class yRODS(object):
    """
    """
    prefix = 'irods://'

    def __init__(self, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        status, myEnv = irods.getRodsEnv()
        self.conn, errMsg = irods.rcConnect(myEnv.rodsHost, myEnv.rodsPort,
                                            myEnv.rodsUserName, myEnv.rodsZone)
        status = irods.clientLogin(self.conn)
        if status < 0:
            self.log.error("iRODS connection error {} ".format(status))
        else:
            self.log.info('Connected to {} iRODS server'.format(myEnv.rodsHost))

    def get_collection(self, icoll):
        c = irods.irodsCollection(self.conn)
        self.log.info('Opening {} collection'.format(icoll))
        c.openCollection(icoll)
        self.log.info('Found {} iRODS objects'.format(c.getLenObjects()))
        return c

    def get_irods_metadata(self, path):
        # FIXME: add path validation
        if path.startswith(self.prefix):
            path = path.replace(self.prefix, '')
        raw_metadata = irods.getFileUserMetadata(self.conn, path)
        metadata = {}
        for m in raw_metadata:
            metadata[m[0]] = {'value': m[1], 'units': m[2]}
        return metadata