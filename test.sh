#/usr/bin/bash

echo "run Python2 Tests"
python2 -m unittest discover -s tests

echo "run Python3 Tests"
python3 -m unittest discover -s tests

echo "run pypy Tests"
pypy -m unittest discover -s tests