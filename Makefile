
TARGETS=all install install_user clean uninstall

all:
	@echo "Try one of: ${TARGETS}"

install_user: build_user
	pip install --user --upgrade dist/*.whl

build_user: clean dependencies_user
	python setup.py bdist_wheel

dependencies_user: requirements.txt
	pip install --user --upgrade -r requirements.txt

install: build
	pip install dist/*.whl

build: clean dependencies
	python setup.py bdist_wheel

dependencies: requirements.txt
	pip install -r requirements.txt

clean:
	python setup.py clean --all
	find . -regex '.*\(\.pyc\|\.pyo\)' -exec rm -fv {} \;
	rm -rf dist *.egg-info

uninstall:
	pip uninstall -y alta
