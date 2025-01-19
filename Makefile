.DEFAULT_GOAL := help

.PHONY: audit
audit:  ## Audit dependencies and common security issues
	python3 -m pip_audit --requirement requirements.in
	python3 -m bandit --configfile pyproject.toml --quiet --recursive .

.PHONY: install_dev
install_dev:  ## Install dev requirements and dependencies
	python3 -m pip install -r requirements.in

.PHONY: precommit
precommit:  ## Fix code formatting, linting and sorting imports
	pre-commit run --all-files

.PHONY: precommit_install
precommit_install:  ## Install pre_commit
	pre-commit install

.PHONY: precommit_update
precommit_update:  ## Update pre_commit
	pre-commit autoupdate

.PHONY: quicktest
quicktest:  ## Run tests
	python3 -m pytest --capture=no

.PHONY: test
test: audit quicktest ## Run tests

.PHONY: update
update: requirements precommit_update ## Run update

.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
