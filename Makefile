PIP=python -m pip
PYR=python -m pipenv
PRINT=python -c "import sys; print(str(sys.argv[1]))"

help:
	$(PRINT) "Usage:"
	$(PRINT) "    help          show this message"
	$(PRINT) "    setup         create virtual environment and install dependencies"
	$(PRINT) "    dist          package application for distribution"
	$(PRINT) "    clean         remove the project dependencies and environment"

setup:
	$(PIP) install pipenv
	$(PYR) install --three
	$(PYR) run pip install .
	$(PYR) lock -r > requirements.txt

dist:	clean setup
	$(PYR) run python setup.py sdist bdist_wheel

pub:    dist
	twine upload dist/*

pubt:    dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -f -r dist build *.egg-info requirements.txt

delete:    clean
	$(PYR) --rm

.PHONY: setup dist pub pubt clean delete
