override PYTHON := python3 -I
override SYNTHETIC_COMMIT := 0123456789abcdef0123456789abcdef01234567

.PHONY: help check validate test demo

help:
	@sed -n 's/^## //p' Makefile

## check: Validate the reference inputs and run positive and negative offline tests.
check: validate test

## validate: Validate contract, ownership, policy, route, exception, and test inputs.
validate:
	@$(PYTHON) tools/federate.py validate --root .

## test: Run the dependency-free composition, governance, and drift test suite.
test:
	@$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

## demo: Build a reviewable synthetic configuration, provenance map, plan, and pending evidence envelope.
demo: check
	@$(PYTHON) tools/federate.py compose --root . --output .work --app-commit $(SYNTHETIC_COMMIT) --current fixtures/current-empty.json
