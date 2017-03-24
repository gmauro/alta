#!/bin/sh

PWD=`pwd`

# create a virtualenv
virtualenv alta

# activate it
. alta/bin/activate

# create a tmp dir
WORK_DIR=`mktemp -d`
echo $WORK_DIR

cd $WORK_DIR

# clone alta repo from github
git clone https://github.com/gmauro/alta.git

# install it
cd alta; make install

# remove everything
cd $PWD ; rm -rf $WORK_DIR


