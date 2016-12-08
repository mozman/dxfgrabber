# Author:  mozman
# License: MIT-License

RUNTESTS = -m unittest discover -s tests

PYTHON35 = py -3.5

PYPY = C:\pypy2-5.6.0\pypy.exe


test35:
	$(PYTHON35) $(RUNTESTS)

testpypy:
	$(PYPY) $(RUNTESTS)

testall: test35 testpypy

packages:
	py setup.py sdist --formats=zip,gztar
	py setup.py bdist_wheel

pypi:
	py setup.py sdist --formats=zip,gztar upload
	py setup.py bdist_wheel upload
