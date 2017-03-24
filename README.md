# ALTA

 Access Library To infrAstructure for ngs data analysis and management

## Requirements:

- Python 2.7
- [OMERO.biobank](https://github.com/crs4/omero.biobank)
- [BioBlend](https://github.com/galaxyproject/bioblend)
- [nglimsclient](https://bitbucket.org/crs4/nglimsclient)
- [python-irodsclient](https://github.com/irods/python-irodsclient)
- [bikaclient](https://github.com/ratzeni/bika.client)


## Installation


```bash
curl -sS http://gmauro.github.io/alta/install.sh | sh -s venv
```

## Usage


### Connect to a Bika server:
```python
from alta.bims import Bims
bk = Bims('http://host', 'user', 'password', 'bikalims')
```
then to access [bikaclient](https://github.com/ratzeni/bika.client) methods, use
```python
bk.bims.client
<bikaclient.BikaClient instance at 0x7f94b1a26e60>
```
instead to access alta.bims methods, use:
```python
bk.bims
<alta.bims.bikalims.BikaLims at 0x7ff03c68c4d0>
```

### Connect to an iRODS server
```python
from alta.objectstore import build_object_store
ir = build_object_store(store='irods', host=host, user=user, password=password, zone=zone)
```
then to access alta.objectore.yrods methods, use:
```python
ir
<alta.objectstore.yrods.IrodsObjectStore object at 0x7f050742c990>
```

