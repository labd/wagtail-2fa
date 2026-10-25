.PHONY: install test upload docs sandbox format lint


install:
	pip install -e .[docs,test]

test:
	py.test

retest:
	py.test -vvv --lf

coverage:
	py.test --cov=wagtail_2fa --cov-report=term-missing --cov-report=html

format:
	ruff check --fix src tests sandbox
	ruff format src tests sandbox

lint:
	ruff format --check src tests sandbox
	ruff check src tests sandbox

docs:
	$(MAKE) -C docs html

makemessages:
	cd src/wagtail_2fa && django-admin makemessages -a

compilemessages:
	cd src/wagtail_2fa && django-admin compilemessages

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*


sandbox:
	pip install -r sandbox/requirements.txt
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/exampledata/users.json
	sandbox/manage.py runserver
