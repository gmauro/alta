import subprocess, sys
from setuptools import setup

if sys.argv[1] == 'install':
    if sys.argv[2] == '--user':
        subprocess.call(['make', 'dependencies_user'])
    else:
        subprocess.call(['make', 'dependencies'])

AuthorInfo = (("Gianmauro Cuccuru", "gmauro@crs4.it"),)

setup(name="alta",
      version='0.5',
      description="package to access the NGS infrastructure",
      author=",".join(a[0] for a in AuthorInfo),
      author_email=",".join("<%s>" % a[1] for a in AuthorInfo),
      license='MIT',
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Infrastructure",
                   "Programming Language :: Python :: 2.7"],
      )

