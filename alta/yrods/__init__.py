import irods
from alta.utils import a_logger
import subprocess


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

    def set_irods_metadata(self, path, metadata):
        # FIXME: add path validation
        if path.startswith(self.prefix):
            path = path.replace(self.prefix, '')

        for name, value in metadata.iteritems():
            self._set_irods_metadata(path,
                                     name=name,
                                     value=value.get('value', None),
                                     units=value.get('units', ''))

    def reg_file(self, local_path, path):
        # FIXME: add path validation
        if path.startswith(self.prefix):
            path = path.replace(self.prefix, '')
        self.__irods_check_output(['ireg', local_path, path])

    def get_irods_file(self, path):
        # FIXME: add path validation
        if path.startswith(self.prefix):
            path = path.replace(self.prefix, '')

        f = irods.irodsOpen(self.conn, path, 'r')
        return f

    def _set_irods_metadata(self, path, name, value, units=''):
        # FIXME: add path validation
        if path.startswith(self.prefix):
            path = path.replace(self.prefix, '')

        if irods.irodsOpen(self.conn, path, 'r'):
            irods.addFileUserMetadata(self.conn, path,
                                      name=name,
                                      value=value,
                                      units=units)

    def __irods_check_output(self, args):
        try:
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as e:
            raise IRodsError(e.cmd, e.returncode, e.output)


class IRodsError(RuntimeError):
    def __init__(self, cmd, retcode, output=None):
        self._cmd = cmd
        self._retcode = retcode
        self._output = output
        cmdstring = ' '.join(map(str, self._cmd))
        message = "iRODS error -> cmd: %s; returncode: %s; output: %s" % \
                (cmdstring, self._retcode, self._output)
        RuntimeError.__init__(self, message)

    @property
    def output(self):
        return self._output

    @property
    def retcode(self):
        return self._retcode

    @property
    def cmd(self):
        return self._cmd