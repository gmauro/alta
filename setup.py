import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'VERSION')) as f:
    __version__ = f.read().strip()

with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

extra_files = [os.path.join(here, 'requirements.txt'),
               os.path.join(here, 'VERSION'),
               ]

AUTHOR_INFO = [
  ("Gianmauro Cuccuru", "gianmauro.cuccuru@crs4.it"),
  ("Rossano Atzeni", "rossano.atzeni@crs4.it"),
  ]
MAINTAINER_INFO = [
  ("Gianmauro Cuccuru", "gianmauro.cuccuru@crs4.it"),
  ]
AUTHOR = ", ".join(t[0] for t in AUTHOR_INFO)
AUTHOR_EMAIL = ", ".join("<%s>" % t[1] for t in AUTHOR_INFO)
MAINTAINER = ", ".join(t[0] for t in MAINTAINER_INFO)
MAINTAINER_EMAIL = ", ".join("<%s>" % t[1] for t in MAINTAINER_INFO)
PACKAGES = ['alta', 'alta.bims', 'alta.workflows', 'alta.objectstore', 'alta.browsers']

setup(name="alta",
      version=__version__,
      description="package to access the NGS infrastructure",
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      install_requires=required,
      package_data={'': extra_files},
      packages=PACKAGES,
      license='MIT',
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Software Development :: Libraries",
                   "Programming Language :: Python :: 2.7"],
      )
