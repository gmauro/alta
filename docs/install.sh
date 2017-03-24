#!/bin/sh

PWD=`pwd`

# virtualenv label unless overridden by first command-line argument
VENV=${1:-venv}

# create a virtualenv
virtualenv $VENV

# activate it
. $VENV/bin/activate

# create a tmp dir
WORK_DIR=`mktemp -d`

cd $WORK_DIR

# clone alta repo from github
git clone https://github.com/gmauro/alta.git

# install it
cd alta; make install

# remove everything
cd $PWD ; rm -rf $WORK_DIR

echo ""
echo "*****"
echo "To activate the virtual environment, type: source $WORK_DIR/bin/activate"
echo "*****"
