from setuptools import setup

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
PACKAGES = ['alta', 'alta.bims', 'alta.workflows', 'alta.objectstore']

setup(name="alta",
      version='0.5',
      description="package to access the NGS infrastructure",
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      install_requires=['bioblend', 'nglimsclient', 'bikaclient>=0.2',
                        'python-irodsclient>=0.5.0'],
      packages=PACKAGES,
      dependency_links=[
        "https://github.com/ratzeni/bika.client/tarball/master#egg=bikaclient",
        "https://github.com/irods/python-irodsclient/tarball/master#egg=python-irodsclient-0.5.0",
        "https://bitbucket.org/crs4/nglimsclient/get/master.zip#egg=nglimsclient" 
      ],
      license='MIT',
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Software Development :: Libraries",
                   "Programming Language :: Python :: 2.7"],
      )
