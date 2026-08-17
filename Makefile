SHELL := /bin/sh
COMPOSE := docker compose -f poc/docker-compose.yaml

SITE_OUTPUT := _site
SITE_PORT ?= 8008

.PHONY: help validate validate-openapi validate-yaml validate-counts validate-links validate-visuals validate-site lint-shell site site-serve poc-up poc-down smoke rate-limit-test kind-up kind-down k8s-smoke

help:
	@sed -n 's/^## //p' Makefile

## validate: Run all repository checks that do not require a live cluster.
validate: validate-openapi validate-yaml validate-counts validate-links validate-visuals validate-site lint-shell

## validate-openapi: Parse every OpenAPI document and enforce key fields.
validate-openapi:
	@python3 scripts/validate_openapi.py poc/apis

## validate-yaml: Parse YAML when PyYAML is installed; otherwise report the skipped optional check.
validate-yaml:
	@python3 scripts/validate_yaml.py

## validate-counts: Enforce the minimum 120 criteria and 180 workshop questions.
validate-counts:
	@python3 scripts/validate_counts.py

## validate-links: Verify relative Markdown links resolve inside the repository.
validate-links:
	@python3 scripts/validate_links.py

## validate-visuals: Keep architecture Mermaid mirrors and Markdown charts aligned to canonical sources.
validate-visuals:
	@python3 scripts/validate_visuals.py

## validate-site: Build the static research portal and verify its required entry points.
validate-site: site
	@test -s $(SITE_OUTPUT)/index.html
	@test -s $(SITE_OUTPUT)/404.html
	@test -s $(SITE_OUTPUT)/content-manifest.json
	@python3 -m json.tool $(SITE_OUTPUT)/content-manifest.json >/dev/null

## site: Generate the API Management Studies site in _site/.
site:
	@python3 scripts/build_site.py --output $(SITE_OUTPUT)

## site-serve: Build and preview the site at http://localhost:8008.
site-serve: site
	@python3 -m http.server $(SITE_PORT) --directory $(SITE_OUTPUT)

## lint-shell: Check shell scripts when ShellCheck is available.
lint-shell:
	@if command -v shellcheck >/dev/null 2>&1; then shellcheck scripts/*.sh; else echo 'SKIP: shellcheck unavailable'; fi

## poc-up: Start the Docker-based Kong baseline.
poc-up:
	$(COMPOSE) up --build -d
	@./scripts/wait_for_http.sh http://localhost:8000/health 90

## poc-down: Stop and remove the Docker-based baseline.
poc-down:
	$(COMPOSE) down --remove-orphans

## smoke: Run functional gateway checks against the Docker baseline.
smoke:
	@./scripts/smoke.sh http://localhost:8000

## rate-limit-test: Demonstrate the configured 429 response.
rate-limit-test:
	@./scripts/rate_limit_test.sh http://localhost:8000

## kind-up: Create the local Kubernetes PoC and leave it running.
kind-up:
	@./scripts/kind_up.sh

## kind-down: Delete only the named API platform PoC kind cluster.
kind-down:
	@./scripts/kind_down.sh

## k8s-smoke: Port-forward Kong and run the smoke test.
k8s-smoke:
	@./scripts/k8s_smoke.sh
