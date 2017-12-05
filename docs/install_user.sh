#!/bin/sh

MYPWD=$(pwd)

# create a tmp dir
WORK_DIR=`mktemp -d`

cd ${WORK_DIR}

# clone alta repo from github
git clone https://github.com/gmauro/alta.git

# install it
cd alta; make install_user

# remove everything
cd ${MYPWD} ; rm -rf ${WORK_DIR}
