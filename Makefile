override SHELL := /bin/sh
override COMPOSE := docker compose -f poc/docker-compose.yaml

override SITE_OUTPUT := _site
override SITE_PORT := 8008

.PHONY: help validate validate-openapi validate-yaml validate-counts validate-links validate-sources validate-source-coverage validate-visuals validate-studies validate-workflow validate-public-content validate-site validate-site-manifest lint-shell site site-serve poc-up poc-down smoke rate-limit-test kind-up kind-down k8s-smoke

help:
	@sed -n 's/^## //p' Makefile

## validate: Run all repository checks that do not require a live cluster.
validate: validate-openapi validate-yaml validate-counts validate-links validate-sources validate-source-coverage validate-visuals validate-studies validate-workflow validate-public-content validate-site lint-shell

## validate-openapi: Parse every OpenAPI document and enforce key fields.
validate-openapi:
	@python3 scripts/validate_openapi.py poc/apis

## validate-yaml: Parse all YAML with required pinned PyYAML; fail closed when unavailable.
validate-yaml:
	@python3 scripts/validate_yaml.py

## validate-counts: Enforce canonical criteria, workshop questions, and remediation-review traceability.
validate-counts:
	@python3 scripts/validate_counts.py

## validate-links: Verify relative Markdown links resolve inside the repository.
validate-links:
	@python3 scripts/validate_links.py

## validate-sources: Enforce unique registered sources and resolvable finding provenance.
validate-sources:
	@python3 scripts/validate_sources.py

## validate-source-coverage: Enforce the registered-versus-contextual citation inventory.
validate-source-coverage:
	@python3 scripts/validate_source_coverage.py

## validate-visuals: Keep architecture Mermaid mirrors and Markdown charts aligned to canonical sources.
validate-visuals:
	@python3 scripts/validate_visuals.py

## validate-studies: Enforce the opt-in principal-study depth and evidence contract.
validate-studies:
	@python3 scripts/validate_studies.py

## validate-workflow: Validate the publication workflow, reusable skill, intake template, and committed packets.
validate-workflow: site
	@python3 scripts/study_workflow.py validate-repo
	@python3 scripts/test_study_workflow.py

## validate-public-content: Reject high-confidence secrets, local paths, and prohibited legacy branding.
validate-public-content: site
	@python3 scripts/study_workflow.py validate-public-content

## validate-site: Build the static research portal and verify its required entry points.
validate-site: site
	@test -s $(SITE_OUTPUT)/index.html
	@test -s $(SITE_OUTPUT)/404.html
	@test -s $(SITE_OUTPUT)/content-manifest.json
	@python3 -m json.tool $(SITE_OUTPUT)/content-manifest.json >/dev/null
	@python3 scripts/validate_site_manifest.py --output $(SITE_OUTPUT)

## validate-site-manifest: Validate site provenance, routes, audiences, hashes, and source mirrors.
validate-site-manifest: site
	@python3 scripts/validate_site_manifest.py --output $(SITE_OUTPUT)

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
