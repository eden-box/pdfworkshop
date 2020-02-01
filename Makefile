ifndef PYTHONCALL
PYTHONCALL=python3
endif

POETRY=$(PYTHONCALL) -m poetry
PRINT=$(PYTHONCALL) -c "import sys; print(str(sys.argv[1]))"

help:
	$(PRINT) "Usage:"
	$(PRINT) "    help          show this message"
	$(PRINT) "    setup         create virtual environment and install dependencies"
	$(PRINT) "    devsetup      create virtual environment and install dev dependencies"
	$(PRINT) "    shell         spawn a shell within the virtual environment"
	$(PRINT) "    test          run test suites"
	$(PRINT) "    autotest      run non manual test suites, used by CI tools"
	$(PRINT) "    dist          package application for distribution"
	$(PRINT) "    pub           publish package to PyPI"
	$(PRINT) "    pubt          publish package to Test PyPI"

setup: update
	$(POETRY) install --no-dev
	$(POETRY) config repositories.testpypi https://test.pypi.org/simple

devsetup: update
	$(POETRY) install
	$(POETRY) config repositories.testpypi https://test.pypi.org/simple

shell:
	$(POETRY) shell

update:
	$(POETRY) update

test: update
	$(POETRY) run pytest

autotest: update
	$(POETRY) run pytest -m "not manual"

dist:   update
	$(POETRY) build

pub:    dist
	$(POETRY) publish

pubt:   dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: setup devsetup shell update test autotest dist pub pubt
