ifeq ($(OS),Windows_NT)
	PYTHON = env/Scripts/python
    PIP = env/Scripts/pip
    PYTEST = env/Scripts/py.test
    LINT = env/Scripts/pylint
    SPHINX = env/Scripts/sphinx-build  
else
	PYTHON = env/bin/python
    PIP = env/bin/pip
    PYTEST = env/bin/py.test
    LINT = env/bin/pylint
    SPHINX = env/bin/sphinx-build  
endif


install:
	$(PIP) install -r requirements.txt

run:
ifndef TARGET
	$(error TARGET not set)
else
	$(PYTHON) lift/main.py $(TARGET) && $(PYTHON) tube/main.py a.out
endif

test:
	$(PYTEST) tests

lint:
	$(LINT) tests/* src/* 

doc:
	$(SPHINX) -b html docs/source docs/build

clean:
	@ find . -type f -name '*.pyc' -delete
	@ find . -type f -name '.DS_Store' -delete
	@ find . -type d -name '__pycache__' -delete
	@ rm -f ./a.out

clean-doc:
	@ rm -rf ./docs/build

.PHONY: install, test, lint, doc, run, clean, clean-doc
