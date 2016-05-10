from alta.utils import a_logger


class ObjectStore(object):
    """

    """
    def __init__(self, loglevel='INFO'):
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


def build_object_store(store, **kwargs):
    """
    Build an objecstore on demand.

    :param store: label of the store to invoke
    :param kwargs: all the details needed by the store
    :return: the appropriate object store
    """
    if store == 'irods':
        from .yrods import IrodsObjectStore
        host = kwargs.get('host')
        port = kwargs.get('port', 1247)
        user = kwargs.get('user')
        password = kwargs.get('password')
        zone = kwargs.get('zone')
        return IrodsObjectStore(host=host, port=port, user=user,
                                password=password, zone=zone)
