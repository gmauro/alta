from setuptools import setup, find_packages

AuthorInfo = (
    ("Gianmauro Cuccuru", "gmauro@crs4.it")
)

setup(name="alta",
      version='0.3',
      description="package to access the NGS infrastructure",
      author=",".join(a[0] for a in AuthorInfo),
      author_email=",".join("<%s>" % a[1] for a in AuthorInfo),
      install_requires=['biobank', 'bioblend', 'nglimsclient',
                        'python-irodsclient >= 0.5.0'],
      packages=find_packages(),
      license='MIT',
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Internet",
                   "Programming Language :: Python :: 2.7"],
      )
