SHELL=/bin/bash
.DEFAULT_GOAL := default

.PHONY: install
install:
	@echo "---------------------------"
	@echo "- Installing dependencies -"
	@echo "---------------------------"
	python -m pip install --upgrade setuptools pip pip-tools
	python -m piptools sync requirements.txt requirements-dev.txt docs/requirements.txt
	pre-commit install

.PHONY: update
update:
	@echo "-------------------------"
	@echo "- Updating dependencies -"
	@echo "-------------------------"
	python -m piptools sync requirements.txt requirements-dev.txt docs/requirements.txt

	pip install --upgrade pip
	pip-compile
	pip-compile requirements-dev.in
	pip-compile docs/requirements.in

	python -m piptools sync requirements.txt requirements-dev.txt docs/requirements.txt

.PHONY: clean
clean:
	@echo "---------------------------"
	@echo "- Cleaning unwanted files -"
	@echo "---------------------------"
	git clean -Xdf

.PHONY: lint
lint:
	@echo "-----------------------------"
	@echo "- Run linters and formaters -"
	@echo "-----------------------------"
	SKIP=no-commit-to-branch pre-commit run --all-files

.PHONY: test
test:
	@echo "-------------"
	@echo "- Run tests -"
	@echo "-------------"
	python -m pytest ${ARGS}

.PHONY: default
default: lint test

.PHONY: pull
pull:
	@echo "------------------------"
	@echo "- Pulling last changes -"
	@echo "------------------------"
	git checkout main
	git pull

.PHONY: full
full: install pull clean update lint test

.PHONY: docs
docs:
	@echo "----------------"
	@echo "- Serving docs -"
	@echo "----------------"
	mkdocs serve --config-file docs/mkdocs.yml

.PHONY: docs-build
docs-build:
	@echo "-------------------"
	@echo "- Generating docs -"
	@echo "-------------------"
	mkdocs build --config-file docs/mkdocs.yml
