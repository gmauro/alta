import os.path
import unittest
import uuid

from alta.objectstore.yrods import IrodsObjectStore
from tempfile import NamedTemporaryFile as ntf


class IrodsObjectStoreTest(unittest.TestCase):
    """
    Uses https://hub.docker.com/r/gmauro/boxed-irods/ as test iRODS server
    """
    IRODS_SERVER_HOST = "localhost"
    IRODS_SERVER_PORT = "1247"
    IRODS_SERVER_ZONE = "tempZone"
    IRODS_USER_USERNAME = "iuser"
    IRODS_USER_PASSWORD = "irods123"

    def setUp(self):
        self.ios = IrodsObjectStore(host=self.IRODS_SERVER_HOST,
                                    port=self.IRODS_SERVER_PORT,
                                    user=self.IRODS_USER_USERNAME,
                                    password=self.IRODS_USER_PASSWORD,
                                    zone=self.IRODS_SERVER_ZONE,
                                    loglevel='INFO')
        self.user = self.IRODS_USER_USERNAME
        self.zone = self.IRODS_SERVER_ZONE
        self.home_path = os.path.join('/', self.zone, 'home', self.user)
        self.home_path_fake = os.path.join('/', self.zone, 'nohome', self.user)

    def test_retrieve_home_collection(self):
        coll = self.ios.sess.collections.get(self.home_path)
        self.assertIsInstance(coll.id, int)

    def test_is_a_collection(self):
        self.assertTrue(self.ios.is_a_collection(self.home_path))
        self.assertFalse(self.ios.is_a_collection(self.home_path_fake))

    def test_is_a_data_object(self):
        obj_path = os.path.join(self.home_path, str(uuid.uuid4()))
        self.ios.sess.data_objects.create(obj_path)
        self.assertTrue(self.ios.is_a_data_object(obj_path))
        self.ios.sess.data_objects.unlink(obj_path)

        obj_path_fake = os.path.join(self.home_path, str(uuid.uuid4()))
        self.assertFalse(self.ios.is_a_data_object(self.home_path))
        self.assertFalse(self.ios.is_a_data_object(obj_path_fake))


    def test_a_path_exists_or_not(self):
        exists, obj = self.ios.exists(self.home_path, delivery=True)
        self.assertTrue(exists)
        self.assertIsNotNone(obj)

        exists, obj = self.ios.exists(self.home_path_fake, delivery=True)
        self.assertFalse(exists)
        self.assertIsNone(obj)

        obj_path = os.path.join(self.home_path, str(uuid.uuid4()))
        self.ios.sess.data_objects.create(obj_path)

        exists, obj = self.ios.exists(obj_path, delivery=True)
        self.assertTrue(exists)
        self.assertIsNotNone(obj)

        self.ios.sess.data_objects.unlink(obj_path)

        obj_path_fake = os.path.join(self.home_path, str(uuid.uuid4()))

        exists, obj = self.ios.exists(obj_path_fake, delivery=True)
        self.assertFalse(exists)
        self.assertIsNone(obj)

    def test_create_a_collection(self):
        obj_path = os.path.join(self.home_path, str(uuid.uuid4()))
        obj = self.ios.create_object(obj_path)
        self.assertIsInstance(obj.id, int)
        self.ios.sess.collections.remove(obj_path)

    def test_create_a_data_object(self):
        obj_path = os.path.join(self.home_path, str(uuid.uuid4()))
        obj = self.ios.create_object(obj_path, collection=False)
        self.assertIsInstance(obj.id, int)
        self.ios.sess.data_objects.unlink(obj_path)

    def test_get_a_path_with_prefix(self):
        prefix = 'irods://'
        coll = self.ios.get_object(self.home_path, prefix)
        self.assertIsInstance(coll.id, int)

    def test_get_a_path_that_does_not_exists(self):
        obj_path_fake = os.path.join(self.home_path, str(uuid.uuid4()))
        obj = self.ios.get_object(obj_path_fake)
        self.assertIsNone(obj)

    def test_put_a_path_that_does_not_exists(self):
        msg = "Hi there"
        f = ntf(bufsize=0, delete=False)
        f.write(msg)
        f.close()
        dp1 = os.path.join(self.home_path, os.path.basename(f.name))

        self.ios.put_object(f.name, dest_path=dp1)
        os.unlink(f.name)
        obj = self.ios.sess.data_objects.get(dp1)
        with obj.open('r+') as lf:
            msg_retrieved = lf.readlines()[0]
        self.ios.sess.data_objects.unlink(dp1)
        self.assertEqual(msg, msg_retrieved)

    def test_put_a_path_that_exists(self):
        """Simulate an update"""
        msg1 = "Hi there"
        f = ntf(bufsize=0, delete=False)
        f.write(msg1)
        f.close()
        d = os.path.join(self.home_path, os.path.basename(f.name))
        self.ios.put_object(f.name, dest_path=d)

        msg2 = "Hello there"
        with open(f.name, 'w') as ff:
            ff.write(msg2)

        with self.assertRaises(ValueError):
            self.ios.put_object(f.name, dest_path=d)

        self.ios.put_object(f.name, dest_path=d, force=True)
        obj = self.ios.sess.data_objects.get(d)
        with obj.open('r+') as lf:
            msg_retrieved = lf.readlines()[0]
        self.assertEqual(msg2, msg_retrieved)
        self.ios.sess.data_objects.unlink(d)
        os.unlink(f.name)

    def test_remove_a_path(self):
        obj_path = os.path.join(self.home_path, str(uuid.uuid4()))
        obj = self.ios.create_object(obj_path, collection=False)
        self.ios.remove_object(obj_path)
        self.assertFalse(self.ios.exists(obj_path))

        obj_path = os.path.join(self.home_path, str(uuid.uuid4()))
        obj = self.ios.create_object(obj_path, collection=True)
        self.ios.remove_object(obj_path)
        self.assertFalse(self.ios.exists(obj_path))

        str1 = str(uuid.uuid4())
        str2 = str(uuid.uuid4())

        obj_path1 = os.path.join(self.home_path, str1)
        self.ios.create_object(obj_path1, collection=True)
        obj_path2 = os.path.join(self.home_path, str1, str2)
        self.ios.create_object(obj_path2, collection=False)
        self.ios.remove_object(obj_path1, recurse=True)

        self.assertFalse(self.ios.exists(obj_path1))
        self.assertFalse(self.ios.exists(obj_path2))

    def test_add_metadata(self):
        msg = "Hi there"
        f = ntf(bufsize=0, delete=False)
        f.write(msg)
        f.close()
        d = os.path.join(self.home_path, os.path.basename(f.name))
        self.ios.put_object(f.name, dest_path=d)
        os.unlink(f.name)

        # avu has to be >=2
        avu = ('key1',)
        with self.assertRaises(AssertionError):
            self.ios.add_object_metadata(d, avu)

        # first avu in
        avu = ('key1', 'value1', 'units1')
        self.ios.add_object_metadata(d, avu)
        obj = self.ios.sess.data_objects.get(d)
        obj_metadata = []
        for i in obj.metadata.items():
            obj_metadata.append((i.name, i.value, i.units))
        self.assertIn(avu, obj_metadata)

        # second identical avu has to be rejected
        with self.assertRaises(RuntimeError):
            self.ios.add_object_metadata(d, avu)

        self.ios.sess.data_objects.unlink(d)
