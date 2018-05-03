#!/bin/bash

echo "-----------------------------"
echo "Installing python dependicies"
echo "-----------------------------"
pip install -r requirements.txt

echo "-----------------------------"
echo "Starting the Smart Mirror"
echo "-----------------------------"

python run.py