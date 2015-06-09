TEMPDIR := $(shell mktemp -u)
PY_V := $(shell python -c 'import sys; print "%d.%d" % sys.version_info[:2]')

TARGETS=all build install_user install_dependency clean uninstall_user

all:
	@echo "Try one of: ${TARGETS}"

install_user: build
	python setup.py install --user

install: build
	python setup.py install

install_dependency: build
	mkdir -p $(TEMPDIR)
	git clone https://bitbucket.org/crs4/nglimsclient.git $(TEMPDIR)
	cd $(TEMPDIR) && python setup.py install --user
	rm -rf $(TEMPDIR)

build:
	python setup.py build

clean:
	python setup.py clean --all
	find . -regex '.*\(\.pyc\|\.pyo\)' -exec rm -fv {} \;
	rm -rf dist *.egg-info

uninstall_user:
	rm -rf ~/.local/lib/python$(PY_V)/site-packages/yclient*
