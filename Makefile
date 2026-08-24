override SHELL := /bin/sh
override COMPOSE := docker compose -f poc/docker-compose.yaml

override SITE_OUTPUT := _site
override SITE_PORT := 8008
override PYTHON := python3 -I

.PHONY: help validate validate-public-source validate-openapi validate-yaml validate-counts validate-links validate-sources validate-source-coverage validate-visuals validate-studies validate-migration-protocols validate-federated-delivery validate-workflow validate-public-content validate-site validate-site-manifest lint-shell site site-serve poc-up poc-down smoke rate-limit-test kind-up kind-down k8s-smoke

help:
	@sed -n 's/^## //p' Makefile

## validate: Run all repository checks that do not require a live cluster.
validate: validate-public-content validate-openapi validate-yaml validate-counts validate-links validate-sources validate-source-coverage validate-visuals validate-studies validate-migration-protocols validate-federated-delivery validate-workflow validate-site lint-shell

## validate-openapi: Parse every OpenAPI document and enforce key fields.
validate-openapi: validate-public-source
	@$(PYTHON) scripts/validate_openapi.py poc/apis

## validate-public-source: Reject unsafe source bytes before any parser or generator reads them.
validate-public-source:
	@$(PYTHON) scripts/study_workflow.py validate-public-content --source-only

## validate-yaml: Parse all YAML with required pinned PyYAML; fail closed when unavailable.
validate-yaml: validate-public-source
	@$(PYTHON) scripts/validate_yaml.py

## validate-counts: Enforce canonical criteria, workshop questions, and remediation-review traceability.
validate-counts: validate-public-source
	@$(PYTHON) scripts/validate_counts.py

## validate-links: Verify relative Markdown links resolve inside the repository.
validate-links: validate-public-source
	@$(PYTHON) scripts/validate_links.py

## validate-sources: Enforce unique registered sources and resolvable finding provenance.
validate-sources: validate-public-source
	@$(PYTHON) scripts/validate_sources.py

## validate-source-coverage: Enforce the registered-versus-contextual citation inventory.
validate-source-coverage: validate-public-source
	@$(PYTHON) scripts/validate_source_coverage.py

## validate-visuals: Keep architecture Mermaid mirrors and Markdown charts aligned to canonical sources.
validate-visuals: validate-public-source
	@$(PYTHON) scripts/validate_visuals.py

## validate-studies: Enforce the opt-in principal-study depth and evidence contract.
validate-studies: validate-public-source
	@$(PYTHON) scripts/validate_studies.py

## validate-migration-protocols: Self-test the Apigee migration evidence gate without claiming product execution.
validate-migration-protocols: validate-public-source
	@$(PYTHON) poc/apigee-migration/validate_evidence.py --self-test

## validate-federated-delivery: Run the offline federated-delivery governance and drift reference.
validate-federated-delivery: validate-public-source
	@$(MAKE) -C poc/federated-api-delivery check

## validate-workflow: Validate the publication workflow, reusable skill, intake template, and committed packets.
validate-workflow: site
	@$(PYTHON) scripts/study_workflow.py validate-repo
	@$(PYTHON) scripts/test_study_workflow.py

## validate-public-content: Rescan source plus generated output after the site build.
validate-public-content: site
	@$(PYTHON) scripts/study_workflow.py validate-public-content

## validate-site: Build the static research portal and verify its required entry points.
validate-site: site
	@test -s $(SITE_OUTPUT)/index.html
	@test -s $(SITE_OUTPUT)/404.html
	@test -s $(SITE_OUTPUT)/content-manifest.json
	@$(PYTHON) -m json.tool $(SITE_OUTPUT)/content-manifest.json >/dev/null
	@$(PYTHON) scripts/validate_site_manifest.py --output $(SITE_OUTPUT)

## validate-site-manifest: Validate site provenance, routes, audiences, hashes, and source mirrors.
validate-site-manifest: site
	@$(PYTHON) scripts/validate_site_manifest.py --output $(SITE_OUTPUT)

## site: Generate the API Management Studies site in _site/.
site: validate-public-source
	@$(PYTHON) scripts/build_site.py --output $(SITE_OUTPUT)

## site-serve: Build and preview the site at http://localhost:8008.
site-serve: site
	@$(PYTHON) -m http.server $(SITE_PORT) --directory $(SITE_OUTPUT)

## lint-shell: Check shell scripts when ShellCheck is available.
lint-shell: validate-public-source
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
