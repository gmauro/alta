from setuptools import setup

AuthorInfo = (("Gianmauro Cuccuru", "gmauro@crs4.it"),)

setup(name="alta",
      version='0.5',
      description="package to access the NGS infrastructure",
      author=",".join(a[0] for a in AuthorInfo),
      author_email=",".join("<%s>" % a[1] for a in AuthorInfo),
      install_requires=['bioblend', 'nglimsclient', 'bikaclient',
                        'python-irodsclient>=0.5.0'],
      packages=['alta'],
      dependency_links=[
        "https://github.com/ratzeni/bika.client/tarball/master#egg=bikaclient",
        "https://github.com/irods/python-irodsclient/tarball/master#egg=python-irodsclient-0.5.0",
        "https://bitbucket.org/crs4/nglimsclient/get/master.zip#egg=nglimsclient" 
      ],
      license='MIT',
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Infrastructure",
                   "Programming Language :: Python :: 2.7"],
      )

