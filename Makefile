TEMPDIR := $(shell mktemp -u)
PY_V := $(shell python -c 'import sys; print "%d.%d" % sys.version_info[:2]')

TARGETS=all install install_user install_dependency_user clean uninstall

all:
	@echo "Try one of: ${TARGETS}"

install_user: build
	pip install --user dist/*.whl

install: build
	pip install dist/*.whl

install_dependency_user: build
    pip install --user git+https://bitbucket.org/crs4/nglimsclient.git
	pip install --user git+https://github.com/irods/python-irodsclient.git

build: clean
	python setup.py bdist_wheel

clean:
	python setup.py clean --all
	find . -regex '.*\(\.pyc\|\.pyo\)' -exec rm -fv {} \;
	rm -rf dist *.egg-info

uninstall:
	pip uninstall -y alta
