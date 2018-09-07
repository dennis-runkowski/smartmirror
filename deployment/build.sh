#!/bin/bash

set -e

echo "###############################"
echo "Building Smart Mirror package...."
echo "###############################"

timestamp=$(date +%s)

tar --exclude='../../smartmirror/deployment/packages' \
--exclude='../../smartmirror/img' \
--exclude='../../smartmirror/smartmirror/data_files/main.db' \
--exclude='../../smartmirror/config.yml' \
--exclude='*.pyc' \
--exclude='smartmirror/.git' \
-czvf packages/build_$timestamp.tar.gz ../../smartmirror

echo ""
echo "#######################################"
echo "Completed"
echo "Package Name: build_$timestamp.tar.gz"
echo "#######################################"