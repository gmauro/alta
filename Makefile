APPNAME=`cat APPNAME`
TARGETS=clean build dependencies install tag uninstall

all:
	@echo "Try one of: ${TARGETS}"

build: clean dependencies
	python setup.py sdist
	python setup.py bdist_wheel

dependencies: requirements.txt
	pip install -r requirements.txt

clean:
	python setup.py clean --all
	find . -name '*.pyc' -delete
	rm -rf dist *.egg-info __pycache__ build

install: build
	pip install dist/*.whl

tag:
	git tag v${VERSION}

uninstall:
	pip uninstall -y ${APPNAME}
