HERE := .
VENV := $(shell pipenv --venv)
SRC := ${HERE}/src
PYTHONPATH := ${SRC}

RUN := pipenv run
PY := ${RUN} python


.PHONY: format
format:
	${RUN} isort --virtual-env "${VENV}" "${HERE}/src"
	${RUN} isort --virtual-env "${VENV}" "${HERE}/serverless/src"
	${RUN} black "${HERE}/src"
	${RUN} black "${HERE}/serverless/src"


.PHONY: run
run:
	${PY} src/manage.py runserver


.PHONY: migrate
migrate:
	${PY} src/manage.py migrate


.PHONY: migrations
migrations:
	${PY} src/manage.py makemigrations


.PHONY: su
su:
	${PY} src/manage.py createsuperuser


.PHONY: sh
sh:
	${PY} src/manage.py shell


.PHONY: truncate
truncate:
	${PY} src/manage.py truncatesessions


.PHONY: static
static:
	${PY} src/manage.py collectstatic --no-input

.PHONY: wipe
wipe: wipe-static wipe-sls


.PHONY: wipe-static
wipe-static:
	rd /s /q "${HERE}/.static/"

.PHONY: wipe-sls
wipe-sls:
	rd /s /q "${HERE}/serverless/.serverless/"