from alta.utils import a_logger


class ObjectStore(object):
    """

    """
    def __init__(self, host, port, user, password, zone, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)

    def exists(self, obj_path):
        raise NotImplementedError()

    def get_object(self, obj_path):
        raise NotImplementedError()

    def put_object(self, source_path, dest_path, force=False):
        raise NotImplementedError()

    def remove_object(self, obj_path, recurse=True, force=False):
        raise NotImplementedError()

    def add_object_metadata(self, obj_path, meta):
        raise NotImplementedError()


def build_object_store(store):
    if store == 'irods':
        from .yrods import IrodsObjectStore
        return IrodsObjectStore(host='localhost', port='1247', user='iuser',
                                password='irods123', zone='tempZone')
