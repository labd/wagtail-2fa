.PHONY: install test upload docs sandbox


install:
	pip install -e .[docs,test]

test:
	py.test

retest:
	py.test -vvv --lf

coverage:
	py.test --cov=wagtail_2fa --cov-report=term-missing --cov-report=html

docs:
	$(MAKE) -C docs html

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*


sandbox:
	pip install -r sandbox/requirements.txt
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/exampledata/users.json
	sandbox/manage.py runserver
