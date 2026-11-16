.PHONY: install test retest coverage format lint docs makemessages compilemessages release sandbox


install:
	uv sync --all-groups

test:
	uv run pytest

retest:
	uv run pytest -vvv --lf

coverage:
	uv run pytest --cov=wagtail_2fa --cov-report=term-missing --cov-report=html

format:
	uv run ruff check --fix src tests sandbox
	uv run ruff format src tests sandbox

lint:
	uv run ruff format --check src tests sandbox
	uv run ruff check src tests sandbox

docs:
	uv run --group docs $(MAKE) -C docs html

makemessages:
	cd src/wagtail_2fa && uv run django-admin makemessages -a

compilemessages:
	cd src/wagtail_2fa && uv run django-admin compilemessages

release:
	rm -rf dist/*
	uv build


sandbox:
	uv sync --group sandbox
	uv run sandbox/manage.py migrate
	uv run sandbox/manage.py loaddata sandbox/exampledata/users.json
	uv run sandbox/manage.py runserver
