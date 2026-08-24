#!/usr/bin/env python3
"""Verify that GitHub Pages serves one clean, byte-exact repository revision."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repository_inventory import git_environment


SCHEMA_VERSION = 2
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
REVISION_PATTERN = re.compile(r"[0-9a-f]{40,64}")
GENERATED_AT_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
REQUIRED_ASSETS = {
    "index.html",
    "404.html",
    "assets/assessment.js",
    "assets/app.js",
    "assets/charts.js",
    "assets/styles.css",
    "assets/audiences.js",
}
MAX_METADATA_BYTES = 16 * 1024 * 1024
MAX_TARGET_BYTES = 64 * 1024 * 1024
STATIC_ROUTES = {
    "#/overview", "#/library", "#/compare", "#/architecture", "#/lab",
    "#/visuals", "#/audiences",
}
KONG_PLATFORM_FIT_SLIDE_KEYS = (
    "kong-platform-fit-boundary",
    "kong-platform-fit-runtime",
    "kong-platform-fit-change",
    "kong-platform-fit-fallback",
)
KONG_PLATFORM_FIT_IDS = tuple(f"KPS-FIT-{index:02d}" for index in range(1, 8))
KONG_PLATFORM_FIT_SLIDE_ROWS = {
    "kong-platform-fit-boundary": ("KPS-FIT-01", "KPS-FIT-02"),
    "kong-platform-fit-runtime": ("KPS-FIT-03", "KPS-FIT-04"),
    "kong-platform-fit-change": ("KPS-FIT-05", "KPS-FIT-06"),
    "kong-platform-fit-fallback": ("KPS-FIT-07",),
}
REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS = frozenset({"kong-platform-fit-1", "kong-platform-fit-2"})
KONG_PLATFORM_JOURNEY_DECK_ID = "kong-platform-journey"
KONG_PLATFORM_JOURNEY_SLIDE_KEYS = (
    "kong-journey-decision",
    "kong-journey-options",
    "kong-journey-selected-option",
    "kong-platform-architecture",
    "kong-technical-state-trust",
    "kong-technical-degraded-mode",
    "kong-technical-operating-model",
    "kong-platform-roadmap",
    "kong-journey-migration-boundary",
    "kong-journey-migration-coexistence",
    "kong-journey-migration-waves",
    "kong-journey-proof",
    "kong-platform-outcomes-1",
    "kong-platform-outcomes-2",
    "kong-technical-assurance",
)
KONG_PLATFORM_JOURNEY_ROLE_IDS = (
    "vp-executive", "directors", "architects", "developers", "devops-sre", "platform-teams",
)
KONG_PLATFORM_JOURNEY_SOURCE_PATHS = (
    "docs/47-kong-enterprise-platform-strategy.md",
    "docs/44-kong-multicloud-study-roadmap.md",
    "docs/35-mule-migration-strategy.md",
    "poc/README.md",
)
KONG_PLATFORM_JOURNEY_SOURCE_IDS = (
    "docs-47-kong-enterprise-platform-strategy",
    "docs-44-kong-multicloud-study-roadmap",
    "docs-35-mule-migration-strategy",
    "poc-readme",
)
KONG_PLATFORM_JOURNEY_PHASES = (
    ("01", "Options", "Fix custody, runtime, and evidence ownership", "kong-journey-decision"),
    ("02", "Architecture", "Separate management state from request execution", "kong-platform-architecture"),
    ("03", "Adoption", "Turn installation into a paved, supportable platform", "kong-technical-operating-model"),
    ("04", "Migration", "Move representative slices with route-back; retire only after dependency zero", "kong-journey-migration-boundary"),
    ("05", "Production", "Scale only accepted patterns; narrow, switch, or exit otherwise", "kong-journey-proof"),
)
KONG_GUIDED_DECK_ID = "kong-platform-journey-guided"
KONG_GUIDED_THEME = "kong-guided"
KONG_GUIDED_SLIDE_KEYS = (
    "kong-guided-cover",
    "kong-guided-target-model",
    "kong-guided-weights",
    "kong-guided-options",
    "kong-guided-score",
    "kong-guided-decision",
    "kong-guided-boundary",
    "kong-guided-duty",
    "kong-guided-architecture",
    "kong-guided-state-trust",
    "kong-guided-degraded",
    "kong-guided-operating-model",
    "kong-guided-adoption",
    "kong-guided-migration-boundary",
    "kong-guided-coexistence",
    "kong-guided-waves",
    "kong-guided-proof-boundary",
    "kong-guided-proof-programme",
    "kong-guided-outcomes-1",
    "kong-guided-outcomes-2",
    "kong-guided-assurance",
    "kong-guided-compare-architecture",
    "kong-guided-compare-management",
    "kong-guided-compare-economics",
    "kong-guided-score-audit",
)
KONG_GUIDED_ROLE_IDS = KONG_PLATFORM_JOURNEY_ROLE_IDS
KONG_GUIDED_SOURCE_PATHS = (
    "docs/48-kong-guided-evaluation.md",
    "docs/44-kong-multicloud-study-roadmap.md",
    "docs/47-kong-enterprise-platform-strategy.md",
    "docs/35-mule-migration-strategy.md",
    "research/glossary.md",
    "docs/50-apigee-migration-strategy.md",
    "poc/README.md",
)
KONG_GUIDED_SOURCE_IDS = (
    "docs-48-kong-guided-evaluation",
    "docs-44-kong-multicloud-study-roadmap",
    "docs-47-kong-enterprise-platform-strategy",
    "docs-35-mule-migration-strategy",
    "research-glossary",
    "docs-50-apigee-migration-strategy",
    "poc-readme",
)
KONG_GUIDED_ARCHITECTURE_CONTROL_IDS = (
    "gitops-trust", "kong-control-plane", "postgresql-ha",
)
KONG_GUIDED_ARCHITECTURE_LANE_IDS = (
    "cloud-a", "cloud-b", "private-legacy",
)
KONG_GUIDED_ARCHITECTURE_EDGES = (
    ("gitops-trust", "kong-control-plane", "approved-intent"),
    ("kong-control-plane", "postgresql-ha", "management-state"),
    ("kong-control-plane", "cloud-a-dp", "configuration"),
    ("kong-control-plane", "cloud-b-dp", "configuration"),
    ("kong-control-plane", "private-legacy-dp", "configuration"),
    ("cloud-a-dp", "cloud-a-services-evidence", "local-request-and-evidence"),
    ("cloud-b-dp", "cloud-b-services-evidence", "local-request-and-evidence"),
    ("private-legacy-dp", "private-legacy-services-evidence", "local-request-and-evidence"),
)
KONG_GUIDED_TARGET_IDS = tuple(f"GTM-{index:02d}" for index in range(1, 10))
KONG_GUIDED_EARLY_GATE_IDS = tuple(f"EAG-{index:02d}" for index in range(1, 5))
KONG_GUIDED_WEIGHT_IDS = tuple(f"GEW-{index:02d}" for index in range(1, 9))
KONG_GUIDED_OPTION_IDS = ("GEO-KONG", "GEO-APIGEE", "GEO-MULE", "GEO-APIM")
KONG_GUIDED_RESCORE_IDS = tuple(f"GRS-{index:02d}" for index in range(1, 7))
KONG_GUIDED_WORKSTREAM_IDS = tuple(f"GEP-{index:02d}" for index in range(1, 8))
KONG_GUIDED_SECURITY_ADJUNCT_IDS = ("GSA-01",)
KONG_GUIDED_COMPARISON_IDS = (
    (*tuple(f"GEC-{index:02d}" for index in range(1, 9)), "GEC-19"),
    (*tuple(f"GEC-{index:02d}" for index in range(9, 16)), "GEC-20"),
    tuple(f"GEC-{index:02d}" for index in range(16, 19)),
)
KONG_GUIDED_SCORE_TOTALS = {"weight": 100.0, "kong": 90.5, "apigee": 89.0, "muleSoft": 82.0}
KONG_GUIDED_DISPLAYED_TOTALS = {"kong": 90.5, "apigee": 89.0, "muleSoft": 82.0}
KONG_GUIDED_PHASES = (
    (
        "KGE-P1",
        "Why now",
        "Agree on the business priorities and four questions that could change the recommendation",
        "kong-guided-cover",
    ),
    ("KGE-P2", "Options and decision", "Compare options by outcomes and decide whether Kong earns a small first implementation", "kong-guided-options"),
    ("KGE-P3", "Architecture and adoption", "Decide who runs what, how traffic continues, and how teams adopt the platform safely", "kong-guided-architecture"),
    ("KGE-P4", "Migration", "Move MuleSoft responsibilities or Apigee in controlled waves while keeping the customer endpoint stable", "kong-guided-migration-boundary"),
    ("KGE-P5", "Production proof", "Run production-like tests for recovery, security, scale, cost, and ongoing operations", "kong-guided-proof-boundary"),
    ("KGE-P6", "Audit appendix", "Inspect the inputs and unknowns when the recommendation is challenged", "kong-guided-compare-architecture"),
)
KONG_GUIDED_IDENTIFIER_TOKENS = (
    "KGE", "EAG", "GTM", "GEW", "GRS", "GEO", "GEB", "KMC",
    "KPS", "KP", "P", "MULE", "GEP", "GSA", "KO", "GEC",
)
KONG_GUIDED_INTERNAL_DESCRIPTOR_TOKENS = KONG_GUIDED_IDENTIFIER_TOKENS[2:]
KONG_GUIDED_TERM_TOKENS = (
    ("KGE-01", ("KGE", "API", "EAG", "WAAP")),
    ("KGE-02", ("KGE", "GTM", "AKS", "AI", "TCO", "APIOps", "MCP", "A2A", "EAG")),
    ("KGE-03", ("KGE", "GEW", "GRS", "IAM", "API", "EAG", "AI", "TCO")),
    ("KGE-04", ("KGE", "API", "APIM", "CP", "PKI", "MART", "GEO", "KP-SMH1")),
    ("KGE-05", ("KGE", "GRS")),
    ("KGE-06", ("KGE", "E2", "E3", "E4", "HA", "DR", "KP-SMH1")),
    ("KGE-07", ("KGE", "GEB", "KMC", "KP-SMH1", "E1", "DP", "KPS", "API", "APIM", "CP", "PKI", "GEO")),
    ("KGE-08", ("KGE", "KPS-FIT", "API", "CP", "PKI", "E1", "DP")),
    ("KGE-09", ("KGE", "API", "CP", "DP", "PKI", "IdP", "mTLS", "DNS", "HA", "SLO", "KPS", "E1", "RBAC", "WAF", "SIEM")),
    ("KGE-10", ("KGE", "IdP", "CA", "CN", "JSON", "JWKS", "CP", "PKI", "E1", "DP", "KPS", "SIEM")),
    ("KGE-11", ("KGE", "E1", "DP", "KPS", "CP")),
    ("KGE-12", ("KGE", "DB", "SRE", "IAM", "PKI", "E1", "KPS", "API", "CP", "DP")),
    ("KGE-13", ("KGE", "KP0–KP5", "KP-SMH1", "E2", "E3", "E4", "BOM", "RACI", "GP-1–GP-6", "P1–P10", "API", "CP", "DB", "DP", "IdP", "PKI", "RBAC", "SLO")),
    ("KGE-14", ("KGE", "API", "MULE", "SFTP", "SaaS")),
    ("KGE-15", ("KGE", "AKS", "CRM", "API", "MULE")),
    ("KGE-16", ("KGE", "A0–A6", "M0–M5", "SLO", "E4", "KVM", "TLS")),
    ("KGE-17", ("KGE", "API", "PoC", "KP-SMH1", "E3", "E4", "CP", "AI", "TCO")),
    ("KGE-18", ("KGE", "API", "GEP", "GSA", "LTS", "BOM", "SBOM", "APIOps", "IAM", "MCP", "A2A", "RTO", "RPO", "RACI", "WAAP", "PoC", "TPA", "EDS", "CPU", "SSE")),
    ("KGE-19", ("KGE", "KO", "DP", "SLI", "SLO", "SRE", "OAuth", "mTLS", "IdP", "PKI", "PR", "CP", "RTO", "RPO", "IAM")),
    ("KGE-20", ("KGE", "DLP", "DNS", "KP0", "FinOps", "KO", "API", "SRE")),
    ("KGE-21", ("KGE", "KPS", "E1", "E2", "E3", "E4", "BOM", "CP")),
    ("KGE-22", ("KGE", "API", "GEC", "CP", "DP")),
    ("KGE-23", ("KGE", "AI", "GenAI", "MCP", "A2A", "E1", "API", "WAAP", "TPA", "EDS", "GEC")),
    ("KGE-24", ("KGE", "TCO", "CP", "PKI", "HA", "DR", "PAYG", "RACI", "GEC")),
    ("KGE-25", ("KGE", "E0", "GEW", "GRS", "IAM", "TCO", "CP", "API", "AI")),
)
KONG_GUIDED_ASSESSMENT_INTERFACE_TERMS = (
    ("API", "application programming interface (API)"),
    ("EAG", "Early Assessment Gate (EAG)"),
    ("APIM", "Azure API Management (APIM)"),
    ("E0", "assertion-only evidence (E0)"),
    ("E1", "current official documentation (E1)"),
    ("E2", "vendor answer with named version or contract term (E2)"),
    ("E3", "repeatable lab evidence (E3)"),
    ("E4", "representative pilot evidence (E4)"),
    ("ID", "identifier (ID)"),
    ("BOM", "bill of materials (BOM)"),
    ("JSON", "JavaScript Object Notation (JSON)"),
    ("URL", "uniform resource locator (URL)"),
    ("IP", "Internet Protocol (IP)"),
    ("IAM", "identity and access management (IAM)"),
    ("SRE", "site reliability engineering (SRE)"),
    ("FinOps", "financial operations (FinOps)"),
    ("N/A", "not applicable (N/A)"),
    ("TCO", "total cost of ownership (TCO)"),
    ("HA", "high availability (HA)"),
    ("DR", "disaster recovery (DR)"),
)
KONG_GUIDED_ASSESSMENT_SUMMARY_ROUTE = (
    "#/present/kong-platform-journey-guided/summary"
)
KONG_GUIDED_ASSESSMENT_PHASE_QUESTION_IDS = {
    "KGE-P1": (
        "KGE-P1-Q01", "KGE-P1-Q02", "KGE-P1-Q03",
        "KGE-P1-Q04", "KGE-P1-Q05", "KGE-P1-Q06",
    ),
    "KGE-P2": ("KGE-P2-Q01", "KGE-P2-Q02"),
    "KGE-P3": ("KGE-P3-Q01", "KGE-P3-Q02"),
    "KGE-P4": ("KGE-P4-Q01", "KGE-P4-Q02"),
    "KGE-P5": ("KGE-P5-Q01", "KGE-P5-Q02", "KGE-P5-Q03", "KGE-P5-Q04"),
    "KGE-P6": ("KGE-P6-Q01", "KGE-P6-Q02"),
}
KONG_GUIDED_DECISION_REFERENCE_KEYS = {
    "selectors", "label", "sourcePath", "sourceId", "sourceHeading", "decisionUse",
}
KONG_GUIDED_DECISION_REFERENCE_CANONICAL = {
    "KP-SMH1": (
        "docs/47-kong-enterprise-platform-strategy.md",
        "docs-47-kong-enterprise-platform-strategy",
        "Bounded target option and non-goals",
    ),
    "KGE-AUTH-01": (
        "docs/48-kong-guided-evaluation.md",
        "docs-48-kong-guided-evaluation",
        "Bounded authorization",
    ),
    "KGE-PROOF-01": (
        "docs/48-kong-guided-evaluation.md",
        "docs-48-kong-guided-evaluation",
        "Current proof boundary",
    ),
}
KONG_GUIDED_EARLY_QUESTION_TARGET_IDS = {
    "KGE-P1-Q02": KONG_GUIDED_TARGET_IDS,
    "KGE-P1-Q03": ("KP-SMH1", "EAG-04", "GSA-01", "GEP-07", "GEC-20"),
    "KGE-P1-Q04": ("EAG-01", "GTM-08", "GRS-01", "GEC-07"),
    "KGE-P1-Q05": ("EAG-02", "GRS-04", "GEC-16"),
    "KGE-P1-Q06": ("EAG-03", "GEW-08", "GRS-05", "GEC-17"),
}
KONG_GUIDED_PHASE_BY_KEY = {
    key: phase_id
    for phase_id, keys in (
        ("KGE-P1", KONG_GUIDED_SLIDE_KEYS[0:3]),
        ("KGE-P2", KONG_GUIDED_SLIDE_KEYS[3:8]),
        ("KGE-P3", KONG_GUIDED_SLIDE_KEYS[8:13]),
        ("KGE-P4", KONG_GUIDED_SLIDE_KEYS[13:16]),
        ("KGE-P5", KONG_GUIDED_SLIDE_KEYS[16:21]),
        ("KGE-P6", KONG_GUIDED_SLIDE_KEYS[21:25]),
    )
    for key in keys
}
KONG_GUIDED_POINT_SOURCE_BY_KEY = {
    **{key: KONG_GUIDED_SOURCE_IDS[0] for key in KONG_GUIDED_SLIDE_KEYS},
    "kong-guided-boundary": KONG_GUIDED_SOURCE_IDS[1],
    **{key: KONG_GUIDED_SOURCE_IDS[2] for key in KONG_GUIDED_SLIDE_KEYS[7:13]},
    **{key: KONG_GUIDED_SOURCE_IDS[3] for key in KONG_GUIDED_SLIDE_KEYS[13:16]},
    "kong-guided-waves": KONG_GUIDED_SOURCE_IDS[5],
    "kong-guided-proof-boundary": KONG_GUIDED_SOURCE_IDS[6],
    **{key: KONG_GUIDED_SOURCE_IDS[2] for key in KONG_GUIDED_SLIDE_KEYS[18:21]},
}
KONG_GUIDED_EVIDENCE_GROUPS = (
    (("KGE-01",), "Guided decision brief", "Mixed public-safe synthesis", "Orientation only; no new evidence"),
    (
        ("KGE-02", "KGE-03"),
        "Stakeholder input plus early-gate contract",
        "Sanitized supplied input plus repository decision design",
        "Target preferences, weighting choices, and EAG-01 – EAG-04 admission questions; gate disposition creates evidence work but is not candidate proof or a product score",
    ),
    (("KGE-04",), "Conditional hypothesis", "Supplied input plus documented-mechanism interpretation", "Conditional operating-model archetypes to test; not an observed product comparison"),
    (("KGE-05",), "Provisional scenario over stakeholder input", "Sanitized supplied input plus mechanical uncertainty calculation", "Historical totals remain audit input; overlapping ranges are a HOLD signal, not product evidence"),
    (("KGE-06",), "Bounded direction", "Stakeholder direction plus repository interpretation", "Authorizes foundation and proof only"),
    (("KGE-07", "KGE-08", "KGE-09", "KGE-10", "KGE-11", "KGE-12"), "Proposed target", "Repository E1 interpretation", "Operating options, architecture, failure policy, and ownership to prove"),
    (("KGE-13",), "Scenario assumption", "Repository adoption plan", "Overlapping decision windows, not status or commitment"),
    (("KGE-14", "KGE-15", "KGE-16"), "Proposed migration model", "Repository Mule and Apigee migration interpretations", "No observed estate classification, coexistence result, route-back, or migration status"),
    (("KGE-17",), "Executed local baseline", "Canonical PoC register as of 2026-08-20", "Exact local-baseline counts; not representative target proof"),
    (("KGE-18",), "Not run", "Meeting direction canonicalized as GEP-01–GEP-07", "Required future proof work only; Traceable remains an adjunct hypothesis"),
    (("KGE-19", "KGE-20", "KGE-21"), "Proposed acceptance contract", "Repository outcome and assurance design", "Measures, artifacts, and decisions, not achieved outcomes"),
    (("KGE-22",), "Stakeholder input", "Sanitized supplied input plus repository evidence obligations", "Architecture/delivery labels remain unverified; scalability and robustness are explicitly unscored"),
    (("KGE-23",), "Mixed documented mechanism and stakeholder input", "Sanitized supplied input plus current official Traceable/Kong documentation", "Traceable is E1 feasibility only; management, experience and AI labels remain unverified"),
    (("KGE-24",), "Stakeholder input with documented pricing boundaries", "Sanitized supplied input plus current official pricing pages", "No normalized quote, TCO, control-duty, adjunct-cost, lock-in or exit result"),
    (("KGE-25",), "Provisional scenario over stakeholder input", "Sanitized supplied input plus provisional weighting and uncertainty specification", "Historical ratings remain E0; GRS ratings remain unknown; overlapping envelopes force HOLD"),
)
KONG_GUIDED_REFERENCE_GROUPS = (
    (("KGE-01", "KGE-02", "KGE-03"), (
        "https://developer.konghq.com/gateway/deployment-topologies/",
        "https://developer.konghq.com/gateway/hybrid-mode/",
        "https://docs.traceable.ai/kong",
        "https://developer.konghq.com/plugins/harness-waap/",
        "https://konghq.com/pricing",
    )),
    (("KGE-04", "KGE-05"), (
        "https://developer.konghq.com/gateway/deployment-topologies/",
        "https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid",
        "https://docs.mulesoft.com/gateway/latest/",
        "https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview",
    )),
    (("KGE-06", "KGE-07", "KGE-08"), (
        "https://developer.konghq.com/gateway/hybrid-mode/",
        "https://developer.konghq.com/gateway/version-support-policy/",
    )),
    (("KGE-09", "KGE-10", "KGE-11", "KGE-12", "KGE-13"), (
        "https://developer.konghq.com/gateway/hybrid-mode/",
        "https://developer.konghq.com/gateway/monitoring/",
    )),
    (("KGE-14", "KGE-15", "KGE-16"), (
        "https://docs.mulesoft.com/gateway/latest/",
        "https://developer.konghq.com/gateway/entities/",
        "https://developer.konghq.com/gateway/entities/plugin/",
        "https://developer.konghq.com/gateway/deployment-topologies/",
        "https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/download-api-proxies",
        "https://docs.cloud.google.com/apigee/docs/api-platform/reference/api-proxy-configuration-reference",
    )),
    (("KGE-17",), (
        "https://developer.konghq.com/gateway/hybrid-mode/",
        "https://developer.konghq.com/gateway/monitoring/",
    )),
    (("KGE-18",), (
        "https://developer.konghq.com/gateway/version-support-policy/",
        "https://developer.konghq.com/gateway/hybrid-mode/",
        "https://developer.konghq.com/gateway/monitoring/",
        "https://developer.konghq.com/ai-gateway/",
        "https://docs.traceable.ai/kong",
        "https://developer.konghq.com/plugins/harness-waap/",
    )),
    (("KGE-19", "KGE-20", "KGE-21"), (
        "https://developer.konghq.com/gateway/hybrid-mode/",
        "https://developer.konghq.com/gateway/monitoring/",
        "https://developer.konghq.com/ai-gateway/",
    )),
    (("KGE-22",), (
        "https://developer.konghq.com/gateway/deployment-topologies/",
        "https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid",
        "https://docs.mulesoft.com/gateway/latest/",
        "https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview",
    )),
    (("KGE-23",), (
        "https://developer.konghq.com/ai-gateway/",
        "https://docs.traceable.ai/kong",
        "https://developer.konghq.com/plugins/harness-waap/",
        "https://docs.traceable.ai/docs/tracing-agents-rule-evaluation-for-protection",
    )),
    (("KGE-24", "KGE-25"), (
        "https://konghq.com/pricing",
        "https://cloud.google.com/apigee/pricing",
        "https://www.mulesoft.com/anypoint-pricing",
        "https://developer.konghq.com/gateway/deployment-topologies/",
    )),
)
KONG_TECHNICAL_DEEP_DIVE_SLIDE_KEYS = (
    "decision",
    *KONG_PLATFORM_FIT_SLIDE_KEYS,
    "kong-platform-architecture",
    "kong-technical-state-trust",
    "kong-technical-operating-model",
    "kong-technical-degraded-mode",
    "kong-platform-cases-1",
    "kong-platform-cases-2",
    "kong-technical-evidence-path",
    "kong-platform-outcomes-1",
    "kong-platform-outcomes-2",
    "kong-technical-assurance",
)
KONG_TECHNICAL_DEEP_DIVE_ROLE_IDS = ("architects", "devops-sre", "platform-teams")
KONG_GUIDED_PRIVATE_PATH_PATTERN = re.compile(
    r"(?:file://|/" r"Users/|/var/" r"folders/|/private/" r"var/|[A-Za-z]:\\\\|\.docx(?:\b|$))",
    re.IGNORECASE,
)
KONG_MULTICLOUD_OPTION_IDS = (
    "KMC-1", "KMC-2", "KMC-3", "KMC-4A", "KMC-4B", "KMC-5", "KMC-6", "KMC-7",
)
MULE_MIGRATION_SOURCE_PATH = "docs/35-mule-migration-strategy.md"
MULE_MIGRATION_SOURCE_ID = "docs-35-mule-migration-strategy"
MULE_RESPONSIBILITY_IDS = ("G", "F", "T", "O", "M", "B", "C", "R")
MULE_WAVE_IDS = tuple(f"M{index}" for index in range(6))
APIGEE_MIGRATION_SOURCE_PATH = "docs/50-apigee-migration-strategy.md"
APIGEE_MIGRATION_SOURCE_ID = "docs-50-apigee-migration-strategy"
APIGEE_MIGRATION_PHASE_IDS = tuple(f"A{index}" for index in range(7))
APIGEE_MIGRATION_COLUMNS = (
    "Phase",
    "Audience-facing purpose",
    "Required work",
    "Exit evidence",
    "Hold or route-back signal",
)
MULE_FIGURE_HEADINGS = {
    "MULE-2": "Mechanism analysis: decompose before selecting a target",
    "MULE-3": "Target coexistence architecture",
    "MULE-6": "Migration waves",
}
POC_STATUS_COUNTS = {"Automated": 5, "Not run": 11}
POC_STATUS_BY_ID = {
    **{f"POC-{index:03d}": "Automated" for index in range(1, 6)},
    "POC-006": "Not run",
    **{f"POC-{index}": "Not run" for index in range(101, 111)},
}
POC_TEST_IDS = tuple(POC_STATUS_BY_ID)
CRITERIA_STATUS_COUNTS = {"Unknown": 120}
CRITERIA_CATEGORY_COUNTS = {
    "architecture": (3, 7),
    "security": (7, 3),
    "network": (2, 8),
    "kubernetes": (2, 8),
    "api-lifecycle": (1, 9),
    "apiops": (3, 7),
    "traffic-policy": (1, 9),
    "observability": (1, 9),
    "resilience-performance": (3, 7),
    "operations-support": (2, 8),
    "mule-migration": (2, 8),
    "commercial-strategy": (3, 7),
}
ROOT = Path(__file__).resolve().parents[1]


class VerificationError(RuntimeError):
    """The deployed Pages artifact does not match its provenance contract."""


@dataclass(frozen=True)
class Target:
    relative: str
    sha256: str
    size: int
    label: str


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def validate_journey_phase_starts(deck: dict[str, Any], selected_slides: list[str], label: str) -> None:
    """Ensure every deployed phase resolves to one ordered route inside its deck."""
    phases = deck.get("journeyPhases", [])
    require(isinstance(phases, list), f"{label} journeyPhases must be a list")
    if not phases:
        return
    require(all(isinstance(phase, dict) for phase in phases), f"{label} journey phases must be objects")
    phase_ids = [phase.get("id") for phase in phases]
    start_keys = [phase.get("startKey") for phase in phases]
    require(all(isinstance(phase_id, str) and phase_id for phase_id in phase_ids), f"{label} journey phase IDs must be non-empty strings")
    require(all(isinstance(start_key, str) and start_key for start_key in start_keys), f"{label} journey phase startKeys must be non-empty strings")
    require(len(phase_ids) == len(set(phase_ids)), f"{label} journey phase IDs contain duplicate values")
    require(len(start_keys) == len(set(start_keys)), f"{label} journey phase startKeys contain duplicate values")
    require(all(start_key in selected_slides for start_key in start_keys), f"{label} journey phase startKeys must reference selected slides")
    start_indices = [selected_slides.index(start_key) for start_key in start_keys]
    require(start_indices[0] == 0, f"{label} journey phases must begin with the first selected slide")
    require(start_indices == sorted(start_indices), f"{label} journey phase starts must increase strictly")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    file_digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            file_digest.update(chunk)
    return file_digest.hexdigest()


def validate_poc_projection(manifest: dict[str, Any]) -> None:
    """Bind the deployed PoC visual to the canonical aggregate status register."""
    visuals = manifest.get("visuals")
    require(isinstance(visuals, dict), "manifest visuals must be an object")
    poc = visuals.get("poc")
    require(isinstance(poc, dict), "manifest visuals.poc must be an object")

    total = poc.get("total")
    require(type(total) is int and total > 0, "manifest visuals.poc.total must be a positive integer")

    by_status = poc.get("byStatus")
    require(isinstance(by_status, list) and bool(by_status), "manifest visuals.poc.byStatus must be a non-empty list")
    require(all(isinstance(item, dict) for item in by_status), "manifest visuals.poc.byStatus entries must be objects")
    status_labels: list[str] = []
    status_counts: list[int] = []
    for item in by_status:
        label = item.get("label")
        value = item.get("value")
        require(isinstance(label, str) and bool(label), "manifest visuals.poc.byStatus labels must be non-empty strings")
        require(type(value) is int and value >= 0, f"manifest visuals.poc.byStatus value for {label} must be a non-negative integer")
        status_labels.append(label)
        status_counts.append(value)
    require(
        len(status_labels) == len(set(status_labels)),
        "manifest visuals.poc.byStatus labels must be unique",
    )
    require(
        sum(status_counts) == total,
        "manifest visuals.poc.byStatus counts must sum to visuals.poc.total",
    )
    declared_statuses = dict(zip(status_labels, status_counts))
    require(
        declared_statuses == POC_STATUS_COUNTS,
        "manifest visuals.poc.byStatus must be exactly Automated=5 and Not run=11",
    )

    tests = poc.get("tests")
    require(isinstance(tests, list), "manifest visuals.poc.tests must be a list")
    require(len(tests) == total, "manifest visuals.poc.tests length must equal visuals.poc.total")
    require(all(isinstance(test, dict) for test in tests), "manifest visuals.poc.tests entries must be objects")
    test_ids: list[str] = []
    test_statuses: list[str] = []
    for test in tests:
        test_id = test.get("id")
        status = test.get("status")
        require(isinstance(test_id, str) and bool(test_id), "manifest visuals.poc.tests IDs must be non-empty strings")
        require(
            isinstance(status, str) and status in declared_statuses,
            f"manifest visuals.poc.tests status for {test_id} is undeclared",
        )
        test_ids.append(test_id)
        test_statuses.append(status)
    require(len(test_ids) == len(set(test_ids)), "manifest visuals.poc.tests IDs must be unique")
    require(
        len(test_ids) == len(POC_TEST_IDS) and set(test_ids) == set(POC_TEST_IDS),
        "manifest visuals.poc.tests IDs must be exactly POC-001 through POC-006 and POC-101 through POC-110",
    )
    observed_statuses = {
        label: sum(status == label for status in test_statuses)
        for label in declared_statuses
    }
    require(
        observed_statuses == declared_statuses,
        "manifest visuals.poc.tests status counts must match visuals.poc.byStatus",
    )
    require(
        dict(zip(test_ids, test_statuses)) == POC_STATUS_BY_ID,
        "manifest visuals.poc.tests must preserve the canonical ID-to-status assignments",
    )


def validate_criteria_projection(manifest: dict[str, Any]) -> None:
    """Mirror the local criteria evidence/composition contract on deployed Pages."""
    visuals = manifest.get("visuals")
    require(isinstance(visuals, dict), "manifest visuals must be an object")
    criteria = visuals.get("criteria")
    require(isinstance(criteria, dict), "manifest visuals.criteria must be an object")
    require(criteria.get("total") == 120, "manifest visuals.criteria.total must be exactly 120")
    require(criteria.get("mandatory") == 30, "manifest visuals.criteria.mandatory must be exactly 30")
    require(criteria.get("weighted") == 90, "manifest visuals.criteria.weighted must be exactly 90")

    statuses = criteria.get("statuses")
    require(isinstance(statuses, list) and bool(statuses), "manifest visuals.criteria.statuses must be a non-empty list")
    require(all(isinstance(item, dict) for item in statuses), "manifest visuals.criteria.statuses entries must be objects")
    observed_statuses = {item.get("label"): item.get("value") for item in statuses}
    require(observed_statuses == CRITERIA_STATUS_COUNTS, "manifest visuals.criteria.statuses must be exactly Unknown=120")

    categories = criteria.get("categories")
    require(isinstance(categories, list), "manifest visuals.criteria.categories must be a list")
    require(all(isinstance(row, dict) for row in categories), "manifest visuals.criteria.categories entries must be objects")
    observed_categories: dict[str, tuple[int, int]] = {}
    for row in categories:
        category_id = row.get("id")
        mandatory = row.get("mandatory")
        weighted = row.get("weighted")
        total_value = row.get("total")
        require(isinstance(category_id, str) and bool(category_id), "manifest visuals.criteria category IDs must be non-empty strings")
        require(type(mandatory) is int and mandatory >= 0, f"manifest visuals.criteria {category_id} mandatory count is invalid")
        require(type(weighted) is int and weighted >= 0, f"manifest visuals.criteria {category_id} weighted count is invalid")
        require(total_value == mandatory + weighted, f"manifest visuals.criteria {category_id} total must equal mandatory plus weighted")
        observed_categories[category_id] = (mandatory, weighted)
    require(observed_categories == CRITERIA_CATEGORY_COUNTS, "manifest visuals.criteria category composition is not canonical")


def validate_kong_platform_fit_slides(
    manifest: dict[str, Any],
    presentation: list[dict[str, Any]],
) -> None:
    """Bind every deployed Kong fit slide to the canonical seven-row projection."""
    visuals = manifest.get("visuals")
    require(isinstance(visuals, dict), "manifest visuals must be an object")
    strategy = visuals.get("kongPlatformStrategy")
    require(isinstance(strategy, dict), "manifest visuals.kongPlatformStrategy must be an object")
    fit = strategy.get("fit")
    require(isinstance(fit, dict), "manifest visuals.kongPlatformStrategy.fit must be an object")
    rows = fit.get("rows")
    require(isinstance(rows, list) and bool(rows), "manifest canonical Kong platform fit rows must be a non-empty list")
    require(all(isinstance(row, dict) for row in rows), "manifest canonical Kong platform fit rows must be objects")
    canonical_ids = [row.get("projectionId") for row in rows]
    require(
        all(isinstance(row_id, str) and row_id for row_id in canonical_ids),
        "manifest canonical Kong platform fit IDs must be non-empty strings",
    )
    require(
        len(canonical_ids) == len(set(canonical_ids)),
        "manifest canonical Kong platform fit IDs must be unique",
    )
    require(
        len(canonical_ids) == len(KONG_PLATFORM_FIT_IDS)
        and set(canonical_ids) == set(KONG_PLATFORM_FIT_IDS),
        "manifest canonical Kong platform fit IDs must be exactly KPS-FIT-01 through KPS-FIT-07",
    )

    slides_by_key = {slide["key"]: slide for slide in presentation}
    require(
        not REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS.intersection(slides_by_key),
        "manifest presentation retains a removed Kong platform fit slide",
    )
    fit_slide_keys = {
        slide["key"]
        for slide in presentation
        if slide.get("visual") == "kongPlatformFit"
    }
    require(
        fit_slide_keys == set(KONG_PLATFORM_FIT_SLIDE_KEYS),
        "manifest Kong platform fit slides must be exactly the four semantic fit slide keys",
    )
    require(
        all(key in slides_by_key for key in KONG_PLATFORM_FIT_SLIDE_KEYS),
        "manifest presentation must contain the four semantic Kong platform fit slides",
    )
    for key in KONG_PLATFORM_FIT_SLIDE_KEYS:
        require(
            slides_by_key[key].get("visual") == "kongPlatformFit",
            f"manifest slide {key} must use the kongPlatformFit visual",
        )
        require(
            tuple(slides_by_key[key].get("rowIds", ())) == KONG_PLATFORM_FIT_SLIDE_ROWS[key],
            f"manifest slide {key} rowIds do not match its bounded Kong fit contract",
        )

    canonical_id_set = set(canonical_ids)
    for slide in presentation:
        if slide.get("visual") != "kongPlatformFit":
            continue
        key = slide["key"]
        row_ids = slide.get("rowIds")
        require(isinstance(row_ids, list) and bool(row_ids), f"manifest slide {key} rowIds must be a non-empty list")
        require(
            all(isinstance(row_id, str) and row_id for row_id in row_ids),
            f"manifest slide {key} rowIds must be non-empty strings",
        )
        require(len(row_ids) == len(set(row_ids)), f"manifest slide {key} rowIds must be unique")
        require(
            set(row_ids).issubset(canonical_id_set),
            f"manifest slide {key} rowIds reference an unknown canonical Kong platform fit ID",
        )

    semantic_row_ids = [
        row_id
        for key in KONG_PLATFORM_FIT_SLIDE_KEYS
        for row_id in slides_by_key[key]["rowIds"]
    ]
    require(
        len(semantic_row_ids) == len(KONG_PLATFORM_FIT_IDS)
        and set(semantic_row_ids) == set(KONG_PLATFORM_FIT_IDS),
        "manifest semantic Kong platform fit slides must cover KPS-FIT-01 through KPS-FIT-07 exactly once",
    )


def validate_kong_platform_journey(
    manifest: dict[str, Any],
    presentation: list[dict[str, Any]],
) -> None:
    """Bind the deployed Kong journey to its exact narrative and evidence payload."""
    decks = manifest.get("presentationDecks")
    require(isinstance(decks, list), "manifest presentationDecks must be a list")
    matches = [
        deck for deck in decks
        if isinstance(deck, dict) and deck.get("id") == KONG_PLATFORM_JOURNEY_DECK_ID
    ]
    require(
        len(matches) == 1,
        "manifest presentationDecks must contain exactly one kong-platform-journey deck",
    )
    deck = matches[0]
    require(deck.get("theme") == "kong-journey", "manifest Kong platform journey theme must be kong-journey")
    require(
        tuple(deck.get("presentationSlides", ())) == KONG_PLATFORM_JOURNEY_SLIDE_KEYS,
        "manifest Kong platform journey slides must match the exact 15-slide journey order",
    )
    require(deck.get("slideTotal") == 15, "manifest Kong platform journey slideTotal must be 15")
    require(
        tuple(deck.get("audienceRoleIds", ())) == KONG_PLATFORM_JOURNEY_ROLE_IDS,
        "manifest Kong platform journey audienceRoleIds must match the exact six-role order",
    )
    require(
        tuple(deck.get("sourcePaths", ())) == KONG_PLATFORM_JOURNEY_SOURCE_PATHS,
        "manifest Kong platform journey sourcePaths must match the exact canonical source order",
    )
    require(
        tuple(deck.get("sourceIds", ())) == KONG_PLATFORM_JOURNEY_SOURCE_IDS,
        "manifest Kong platform journey sourceIds must match the exact canonical source order",
    )
    require(
        deck.get("presentationRoute") == "#/present/kong-platform-journey/0",
        "manifest Kong platform journey presentationRoute is invalid",
    )
    require(deck.get("exitRoute") == "#/overview", "manifest Kong platform journey exitRoute must be #/overview")
    phases = deck.get("journeyPhases")
    require(isinstance(phases, list), "manifest Kong platform journey journeyPhases must be a list")
    observed_phases = tuple(
        (phase.get("id"), phase.get("label"), phase.get("outcome"), phase.get("startKey"))
        for phase in phases
        if isinstance(phase, dict)
    )
    require(
        len(observed_phases) == len(phases) and observed_phases == KONG_PLATFORM_JOURNEY_PHASES,
        "manifest Kong platform journey phases must match the exact five-stage spine and start keys",
    )

    slides_by_key = {slide.get("key"): slide for slide in presentation if isinstance(slide, dict)}
    require(
        all(key in slides_by_key for key in KONG_PLATFORM_JOURNEY_SLIDE_KEYS),
        "manifest Kong platform journey references a missing presentation slide",
    )
    expected_source_ids = {
        key: "docs-47-kong-enterprise-platform-strategy"
        for key in KONG_PLATFORM_JOURNEY_SLIDE_KEYS
    }
    expected_source_ids["kong-journey-options"] = "docs-44-kong-multicloud-study-roadmap"
    for key in (
        "kong-journey-migration-boundary",
        "kong-journey-migration-coexistence",
        "kong-journey-migration-waves",
    ):
        expected_source_ids[key] = MULE_MIGRATION_SOURCE_ID
    expected_source_ids["kong-journey-proof"] = "poc-readme"
    require(
        all(slides_by_key[key].get("sourceId") == expected_source_ids[key] for key in KONG_PLATFORM_JOURNEY_SLIDE_KEYS),
        "manifest Kong platform journey slides must preserve their exact canonical source coverage",
    )

    decision_slide = slides_by_key["kong-journey-decision"]
    require(
        decision_slide.get("visual") == "kongJourneySpine",
        "manifest Kong journey decision slide must use kongJourneySpine",
    )
    roadmap_slide = slides_by_key["kong-platform-roadmap"]
    require(
        roadmap_slide.get("visual") == "kongPlatformRoadmap",
        "manifest Kong platform roadmap slide must use kongPlatformRoadmap",
    )

    options_slide = slides_by_key["kong-journey-options"]
    require(options_slide.get("visual") == "kongOptions", "manifest Kong options slide must use kongOptions")
    require(
        tuple(options_slide.get("optionIds", ())) == KONG_MULTICLOUD_OPTION_IDS,
        "manifest Kong options slide optionIds must match the exact KMC option order",
    )
    selected_slide = slides_by_key["kong-journey-selected-option"]
    require(
        selected_slide.get("visual") == "kongSelectedOption",
        "manifest Kong selected-option slide must use kongSelectedOption",
    )
    require(
        tuple(selected_slide.get("rowIds", ())) == ("KPS-FIT-01", "KPS-FIT-02"),
        "manifest Kong selected-option slide rowIds must be KPS-FIT-01 and KPS-FIT-02",
    )
    proof_slide = slides_by_key["kong-journey-proof"]
    require(
        proof_slide.get("visual") == "pocStatus",
        "manifest Kong journey proof slide must use the canonical pocStatus visual",
    )
    required_migration_slides = {
        "kong-journey-migration-boundary": ("muleMigrationBoundary", None),
        "kong-journey-migration-coexistence": ("muleMigrationFigure", "MULE-3"),
        "kong-journey-migration-waves": ("muleMigrationWaves", None),
    }
    for key, (visual, figure_id) in required_migration_slides.items():
        slide = slides_by_key[key]
        require(slide.get("visual") == visual, f"manifest slide {key} must use {visual}")
        if figure_id is not None:
            require(slide.get("figureId") == figure_id, f"manifest slide {key} must use figure {figure_id}")

    visuals = manifest.get("visuals")
    require(isinstance(visuals, dict), "manifest visuals must be an object")
    multicloud = visuals.get("kongMulticloud")
    require(isinstance(multicloud, dict), "manifest visuals.kongMulticloud must be an object")
    options = multicloud.get("options")
    require(isinstance(options, list), "manifest visuals.kongMulticloud.options must be a list")
    require(all(isinstance(option, dict) for option in options), "manifest Kong multicloud options must be objects")
    require(
        tuple(option.get("id") for option in options) == KONG_MULTICLOUD_OPTION_IDS,
        "manifest Kong multicloud option IDs must match the exact KMC option order",
    )
    for option in options:
        require(
            all(isinstance(option.get(field), str) and option[field].strip() for field in ("label", "placement", "role", "journeyLabel")),
            f"manifest Kong multicloud option {option.get('id')} must retain label, placement, role, and journeyLabel evidence",
        )
    for option in options[:3]:
        require(
            all(isinstance(option.get(field), str) and option[field].strip() for field in ("journeyBoundary", "journeyRole")),
            f"manifest primary Kong multicloud option {option.get('id')} must retain journeyBoundary and journeyRole evidence",
        )

    mule = visuals.get("muleMigration")
    require(isinstance(mule, dict), "manifest visuals.muleMigration must be an object")
    require(mule.get("sourcePath") == MULE_MIGRATION_SOURCE_PATH, "manifest Mule migration sourcePath is invalid")
    require(mule.get("sourceId") == MULE_MIGRATION_SOURCE_ID, "manifest Mule migration sourceId is invalid")

    responsibilities = mule.get("responsibilities")
    require(isinstance(responsibilities, list), "manifest Mule migration responsibilities must be a list")
    require(mule.get("responsibilityTotal") == len(MULE_RESPONSIBILITY_IDS), "manifest Mule responsibilityTotal is invalid")
    require(all(isinstance(row, dict) for row in responsibilities), "manifest Mule responsibilities must be objects")
    require(
        tuple(row.get("id") for row in responsibilities) == MULE_RESPONSIBILITY_IDS,
        "manifest Mule responsibility IDs must match the exact G/F/T/O/M/B/C/R order",
    )
    for row in responsibilities:
        require(
            all(isinstance(row.get(field), str) and row[field].strip() for field in ("responsibility", "target", "evidence", "error")),
            f"manifest Mule responsibility {row.get('id')} must retain every canonical evidence field",
        )
    responsibility_provenance = mule.get("responsibilityProvenance")
    require(isinstance(responsibility_provenance, dict), "manifest Mule responsibility provenance must be an object")
    require(
        (
            responsibility_provenance.get("sourcePath"),
            responsibility_provenance.get("sourceId"),
            tuple(responsibility_provenance.get("sourcePaths", ())),
            tuple(responsibility_provenance.get("sourceIds", ())),
            responsibility_provenance.get("sourceHeading"),
            tuple(responsibility_provenance.get("tableColumns", ())),
        )
        == (
            MULE_MIGRATION_SOURCE_PATH,
            MULE_MIGRATION_SOURCE_ID,
            (MULE_MIGRATION_SOURCE_PATH,),
            (MULE_MIGRATION_SOURCE_ID,),
            "Mechanism analysis: decompose before selecting a target",
            ("Class", "Responsibility", "Default target", "Evidence needed", "Common error"),
        ),
        "manifest Mule responsibility provenance must match the exact canonical table",
    )

    waves = mule.get("waves")
    require(isinstance(waves, list), "manifest Mule migration waves must be a list")
    require(mule.get("waveTotal") == len(MULE_WAVE_IDS), "manifest Mule waveTotal is invalid")
    require(all(isinstance(wave, dict) for wave in waves), "manifest Mule migration waves must be objects")
    require(
        tuple(wave.get("id") for wave in waves) == MULE_WAVE_IDS,
        "manifest Mule migration wave IDs must match the exact M0 through M5 order",
    )
    for wave in waves:
        require(
            all(isinstance(wave.get(field), str) and wave[field].strip() for field in ("label", "scope", "pattern", "entryGate", "exitGate")),
            f"manifest Mule migration wave {wave.get('id')} must retain every canonical evidence field",
        )
    wave_provenance = mule.get("waveProvenance")
    require(isinstance(wave_provenance, dict), "manifest Mule wave provenance must be an object")
    require(
        (
            wave_provenance.get("sourcePath"),
            wave_provenance.get("sourceId"),
            tuple(wave_provenance.get("sourcePaths", ())),
            tuple(wave_provenance.get("sourceIds", ())),
            wave_provenance.get("sourceHeading"),
            tuple(wave_provenance.get("tableColumns", ())),
        )
        == (
            MULE_MIGRATION_SOURCE_PATH,
            MULE_MIGRATION_SOURCE_ID,
            (MULE_MIGRATION_SOURCE_PATH,),
            (MULE_MIGRATION_SOURCE_ID,),
            "Migration waves",
            ("Wave", "Assumed scope", "Hard pattern intentionally included", "Entry gate", "Exit gate"),
        ),
        "manifest Mule wave provenance must match the exact canonical table",
    )

    figures = mule.get("figures")
    require(isinstance(figures, list), "manifest Mule migration figures must be a list")
    require(all(isinstance(figure, dict) for figure in figures), "manifest Mule migration figures must be objects")
    require(
        tuple(figure.get("figureId") for figure in figures) == tuple(MULE_FIGURE_HEADINGS),
        "manifest Mule figure IDs must match the exact MULE-2/MULE-3/MULE-6 order",
    )
    for figure in figures:
        figure_id = figure["figureId"]
        require(
            all(isinstance(figure.get(field), str) and figure[field].strip() for field in ("title", "mermaid")),
            f"manifest Mule figure {figure_id} must retain title and Mermaid source",
        )
        provenance = figure.get("provenance")
        require(isinstance(provenance, dict), f"manifest Mule figure {figure_id} provenance must be an object")
        require(
            (
                provenance.get("sourcePath"),
                provenance.get("sourceId"),
                tuple(provenance.get("sourcePaths", ())),
                tuple(provenance.get("sourceIds", ())),
                provenance.get("sourceHeading"),
                provenance.get("figureId"),
            )
            == (
                MULE_MIGRATION_SOURCE_PATH,
                MULE_MIGRATION_SOURCE_ID,
                (MULE_MIGRATION_SOURCE_PATH,),
                (MULE_MIGRATION_SOURCE_ID,),
                MULE_FIGURE_HEADINGS[figure_id],
                figure_id,
            ),
            f"manifest Mule figure {figure_id} provenance must match its exact canonical figure",
        )

    apigee = visuals.get("apigeeMigration")
    require(isinstance(apigee, dict), "manifest visuals.apigeeMigration must be an object")
    require(apigee.get("sourcePath") == APIGEE_MIGRATION_SOURCE_PATH, "manifest Apigee migration sourcePath is invalid")
    require(apigee.get("sourceId") == APIGEE_MIGRATION_SOURCE_ID, "manifest Apigee migration sourceId is invalid")
    phases = apigee.get("phases")
    require(isinstance(phases, list), "manifest Apigee migration phases must be a list")
    require(apigee.get("phaseTotal") == len(APIGEE_MIGRATION_PHASE_IDS), "manifest Apigee migration phaseTotal must be seven")
    require(all(isinstance(phase, dict) for phase in phases), "manifest Apigee migration phases must be objects")
    require(
        tuple(phase.get("id") for phase in phases) == APIGEE_MIGRATION_PHASE_IDS,
        "manifest Apigee migration phase IDs must match the exact A0 through A6 order",
    )
    for phase in phases:
        require(
            all(
                isinstance(phase.get(field), str) and phase[field].strip()
                for field in ("label", "purpose", "work", "exitEvidence", "hold")
            ),
            f"manifest Apigee migration phase {phase.get('id')} must retain every canonical evidence field",
        )
    apigee_provenance = apigee.get("provenance")
    require(isinstance(apigee_provenance, dict), "manifest Apigee migration provenance must be an object")
    require(
        (
            apigee_provenance.get("sourcePath"),
            apigee_provenance.get("sourceId"),
            tuple(apigee_provenance.get("sourcePaths", ())),
            tuple(apigee_provenance.get("sourceIds", ())),
            apigee_provenance.get("sourceHeading"),
            tuple(apigee_provenance.get("tableColumns", ())),
        )
        == (
            APIGEE_MIGRATION_SOURCE_PATH,
            APIGEE_MIGRATION_SOURCE_ID,
            (APIGEE_MIGRATION_SOURCE_PATH,),
            (APIGEE_MIGRATION_SOURCE_ID,),
            "Proposed A0–A6 migration roadmap",
            APIGEE_MIGRATION_COLUMNS,
        ),
        "manifest Apigee migration provenance must match the exact canonical A0–A6 table",
    )


def validate_kong_guided_evaluation(
    manifest: dict[str, Any],
    presentation: list[dict[str, Any]],
) -> None:
    """Run the same fail-closed guided-deck contract against deployed Pages."""
    try:
        from validate_site_manifest import (
            ValidationError as LocalValidationError,
            validate_kong_guided_evaluation as validate_local_guided_evaluation,
        )

        validate_local_guided_evaluation(manifest, presentation)
    except LocalValidationError as exc:
        raise VerificationError(f"manifest {exc}") from exc

    guided = manifest.get("visuals", {}).get("guidedEvaluation", {})
    early_gates = guided.get("earlyGates", {})
    early_gate_rows = early_gates.get("rows", [])
    require(
        early_gates.get("rowTotal") == 4
        and tuple(row.get("id") for row in early_gate_rows if isinstance(row, dict))
        == KONG_GUIDED_EARLY_GATE_IDS,
        "manifest guided early gates must preserve EAG-01 through EAG-04",
    )
    early_gate_provenance = early_gates.get("provenance", {})
    require(
        early_gate_provenance.get("sourcePath") == KONG_GUIDED_SOURCE_PATHS[0]
        and early_gate_provenance.get("sourceId") == KONG_GUIDED_SOURCE_IDS[0]
        and early_gate_provenance.get("sourceHeading") == "Four early assessment gates"
        and early_gate_provenance.get("heading") == "Four early assessment gates"
        and early_gate_provenance.get("asOf") == "2026-08-24",
        "manifest guided early gates must retain exact doc48 provenance",
    )

    identifier_rows = guided.get("identifierCatalog", {}).get("rows", [])
    require(
        tuple(row.get("token") for row in identifier_rows if isinstance(row, dict))
        == KONG_GUIDED_IDENTIFIER_TOKENS,
        "manifest guided identifier catalog must preserve exact token order",
    )
    term_set_rows = guided.get("termSets", {}).get("rows", [])
    require(
        guided.get("termSets", {}).get("rowTotal") == len(KONG_GUIDED_TERM_TOKENS)
        and tuple(
            (
                row.get("slideId"),
                tuple(term.get("token") for term in row.get("terms", ()) if isinstance(term, dict)),
            )
            for row in term_set_rows
            if isinstance(row, dict)
        ) == KONG_GUIDED_TERM_TOKENS,
        "manifest guided term sets must preserve exact per-slide order",
    )
    terms_by_slide_id = {
        row.get("slideId"): row.get("terms", [])
        for row in term_set_rows
        if isinstance(row, dict)
    }
    guided_slides = [
        slide for slide in presentation
        if isinstance(slide, dict) and slide.get("visual") == "guidedEvaluation"
    ]
    require(
        len(guided_slides) == 25
        and all(
            slide.get("terms") == terms_by_slide_id.get(slide.get("slideId"), [])
            for slide in guided_slides
        ),
        "manifest guided presentation terms must exactly project the canonical term sets",
    )

    assessment = guided.get("assessmentContract", {})
    interface_terms = assessment.get("interfaceTerms", [])
    require(
        tuple(
            (term.get("token"), term.get("display"))
            for term in interface_terms
            if isinstance(term, dict)
        ) == KONG_GUIDED_ASSESSMENT_INTERFACE_TERMS
        and all(
            isinstance(term, dict)
            and set(term) == {"token", "display", "purpose"}
            and isinstance(term.get("purpose"), str)
            and term["purpose"].strip()
            for term in interface_terms
        ),
        "manifest guided assessment must preserve the exact first-use interface terminology",
    )
    phase_question_ids = assessment.get("phaseQuestionIds", {})
    require(
        {
            phase_id: tuple(question_ids)
            for phase_id, question_ids in phase_question_ids.items()
            if isinstance(question_ids, list)
        }
        == KONG_GUIDED_ASSESSMENT_PHASE_QUESTION_IDS,
        "manifest guided assessment must preserve the exact 6/2/2/2/4/2 distribution",
    )
    questions = assessment.get("questions", [])
    question_by_id = {
        question.get("id"): question
        for question in questions
        if isinstance(question, dict)
    }
    require(len(questions) == 18, "manifest guided assessment must contain exactly 18 questions")
    for question_id, target_ids in KONG_GUIDED_EARLY_QUESTION_TARGET_IDS.items():
        question = question_by_id.get(question_id, {})
        require(
            tuple(question.get("slideIds", ())) == ("KGE-02", "KGE-03")
            and tuple(question.get("targetIds", ())) == target_ids
            and question.get("minimumEvidence") == "E1"
            and question.get("mandatory") is True
            and question.get("choiceSetId") == "KGE-CS-INPUT",
            f"manifest guided assessment {question_id} early-gate binding is invalid",
        )

    decision_references = assessment.get("decisionReferences", [])
    require(
        isinstance(decision_references, list) and bool(decision_references)
        and all(
            isinstance(reference, dict)
            and set(reference) == KONG_GUIDED_DECISION_REFERENCE_KEYS
            for reference in decision_references
        ),
        "manifest guided assessment decisionReferences must preserve the exact v2 schema",
    )
    selectors = [
        selector
        for reference in decision_references
        for selector in reference.get("selectors", [])
    ]
    require(
        all(isinstance(selector, str) and selector.strip() for selector in selectors)
        and len(selectors) == len(set(selectors)),
        "manifest guided assessment decision-reference selectors must be globally unique non-empty strings",
    )
    reference_by_selector = {
        selector: reference
        for reference in decision_references
        for selector in reference["selectors"]
    }
    require(
        all(
            target_id in reference_by_selector
            for question in questions
            if isinstance(question, dict)
            for target_id in question.get("targetIds", [])
        ),
        "manifest guided assessment target IDs must each resolve to exactly one decision reference",
    )
    manifest_documents = {
        (item.get("path"), item.get("id"))
        for item in manifest.get("items", [])
        if isinstance(item, dict) and item.get("type") == "markdown"
    }
    require(
        all(
            (reference.get("sourcePath"), reference.get("sourceId"))
            in manifest_documents
            for reference in decision_references
        ),
        "manifest guided assessment decision references must identify manifest Markdown documents",
    )
    for selector, expected in KONG_GUIDED_DECISION_REFERENCE_CANONICAL.items():
        reference = reference_by_selector.get(selector, {})
        require(
            (
                reference.get("sourcePath"),
                reference.get("sourceId"),
                reference.get("sourceHeading"),
            ) == expected,
            f"manifest guided assessment decision reference {selector} is invalid",
        )

    contract_by_slide_id = {
        row.get("slideId"): row
        for row in guided.get("slides", {}).get("rows", [])
        if isinstance(row, dict)
    }
    require(
        contract_by_slide_id.get("KGE-02", {}).get("title")
        == "The operating model and four early gates drive the decision"
        and "Traceable" in contract_by_slide_id.get("KGE-02", {}).get("body", "")
        and "EAG-01 – EAG-04" in contract_by_slide_id.get("KGE-02", {}).get("visualContract", "")
        and "unscored admission gate" in contract_by_slide_id.get("KGE-03", {}).get("body", "")
        and "unscored-adjunct" in contract_by_slide_id.get("KGE-03", {}).get("visualContract", ""),
        "manifest KGE-02/KGE-03 must preserve the explicit early-gate content",
    )

    strategy = manifest.get("visuals", {}).get("kongPlatformStrategy", {})
    overview = strategy.get("guidedArchitectureOverview")
    require(isinstance(overview, dict), "manifest KGE-09 guided architecture overview must be an object")
    require(
        overview.get("overviewId") == "KGE-09-OVERVIEW",
        "manifest KGE-09 guided architecture overview ID is invalid",
    )
    control_nodes = overview.get("controlZone", {}).get("nodes", [])
    require(
        tuple(node.get("id") for node in control_nodes if isinstance(node, dict))
        == KONG_GUIDED_ARCHITECTURE_CONTROL_IDS,
        "manifest KGE-09 guided architecture control nodes are invalid",
    )
    lanes = overview.get("lanes", [])
    require(
        tuple(lane.get("id") for lane in lanes if isinstance(lane, dict))
        == KONG_GUIDED_ARCHITECTURE_LANE_IDS,
        "manifest KGE-09 guided architecture lanes are invalid",
    )
    edges = overview.get("edges", [])
    require(
        tuple(
            (edge.get("from"), edge.get("to"), edge.get("kind"))
            for edge in edges
            if isinstance(edge, dict)
        )
        == KONG_GUIDED_ARCHITECTURE_EDGES,
        "manifest KGE-09 guided architecture edges must preserve CP fanout and three local, non-crossing runtime lanes",
    )


def run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ("git", *args),
            cwd=ROOT,
            env=git_environment(),
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise VerificationError(f"git {' '.join(args)} failed: {detail.strip()}") from exc
    return result.stdout.strip()


def verify_local_checkout(expected_revision: str) -> None:
    head = run_git("rev-parse", "--verify", "HEAD^{commit}")
    require(head == expected_revision, f"verifier checkout is {head}; expected {expected_revision}")
    status = run_git("status", "--porcelain=v1", "--untracked-files=all")
    require(not status, "verifier checkout is dirty")


def safe_remote_path(value: Any, label: str) -> str:
    require(isinstance(value, str) and bool(value), f"{label} must be a non-empty string")
    split = urlsplit(value)
    require(not split.scheme and not split.netloc and not split.query and not split.fragment, f"{label} must be a relative path")
    require(not split.path.startswith("/") and "\\" not in split.path, f"{label} must be a normalized relative path")
    require("%" not in split.path, f"{label} must not contain percent-encoded or literal percent syntax")
    parts = split.path.split("/")
    require(all(part not in {"", ".", ".."} for part in parts), f"{label} contains an unsafe path segment")
    return split.path


def validated_route_inventory(manifest: dict[str, Any], items: list[dict[str, Any]]) -> set[str]:
    """Validate every manifest-backed SPA route and return its exact inventory."""
    item_ids = [item.get("id") for item in items]
    item_paths = [item.get("path") for item in items]
    item_routes = [item.get("route") for item in items]
    path_to_id = dict(zip(item_paths, item_ids))

    presentation = manifest.get("presentation")
    require(isinstance(presentation, list) and bool(presentation), "manifest presentation must be a non-empty list")
    require(all(isinstance(slide, dict) for slide in presentation), "manifest presentation slide must be an object")
    slide_keys = [slide.get("key") for slide in presentation]
    require(all(isinstance(key, str) and key for key in slide_keys), "manifest presentation keys must be non-empty strings")
    require(len(slide_keys) == len(set(slide_keys)), "manifest presentation keys must be unique")
    require(
        [slide.get("index") for slide in presentation] == list(range(len(presentation))),
        "manifest presentation indices must be unique and contiguous from zero",
    )
    require(
        all(slide.get("sourceId") in item_ids for slide in presentation),
        "manifest presentation references an unknown sourceId",
    )
    validate_poc_projection(manifest)
    validate_criteria_projection(manifest)
    validate_kong_platform_fit_slides(manifest, presentation)

    content_routes = set(STATIC_ROUTES).union(item_routes)
    routes = set(STATIC_ROUTES)
    require(not routes.intersection(item_routes), "manifest static and document routes collide")
    routes.update(item_routes)
    generic_routes = {"#/present", *(f"#/present/{index}" for index in range(len(presentation)))}
    require(not routes.intersection(generic_routes), "manifest document and presentation routes collide")
    routes.update(generic_routes)

    audiences = manifest.get("audiences")
    require(isinstance(audiences, list) and bool(audiences), "manifest audiences must be a non-empty list")
    require(all(isinstance(audience, dict) for audience in audiences), "manifest audience must be an object")
    audience_ids = [audience.get("id") for audience in audiences]
    require(all(isinstance(audience_id, str) and audience_id for audience_id in audience_ids), "manifest audience IDs must be non-empty strings")
    require(len(audience_ids) == len(set(audience_ids)), "manifest audience IDs must be unique")

    def validate_sources(subject: dict[str, Any], label: str, *, require_nonempty: bool = False) -> list[str]:
        source_paths = subject.get("sourcePaths")
        source_ids = subject.get("sourceIds")
        require(isinstance(source_paths, list) and isinstance(source_ids, list), f"{label} sources must be lists")
        if require_nonempty:
            require(bool(source_paths), f"{label} must declare at least one source")
        require(all(isinstance(path, str) for path in source_paths), f"{label} sourcePaths are invalid")
        require(all(isinstance(item_id, str) for item_id in source_ids), f"{label} sourceIds are invalid")
        require(len(source_paths) == len(set(source_paths)), f"{label} sourcePaths must be unique")
        require(len(source_ids) == len(set(source_ids)), f"{label} sourceIds must be unique")
        expected_ids = [path_to_id.get(path) for path in source_paths]
        require(None not in expected_ids, f"{label} references an unknown source path")
        require(source_ids == expected_ids, f"{label} source IDs do not align with source paths")
        return source_ids

    for audience in audiences:
        audience_id = audience["id"]
        validate_sources(audience, f"manifest audience {audience_id}")
        selected = audience.get("presentationSlides")
        require(isinstance(selected, list) and bool(selected), f"manifest audience {audience_id} has no presentation slides")
        require(all(isinstance(key, str) for key in selected), f"manifest audience {audience_id} presentation slides are invalid")
        require(
            not any(key in REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS for key in selected),
            f"manifest audience {audience_id} retains a removed Kong platform fit slide",
        )
        require(all(key in slide_keys for key in selected), f"manifest audience {audience_id} references an unknown slide")
        require(len(selected) == len(set(selected)), f"manifest audience {audience_id} presentation slides must be unique")
        require(audience.get("presentationRoute") == f"#/present/{audience_id}/0", f"manifest audience {audience_id} presentationRoute is invalid")
        audience_routes = {f"#/present/{audience_id}/{index}" for index in range(len(selected))}
        audience_routes.add(f"#/audiences/{audience_id}")
        require(not routes.intersection(audience_routes), f"manifest audience {audience_id} routes collide")
        routes.update(audience_routes)
        recommended = audience.get("recommendedRoute")
        require(isinstance(recommended, str), f"manifest audience {audience_id} recommendedRoute is invalid")
        require(recommended.split("?", 1)[0] in content_routes, f"manifest audience {audience_id} recommendedRoute is unknown")

    decks = manifest.get("presentationDecks")
    require(isinstance(decks, list) and bool(decks), "manifest presentationDecks must be a non-empty list")
    require(all(isinstance(deck, dict) for deck in decks), "manifest presentation deck must be an object")
    deck_ids = [deck.get("id") for deck in decks]
    require(all(isinstance(deck_id, str) and deck_id for deck_id in deck_ids), "manifest presentation deck IDs must be non-empty strings")
    require(len(deck_ids) == len(set(deck_ids)), "manifest presentation deck IDs must be unique")
    require(not set(deck_ids).intersection(audience_ids), "manifest presentation deck IDs must not collide with audience IDs")

    for deck in decks:
        deck_id = deck["id"]
        source_ids = validate_sources(deck, f"manifest presentation deck {deck_id}", require_nonempty=True)
        selected = deck.get("presentationSlides")
        require(isinstance(selected, list) and bool(selected), f"manifest presentation deck {deck_id} has no presentation slides")
        require(all(isinstance(key, str) for key in selected), f"manifest presentation deck {deck_id} presentation slides are invalid")
        require(
            not any(key in REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS for key in selected),
            f"manifest presentation deck {deck_id} retains a removed Kong platform fit slide",
        )
        require(all(key in slide_keys for key in selected), f"manifest presentation deck {deck_id} references an unknown slide")
        require(len(selected) == len(set(selected)), f"manifest presentation deck {deck_id} presentation slides must be unique")
        require(
            type(deck.get("slideTotal")) is int and deck["slideTotal"] == len(selected),
            f"manifest presentation deck {deck_id} slideTotal must equal its presentation slide count",
        )
        validate_journey_phase_starts(deck, selected, f"manifest presentation deck {deck_id}")
        selected_source_ids = {
            slide["sourceId"] for slide in presentation if slide["key"] in selected
        }
        require(
            selected_source_ids.issubset(set(source_ids)),
            f"manifest presentation deck {deck_id} sources do not cover its selected slides",
        )
        role_ids = deck.get("audienceRoleIds")
        require(isinstance(role_ids, list) and bool(role_ids), f"manifest presentation deck {deck_id} audienceRoleIds must be a non-empty list")
        require(
            all(isinstance(role_id, str) and role_id in audience_ids for role_id in role_ids),
            f"manifest presentation deck {deck_id} references an unknown audience role",
        )
        require(len(role_ids) == len(set(role_ids)), f"manifest presentation deck {deck_id} audienceRoleIds must be unique")
        require(deck.get("presentationRoute") == f"#/present/{deck_id}/0", f"manifest presentation deck {deck_id} presentationRoute is invalid")
        deck_routes = {f"#/present/{deck_id}/{index}" for index in range(len(selected))}
        if deck_id == KONG_GUIDED_DECK_ID:
            summary_route = deck.get("summaryRoute")
            require(
                summary_route == KONG_GUIDED_ASSESSMENT_SUMMARY_ROUTE,
                "manifest guided presentation deck summaryRoute is invalid",
            )
            deck_routes.add(summary_route)
        else:
            require(
                "summaryRoute" not in deck,
                f"manifest presentation deck {deck_id} must not declare a summaryRoute",
            )
        require(not routes.intersection(deck_routes), f"manifest presentation deck {deck_id} routes collide")
        routes.update(deck_routes)
        exit_route = deck.get("exitRoute")
        require(isinstance(exit_route, str), f"manifest presentation deck {deck_id} exitRoute is invalid")
        require(exit_route.split("?", 1)[0] in content_routes, f"manifest presentation deck {deck_id} exitRoute is unknown")

    return routes


def request_url(base_url: str, relative: str, token: str) -> str:
    encoded_path = "/".join(quote(part, safe="") for part in relative.split("/") if part)
    absolute = urljoin(base_url, encoded_path)
    split = urlsplit(absolute)
    query = urlencode({"provenance": token})
    return urlunsplit((split.scheme, split.netloc, split.path, query, ""))


def remaining_timeout(deadline: float, requested_timeout: float) -> float:
    """Return a per-operation timeout that cannot outlive the global deadline."""
    remaining = deadline - time.monotonic()
    require(remaining > 0, "overall verification deadline expired")
    return min(requested_timeout, remaining)


def read_limited(response: Any, limit: int, label: str, deadline: float, timeout: float) -> bytes:
    length = response.headers.get("Content-Length")
    if length is not None:
        try:
            require(int(length) <= limit, f"{label} exceeds its bounded response size")
        except ValueError as exc:
            raise VerificationError(f"{label} has an invalid Content-Length") from exc
    chunks: list[bytes] = []
    total = 0
    read_chunk = getattr(response, "read1", response.read)
    while True:
        remaining_timeout(deadline, timeout)
        chunk = read_chunk(min(1024 * 1024, limit - total + 1))
        remaining_timeout(deadline, timeout)
        if not chunk:
            break
        total += len(chunk)
        require(total <= limit, f"{label} exceeds its bounded response size")
        chunks.append(chunk)
    return b"".join(chunks)


def fetch(
    base_url: str,
    relative: str,
    token: str,
    timeout: float,
    deadline: float,
    max_bytes: int = MAX_METADATA_BYTES,
) -> tuple[int, bytes]:
    url = request_url(base_url, relative, token)
    request = Request(
        url,
        headers={
            "Accept": "application/json,text/html,*/*",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "User-Agent": "api-management-studies-pages-verifier/1",
        },
    )
    try:
        with urlopen(request, timeout=remaining_timeout(deadline, timeout)) as response:
            return response.status, read_limited(response, max_bytes, relative or "site root", deadline, timeout)
    except HTTPError as exc:
        try:
            return exc.code, read_limited(exc, max_bytes, relative or "site root", deadline, timeout)
        finally:
            exc.close()
    except (URLError, TimeoutError, OSError) as exc:
        raise VerificationError(f"request failed for {relative}: {exc}") from exc


def load_manifest(base_url: str, token: str, timeout: float, deadline: float) -> tuple[dict[str, Any], bytes]:
    status, raw = fetch(base_url, "content-manifest.json", token, timeout, deadline)
    require(status == 200, f"content-manifest.json returned HTTP {status}")
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"content-manifest.json is not valid UTF-8 JSON: {exc}") from exc
    require(isinstance(manifest, dict), "content-manifest.json root must be an object")
    return manifest, raw


def validate_manifest_shape(
    manifest: dict[str, Any],
    expected_revision: str,
    study_paths: list[str],
    expected_routes: list[str],
) -> list[Target]:
    require(manifest.get("schemaVersion") == SCHEMA_VERSION, f"schemaVersion must be {SCHEMA_VERSION}")
    revision = manifest.get("sourceRevision")
    require(isinstance(revision, str) and bool(REVISION_PATTERN.fullmatch(revision)), "sourceRevision is invalid")
    require(revision == expected_revision, f"Pages serves revision {revision}; expected {expected_revision}")
    require(manifest.get("sourceDirty") is False, "Pages manifest is not a clean build")
    require(
        isinstance(manifest.get("generatedAt"), str) and bool(GENERATED_AT_PATTERN.fullmatch(manifest["generatedAt"])),
        "generatedAt is not a deterministic UTC timestamp",
    )
    epoch = os.environ.get("SOURCE_DATE_EPOCH") or run_git("show", "-s", "--format=%ct", expected_revision)
    require(bool(re.fullmatch(r"\d+", epoch)), f"SOURCE_DATE_EPOCH is invalid: {epoch!r}")
    try:
        expected_generated_at = datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (OverflowError, OSError, ValueError) as exc:
        raise VerificationError(f"SOURCE_DATE_EPOCH is outside the supported timestamp range: {epoch!r}") from exc
    require(manifest["generatedAt"] == expected_generated_at, f"generatedAt must be {expected_generated_at}")
    generator = manifest.get("generator")
    require(isinstance(generator, dict) and generator.get("path") == "scripts/build_site.py", "generator provenance is invalid")
    require(
        isinstance(generator.get("sha256"), str) and bool(SHA256_PATTERN.fullmatch(generator["sha256"])),
        "generator SHA-256 is invalid",
    )
    require(generator["sha256"] == sha256_file(ROOT / "scripts/build_site.py"), "generator SHA-256 differs from the verifier checkout")

    assets = manifest.get("assets")
    local_asset_paths = {
        path.relative_to(ROOT / "site").as_posix()
        for path in (ROOT / "site").rglob("*")
        if path.is_file()
    } | {"404.html"}
    require(REQUIRED_ASSETS.issubset(local_asset_paths), "required assets are missing from the verifier checkout")
    require(isinstance(assets, dict) and set(assets) == local_asset_paths, "manifest asset digest set differs from the verifier checkout")
    items = manifest.get("items")
    require(isinstance(items, list) and bool(items), "manifest items must be a non-empty list")

    item_paths: list[str] = []
    item_ids: list[str] = []
    content_urls: list[str] = []
    targets: list[Target] = []
    for item in items:
        require(isinstance(item, dict), "manifest item must be an object")
        item_id = item.get("id")
        item_path = safe_remote_path(item.get("path"), "item path")
        content_url = safe_remote_path(item.get("contentUrl"), f"item {item_id} contentUrl")
        require(isinstance(item_id, str) and bool(item_id), "item ID must be a non-empty string")
        require(content_url == f"content/{item_path}", f"item {item_id} contentUrl does not match its path")
        require(item.get("route") == f"#/doc/{item_id}", f"item {item_id} route is invalid")
        item_digest = item.get("sha256")
        item_size = item.get("size")
        require(isinstance(item_digest, str) and bool(SHA256_PATTERN.fullmatch(item_digest)), f"item {item_id} SHA-256 is invalid")
        require(type(item_size) is int and item_size >= 0, f"item {item_id} size is invalid")
        local_source = ROOT / item_path
        require(local_source.is_file(), f"item {item_id} is missing from the verifier checkout")
        require(local_source.stat().st_size == item_size, f"item {item_id} size differs from the verifier checkout")
        require(sha256_file(local_source) == item_digest, f"item {item_id} SHA-256 differs from the verifier checkout")
        item_paths.append(item_path)
        item_ids.append(item_id)
        content_urls.append(content_url)
        targets.append(Target(content_url, item_digest, item_size, f"content item {item_path}"))

    require(len(item_paths) == len(set(item_paths)), "manifest contains duplicate item paths")
    require(len(item_ids) == len(set(item_ids)), "manifest contains duplicate item IDs")
    require(len(content_urls) == len(set(content_urls)), "manifest contains duplicate content URLs")
    for study_path in study_paths:
        normalized = safe_remote_path(study_path, "study path")
        require(normalized in item_paths, f"requested study path is not published: {normalized}")

    available_routes = validated_route_inventory(manifest, items)
    validate_kong_platform_journey(manifest, manifest["presentation"])
    validate_kong_guided_evaluation(manifest, manifest["presentation"])
    for route in expected_routes:
        require(isinstance(route, str) and route.startswith("#/") and route in available_routes, f"requested derived route is not published: {route}")

    for relative, metadata in assets.items():
        safe_remote_path(relative, "asset path")
        require(isinstance(metadata, dict), f"asset {relative} metadata is invalid")
        asset_digest = metadata.get("sha256")
        asset_size = metadata.get("size")
        require(isinstance(asset_digest, str) and bool(SHA256_PATTERN.fullmatch(asset_digest)), f"asset {relative} SHA-256 is invalid")
        require(type(asset_size) is int and asset_size >= 0, f"asset {relative} size is invalid")
        source_relative = "index.html" if relative == "404.html" else relative
        local_source = ROOT / "site" / source_relative
        require(local_source.is_file(), f"asset {relative} is missing from the verifier checkout")
        require(local_source.stat().st_size == asset_size, f"asset {relative} size differs from the verifier checkout")
        require(sha256_file(local_source) == asset_digest, f"asset {relative} SHA-256 differs from the verifier checkout")
        if relative not in {"index.html", "404.html"}:
            targets.append(Target(relative, asset_digest, asset_size, f"asset {relative}"))
    return targets


def fetch_target_digest(
    base_url: str,
    target: Target,
    token: str,
    timeout: float,
    deadline: float,
) -> tuple[int, int, str]:
    require(target.size <= MAX_TARGET_BYTES, f"{target.label} exceeds the public artifact size limit")
    url = request_url(base_url, target.relative, token)
    request = Request(
        url,
        headers={
            "Accept": "*/*",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "User-Agent": "api-management-studies-pages-verifier/1",
        },
    )
    try:
        response = urlopen(request, timeout=remaining_timeout(deadline, timeout))
    except HTTPError as exc:
        try:
            return exc.code, 0, digest(b"")
        finally:
            exc.close()
    except (URLError, TimeoutError, OSError) as exc:
        raise VerificationError(f"request failed for {target.relative}: {exc}") from exc
    with response:
        length = response.headers.get("Content-Length")
        if length is not None:
            try:
                require(int(length) == target.size, f"{target.label} Content-Length differs from the manifest")
            except ValueError as exc:
                raise VerificationError(f"{target.label} has an invalid Content-Length") from exc
        file_digest = hashlib.sha256()
        size = 0
        read_chunk = getattr(response, "read1", response.read)
        while True:
            remaining_timeout(deadline, timeout)
            chunk = read_chunk(min(1024 * 1024, target.size - size + 1))
            remaining_timeout(deadline, timeout)
            if not chunk:
                break
            size += len(chunk)
            require(size <= target.size, f"{target.label} size exceeds the manifest")
            file_digest.update(chunk)
        return response.status, size, file_digest.hexdigest()


def verify_target(base_url: str, target: Target, token: str, timeout: float, deadline: float) -> None:
    status, size, target_digest = fetch_target_digest(base_url, target, token, timeout, deadline)
    require(status == 200, f"{target.label} returned HTTP {status}")
    require(size == target.size, f"{target.label} size differs from the manifest")
    require(target_digest == target.sha256, f"{target.label} SHA-256 differs from the manifest")


def verify_targets(
    base_url: str,
    targets: list[Target],
    token: str,
    timeout: float,
    workers: int,
    deadline: float,
) -> None:
    """Verify the target set without letting queued futures extend the deadline."""
    failures: list[str] = []
    executor = ThreadPoolExecutor(max_workers=workers)
    future_targets = {
        executor.submit(verify_target, base_url, target, f"{token}-{index}", timeout, deadline): target
        for index, target in enumerate(targets)
    }
    pending = set(future_targets)
    timed_out = False
    try:
        while pending:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                raise VerificationError("overall verification deadline expired")
            done, not_done = wait(pending, timeout=remaining, return_when=FIRST_COMPLETED)
            if not done:
                timed_out = True
                raise VerificationError("overall verification deadline expired")
            pending = set(not_done)
            for future in done:
                target = future_targets[future]
                try:
                    future.result()
                except Exception as exc:  # Report every concurrently observed mismatch together.
                    failures.append(f"{target.label}: {exc}")
    finally:
        for future in pending:
            future.cancel()
        executor.shutdown(wait=not timed_out, cancel_futures=True)
    require(not failures, "; ".join(sorted(failures)))


def verify_once(
    base_url: str,
    expected_revision: str,
    study_paths: list[str],
    attempt: int,
    timeout: float,
    workers: int,
    expected_manifest_sha256: str | None,
    expected_routes: list[str],
    deadline: float,
) -> tuple[int, int]:
    token = f"{expected_revision}-{attempt}"
    manifest, manifest_bytes = load_manifest(base_url, token, timeout, deadline)
    if expected_manifest_sha256:
        require(digest(manifest_bytes) == expected_manifest_sha256, "deployed manifest SHA-256 differs from the build artifact")
    targets = validate_manifest_shape(manifest, expected_revision, study_paths, expected_routes)
    assets = manifest["assets"]

    root_status, root = fetch(base_url, "", token, timeout, deadline, assets["index.html"]["size"] + 1)
    require(root_status == 200, f"site root returned HTTP {root_status}")
    require(len(root) == assets["index.html"]["size"], "site root size differs from index.html provenance")
    require(digest(root) == assets["index.html"]["sha256"], "site root does not match index.html provenance")

    missing_path = f"__pages_provenance_{expected_revision}_{attempt}.html"
    missing_status, missing = fetch(
        base_url, missing_path, token, timeout, deadline, assets["404.html"]["size"] + 1
    )
    require(missing_status == 404, f"unknown Pages path returned HTTP {missing_status}, expected 404")
    require(len(missing) == assets["404.html"]["size"], "404 response size differs from 404.html provenance")
    require(digest(missing) == assets["404.html"]["sha256"], "404 response does not match 404.html provenance")

    verify_targets(base_url, targets, token, timeout, workers, deadline)
    return len(manifest["items"]), len(manifest["assets"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Deployed Pages URL, including any repository base path")
    parser.add_argument(
        "--expected-revision",
        default=os.environ.get("SOURCE_REVISION") or os.environ.get("GITHUB_SHA"),
        help="Full revision GitHub Pages must serve (defaults to SOURCE_REVISION, then GITHUB_SHA)",
    )
    parser.add_argument("--study-path", action="append", default=[], help="Require this repository study path; repeat as needed")
    parser.add_argument("--expected-route", action="append", default=[], help="Require this exact manifest-backed SPA route; repeat as needed")
    parser.add_argument(
        "--expected-manifest-sha256",
        default=os.environ.get("EXPECTED_MANIFEST_SHA256"),
        help="SHA-256 of the manifest produced by the build job",
    )
    parser.add_argument("--retries", type=int, default=18, help="Maximum deployment-read attempts")
    parser.add_argument("--delay", type=float, default=10.0, help="Seconds between attempts")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout in seconds")
    parser.add_argument("--overall-timeout", type=float, default=600.0, help="Overall verification deadline in seconds")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent content verification requests")
    args = parser.parse_args()

    require(args.expected_revision is not None, "--expected-revision is required when no revision environment variable is set")
    expected_revision = args.expected_revision.lower()
    require(bool(REVISION_PATTERN.fullmatch(expected_revision)), "--expected-revision must be a full hexadecimal Git object ID")
    if args.expected_manifest_sha256 is not None:
        require(
            bool(SHA256_PATTERN.fullmatch(args.expected_manifest_sha256)),
            "--expected-manifest-sha256 must be a lowercase SHA-256 digest",
        )
    require(args.retries > 0 and args.delay >= 0 and args.timeout > 0 and args.overall_timeout > 0 and args.workers > 0, "retry, delay, timeout, and worker values are invalid")
    split = urlsplit(args.base_url)
    require(split.scheme in {"http", "https"} and bool(split.netloc), "--base-url must be an absolute HTTP(S) URL")
    base_url = args.base_url.rstrip("/") + "/"
    verify_local_checkout(expected_revision)

    last_error: Exception | None = None
    deadline = time.monotonic() + args.overall_timeout
    for attempt in range(1, args.retries + 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            last_error = VerificationError("overall verification deadline expired")
            break
        try:
            item_count, asset_count = verify_once(
                base_url,
                expected_revision,
                args.study_path,
                attempt,
                min(args.timeout, remaining),
                args.workers,
                args.expected_manifest_sha256,
                args.expected_route,
                deadline,
            )
            print(
                f"OK: Pages serves clean revision {expected_revision}; "
                f"root, 404, {item_count} content items, and {asset_count} assets match"
            )
            return 0
        except VerificationError as exc:
            last_error = exc
            if attempt == args.retries:
                break
            print(f"WAIT: Pages verification attempt {attempt}/{args.retries} did not converge: {exc}")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                last_error = VerificationError("overall verification deadline expired")
                break
            time.sleep(min(args.delay, remaining))
    print(f"ERROR: Pages did not serve the expected artifact: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
