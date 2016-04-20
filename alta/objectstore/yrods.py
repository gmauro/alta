import os

from ..objectstore import ObjectStore

try:
    from irods.session import iRODSSession
    from irods.collection import iRODSCollection
    from irods.data_object import iRODSDataObject
    from irods.exception import DataObjectDoesNotExist
    from irods.exception import CollectionDoesNotExist
except ImportError:
    iRODSSession = None
    iRODSCollection = None
    iRODSDataObject = None
    DataObjectDoesNotExist = None
    CollectionDoesNotExist = None

NO_IRODS_CLIENT_MESSAGE = ('The Python irods client is required, please '
                           'install it - https://github.com/irods/python-irodsclient')


class IrodsObjectStore(ObjectStore):
    """
    Here objects mean iRODS data_objects and iRODS collections
    """

    def __init__(self, host=None, port=1247, user=None, password=None,
                 zone=None, loglevel='INFO'):
        super(IrodsObjectStore, self).__init__(host, port, user, password,
                                               zone, loglevel)
        assert iRODSSession is not None, NO_IRODS_CLIENT_MESSAGE
        self.user = user
        self.zone = zone
        self.sess = iRODSSession(host=host, port=port, user=user,
                                 password=password, zone=zone)

    def exists(self, path, delivery=False):
        try:
            obj = self.sess.data_objects.get(path)
            exists = True
        except DataObjectDoesNotExist:
            exists = False
            obj = None

        if not obj:
            try:
                obj = self.sess.collections.get(path)
                exists = True
            except CollectionDoesNotExist:
                exists = False
                obj = None

        if delivery:
            return exists, obj
        else:
            return exists

    def is_a_collection(self, obj_path):
        exists, obj = self.exists(obj_path, delivery=True)
        return True if isinstance(obj, iRODSCollection) else False

    def is_a_data_object(self, obj_path):
        exists, obj = self.exists(obj_path, delivery=True)
        return True if isinstance(obj, iRODSDataObject) else False

    def create_object(self, dest_path, collection=True):
        """
        Creates a new object into the dest_path. Default is a collection

        :type dest_path: str
        :param dest_path: irods path

        :type collection: bool
        :param collection: if True create a collection else a data_object

        :return: an irods.data_object.iRODSDataObject,
        irods.collection.iRODSCollection
        """

        if not self.exists(dest_path):
            if collection:
                obj = self.sess.collections.create(dest_path)
            else:
                obj = self.sess.data_objects.create(dest_path)
        else:
            raise RuntimeError("Collection already present into the catalog")

        return obj

    def get_object(self, obj_path, prefix='irods://'):
        """
        Retrieves an object from an existing path

        :type obj_path: str
        :param obj_path: irods path

        :type prefix: str
        :param prefix: path's prefix (if any)

        :return: an irods.data_object.iRODSDataObject,
        irods.collection.iRODSCollection or None
        """

        if obj_path.startswith(prefix):
            obj_path = os.path.join(obj_path.replace(prefix, '/'))
        exists, obj = self.exists(obj_path, delivery=True)

        return obj

    def put_object(self, source_path, dest_path=None, force=False):
        """
        Reads from source_path and puts into the dest_path.
        If dest_path is not set, will be used the same value of source_path
        down to the iRODS user home.
        Mimics the same behaviour of iput: don't write without the force flag
        raised.

        :type source_path: str
        :param source_path: source path

        :type dest_path: str
        :param dest_path: destination path

        :type force: bool
        :param force: force the put execution

        :return: nothing
        """

        if not dest_path:
            dest_path = os.path.join('/', self.zone, 'home', self.user,
                                     source_path.strip('/'))
        new_object = False

        if os.path.isfile(source_path):
            if self.exists(dest_path):
                obj = self.sess.data_objects.get(dest_path)
            else:
                obj = self.create_object(dest_path, collection=False)
                new_object = True

            if not(new_object or force):
                raise ValueError('Overwrite without force flag: {}'.format(obj.path))
            else:
                with obj.open('r+') as d:
                    with open(source_path, 'r') as s:
                        for line in s:
                            d.write(line)
        else:
            self.log.warning('Something wrong here. I received a path that is '
                             'not a regular file - {}'.format(dest_path))

    def remove_object(self, obj_path, recurse=False, force=False):
        """

        :type obj_path: str
        :param obj_path: iRODS path

        :type recurse: bool
        :param recurse: delete everything under the path

        :type force: bool
        :param force: force remove execution

        :return: False if object is missing
        """

        if self.is_a_data_object(obj_path):
            self.sess.data_objects.unlink(obj_path, force=force)
        elif self.is_a_collection(obj_path):
            self.sess.collections.remove(obj_path, recurse=recurse, force=force)
        else:
            self.log.error("Object missing")
            return False

    def add_object_metadata(self, path, meta):
        """
        adds an AVU tuple to the path

        :type path: str
        :param path: destination path in iRODS zone

        :type meta: tuple
        :param meta: a tuple of strings with at least the first two elements (
        attribute and value). If missing, units are set to None

        :return: nothing
        """
        assert (len(meta) >= 2), "Missing element in the metadata tuple {}".format(meta)

        obj = self.get_object(path)
        obj_metadata = []
        for i in obj.metadata.items():
            obj_metadata.append({'name': i.name,
                                 'value': i.value,
                                 'units': i.units})
        if len(meta) == 2:
            meta = meta + (None,)
        avu = {'name': meta[0] if type(meta[0]) == str else str(meta[0]),
               'value': meta[1] if type(meta[1]) == str else str(meta[1]),
               'units': meta[2] if type(meta[2]) == str else str(meta[2])}

        if avu in obj_metadata:
            self.log.error("AVU {} already present into the catalog".format(
                avu))
            raise RuntimeError("AVU already present into the catalog")
        else:
            obj.metadata.add(avu['name'], avu['value'], avu['units'])

