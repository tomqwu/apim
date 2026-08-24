#!/usr/bin/env python3
"""Validate and compose the public-safe federated API delivery reference.

The module intentionally uses only Python's standard library. It validates the
small reference schema; production still requires pinned OpenAPI, decK, Kong,
and policy-as-code validation for the exact target option.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class ValidationError(ValueError):
    """Raised when a governance or evidence rule fails closed."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing input: {path}") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"unreadable JSON input: {path}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{context} must be an object")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be a list")
    return value


def require_string(record: dict[str, Any], key: str, context: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context}.{key} must be a non-empty string")
    return value.strip()


def require_integer(record: dict[str, Any], key: str, context: str, minimum: int, maximum: int) -> int:
    value = record.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise ValidationError(f"{context}.{key} must be an integer in [{minimum},{maximum}]")
    return value


def unique_strings(value: Any, context: str, allow_empty: bool = False) -> list[str]:
    items = require_list(value, context)
    if not allow_empty and not items:
        raise ValidationError(f"{context} must not be empty")
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValidationError(f"{context} must contain non-empty strings")
    normalized = [item.strip() for item in items]
    if len(normalized) != len(set(normalized)):
        raise ValidationError(f"{context} contains duplicates")
    return normalized


def load_inputs(root: Path) -> dict[str, Any]:
    root = root.resolve()
    bundles = sorted((root / "platform" / "policy-bundles").glob("*.json"))
    if len(bundles) != 1:
        raise ValidationError("reference must contain exactly one selected central policy bundle")
    return {
        "openapi": read_json(root / "app" / "openapi.json"),
        "intent": read_json(root / "app" / "api-intent.json"),
        "metadata": read_json(root / "app" / "metadata.json"),
        "tests": read_json(root / "app" / "tests.json"),
        "policy": read_json(bundles[0]),
        "policy_path": bundles[0].relative_to(root).as_posix(),
        "writers": read_json(root / "platform" / "writer-registry.json"),
        "exceptions": read_json(root / "platform" / "exceptions.json"),
        "target": read_json(root / "platform" / "target.json"),
    }


def plugin_instance(api_id: str, control_or_name: str, application_owned: bool = False) -> str:
    token = re.sub(r"[^a-z0-9-]+", "-", control_or_name.lower()).strip("-")
    prefix = "app-" if application_owned else ""
    return f"{api_id}-{prefix}{token}"


def operation_index(openapi: dict[str, Any]) -> dict[str, tuple[str, str]]:
    operations: dict[str, tuple[str, str]] = {}
    paths = require_mapping(openapi.get("paths"), "openapi.paths")
    if not paths:
        raise ValidationError("openapi.paths must not be empty")
    for api_path, path_item_value in paths.items():
        if not isinstance(api_path, str) or not api_path.startswith("/"):
            raise ValidationError("OpenAPI paths must begin with /")
        path_item = require_mapping(path_item_value, f"openapi.paths[{api_path}]")
        for method, operation_value in path_item.items():
            if method.lower() not in HTTP_METHODS:
                continue
            operation = require_mapping(operation_value, f"openapi.paths[{api_path}].{method}")
            operation_id = require_string(operation, "operationId", f"openapi.paths[{api_path}].{method}")
            if operation_id in operations:
                raise ValidationError(f"duplicate OpenAPI operationId: {operation_id}")
            operations[operation_id] = (method.upper(), api_path)
    if not operations:
        raise ValidationError("OpenAPI must contain at least one operation")
    return operations


def validate_url(url: str, suffix: str, context: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host.endswith(suffix) or host == suffix.removeprefix("."):
        raise ValidationError(f"unsafe route: {context} must use https and an approved {suffix} host")
    if parsed.username or parsed.password or parsed.fragment:
        raise ValidationError(f"unsafe route: {context} contains prohibited URL components")
    return host


def validate_inputs(inputs: dict[str, Any]) -> None:
    openapi = require_mapping(inputs.get("openapi"), "openapi")
    intent = require_mapping(inputs.get("intent"), "intent")
    metadata = require_mapping(inputs.get("metadata"), "metadata")
    tests = require_mapping(inputs.get("tests"), "tests")
    policy = require_mapping(inputs.get("policy"), "policy")
    writers = require_mapping(inputs.get("writers"), "writers")
    exceptions = require_mapping(inputs.get("exceptions"), "exceptions")
    target = require_mapping(inputs.get("target"), "target")

    if openapi.get("openapi") != "3.0.3":
        raise ValidationError("openapi.openapi must be 3.0.3 in this reference")
    info = require_mapping(openapi.get("info"), "openapi.info")
    require_string(info, "title", "openapi.info")
    require_string(info, "version", "openapi.info")
    operations = operation_index(openapi)

    api_id = require_string(intent, "api_id", "intent")
    if not NAME_PATTERN.fullmatch(api_id):
        raise ValidationError("intent.api_id must use lower-case letters, numbers, and hyphens")
    app_writer = require_string(intent, "writer_id", "intent")
    if not app_writer.startswith("app:"):
        raise ValidationError("intent.writer_id must identify an application source authority")
    if metadata.get("api_id") != api_id:
        raise ValidationError("metadata.api_id must match intent.api_id")
    for key in ("owner_id", "support_ref", "lifecycle", "data_classification"):
        require_string(metadata, key, "metadata")
    exception_refs = unique_strings(metadata.get("exception_ids"), "metadata.exception_ids", allow_empty=True)

    route_rules = require_mapping(policy.get("route_rules"), "policy.route_rules")
    public_suffix = require_string(route_rules, "allowed_public_host_suffix", "policy.route_rules")
    backend_suffix = require_string(route_rules, "allowed_backend_host_suffix", "policy.route_rules")
    allowed_protocols = set(unique_strings(route_rules.get("allowed_protocols"), "policy.route_rules.allowed_protocols"))
    if route_rules.get("allow_wildcard_hosts") is not False or route_rules.get("allow_regex_paths") is not False:
        raise ValidationError("reference route policy must reject wildcard hosts and regex paths")
    minimum_segments = require_integer(route_rules, "minimum_path_segments", "policy.route_rules", 1, 20)

    service = require_mapping(intent.get("service"), "intent.service")
    service_name = require_string(service, "name", "intent.service")
    if not NAME_PATTERN.fullmatch(service_name):
        raise ValidationError("intent.service.name has an unsafe format")
    validate_url(require_string(service, "url", "intent.service"), backend_suffix, "backend URL")
    require_integer(service, "connect_timeout_ms", "intent.service", 100, 120000)
    require_integer(service, "read_timeout_ms", "intent.service", 100, 120000)
    require_integer(service, "write_timeout_ms", "intent.service", 100, 120000)
    require_integer(service, "retries", "intent.service", 0, 5)

    route = require_mapping(intent.get("route"), "intent.route")
    route_name = require_string(route, "name", "intent.route")
    if not NAME_PATTERN.fullmatch(route_name):
        raise ValidationError("intent.route.name has an unsafe format")
    hosts = unique_strings(route.get("hosts"), "intent.route.hosts")
    for host in hosts:
        if "*" in host or not host.lower().endswith(public_suffix) or host.lower() == public_suffix.removeprefix("."):
            raise ValidationError("unsafe route: host is outside the approved suffix or contains a wildcard")
    protocols = set(unique_strings(route.get("protocols"), "intent.route.protocols"))
    if not protocols or not protocols.issubset(allowed_protocols):
        raise ValidationError("unsafe route: protocol is outside the central allowlist")
    route_paths = unique_strings(route.get("paths"), "intent.route.paths")
    for route_path in route_paths:
        segment_count = len([segment for segment in route_path.split("/") if segment])
        if not route_path.startswith("/") or "~" in route_path or segment_count < minimum_segments:
            raise ValidationError("unsafe route: path is root, regex-like, or too broad")
    if route.get("strip_path") is not False or route.get("preserve_host") is not True:
        raise ValidationError("intent.route must preserve the reviewed host/path semantics")
    if not all(any(api_path == prefix or api_path.startswith(prefix + "/") for prefix in route_paths) for _, api_path in operations.values()):
        raise ValidationError("OpenAPI operation path falls outside the requested Route prefixes")
    servers = require_list(openapi.get("servers"), "openapi.servers")
    if not servers:
        raise ValidationError("openapi.servers must not be empty")
    server_hosts = {
        validate_url(require_string(require_mapping(item, "openapi.servers[]"), "url", "openapi.servers[]"), public_suffix, "OpenAPI server")
        for item in servers
    }
    if server_hosts != {host.lower() for host in hosts}:
        raise ValidationError("OpenAPI servers and requested Route hosts must match exactly")

    policy_writer = require_string(policy, "writer_id", "policy")
    policy_version = require_string(policy, "version", "policy")
    require_string(policy, "bundle_id", "policy")
    try:
        as_of = date.fromisoformat(require_string(policy, "as_of_date", "policy"))
    except ValueError as exc:
        raise ValidationError("policy.as_of_date must use YYYY-MM-DD") from exc
    mandatory_ids = unique_strings(policy.get("mandatory_control_ids"), "policy.mandatory_control_ids")
    non_exemptible = set(unique_strings(policy.get("non_exemptible_control_ids"), "policy.non_exemptible_control_ids"))
    exception_eligible = set(unique_strings(policy.get("exception_eligible_control_ids"), "policy.exception_eligible_control_ids", allow_empty=True))
    if not set(mandatory_ids).issubset(non_exemptible):
        raise ValidationError("every mandatory central control must be non-exemptible")
    required_plugins = require_list(policy.get("required_plugins"), "policy.required_plugins")
    required_by_name: dict[str, dict[str, Any]] = {}
    required_ids: list[str] = []
    for index, plugin_value in enumerate(required_plugins):
        plugin = require_mapping(plugin_value, f"policy.required_plugins[{index}]")
        control_id = require_string(plugin, "control_id", f"policy.required_plugins[{index}]")
        name = require_string(plugin, "name", f"policy.required_plugins[{index}]")
        if name in required_by_name:
            raise ValidationError(f"duplicate required plugin: {name}")
        if plugin.get("scope") != "service":
            raise ValidationError("reference required plugins must use service scope")
        require_mapping(plugin.get("config"), f"policy.required_plugins[{index}].config")
        required_by_name[name] = plugin
        required_ids.append(control_id)
    if sorted(required_ids) != sorted(mandatory_ids):
        raise ValidationError("mandatory control IDs and required plugin control IDs must match")

    prohibited = set(unique_strings(policy.get("prohibited_application_plugins"), "policy.prohibited_application_plugins"))
    if not set(required_by_name).issubset(prohibited):
        raise ValidationError("every central required plugin must be reserved from application ownership")
    catalog = require_mapping(policy.get("application_plugin_catalog"), "policy.application_plugin_catalog")
    app_plugins = require_list(intent.get("plugins"), "intent.plugins")
    seen_app_plugins: set[str] = set()
    for index, plugin_value in enumerate(app_plugins):
        plugin = require_mapping(plugin_value, f"intent.plugins[{index}]")
        name = require_string(plugin, "name", f"intent.plugins[{index}]")
        if name in required_by_name:
            raise ValidationError(f"application attempts to own reserved mandatory plugin: {name}")
        if name in prohibited:
            raise ValidationError(f"prohibited application plugin: {name}")
        if name in seen_app_plugins:
            raise ValidationError(f"duplicate application plugin: {name}")
        seen_app_plugins.add(name)
        rule = require_mapping(catalog.get(name), f"policy.application_plugin_catalog[{name}]")
        config = require_mapping(plugin.get("config"), f"intent.plugins[{index}].config")
        allowed_keys = set(unique_strings(rule.get("allowed_config_keys"), f"catalog[{name}].allowed_config_keys"))
        if not set(config).issubset(allowed_keys):
            raise ValidationError(f"application plugin {name} uses configuration outside the central catalog")
        maximums = require_mapping(rule.get("maximums", {}), f"catalog[{name}].maximums")
        for key, maximum in maximums.items():
            value = config.get(key)
            if not isinstance(maximum, (int, float)) or isinstance(maximum, bool):
                raise ValidationError(f"catalog maximum for {name}.{key} must be numeric")
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value > maximum:
                raise ValidationError(f"application plugin {name}.{key} exceeds the central maximum")

    registry_items = require_list(writers.get("entities"), "writers.entities")
    registry: dict[tuple[str, str], str] = {}
    for index, item_value in enumerate(registry_items):
        item = require_mapping(item_value, f"writers.entities[{index}]")
        key = (
            require_string(item, "kind", f"writers.entities[{index}]"),
            require_string(item, "name", f"writers.entities[{index}]"),
        )
        if key in registry:
            raise ValidationError(f"conflicting writers: duplicate registry entry for {key[0]} {key[1]}")
        registry[key] = require_string(item, "writer_id", f"writers.entities[{index}]")
    expected_writers = {
        ("service", service_name): app_writer,
        ("route", route_name): app_writer,
    }
    for plugin in required_plugins:
        expected_writers[("plugin", plugin_instance(api_id, plugin["control_id"]))] = policy_writer
    for plugin in app_plugins:
        expected_writers[("plugin", plugin_instance(api_id, plugin["name"], application_owned=True))] = app_writer
    for key, expected_writer in expected_writers.items():
        actual_writer = registry.get(key)
        if actual_writer != expected_writer:
            raise ValidationError(
                f"conflicting writers: {key[0]} {key[1]} expects {expected_writer}, found {actual_writer or 'none'}"
            )

    exception_items = require_list(exceptions.get("exceptions"), "exceptions.exceptions")
    exception_by_id: dict[str, dict[str, Any]] = {}
    for index, item_value in enumerate(exception_items):
        item = require_mapping(item_value, f"exceptions.exceptions[{index}]")
        exception_id = require_string(item, "id", f"exceptions.exceptions[{index}]")
        if exception_id in exception_by_id:
            raise ValidationError(f"duplicate exception ID: {exception_id}")
        exception_by_id[exception_id] = item
    missing_exceptions = set(exception_refs) - set(exception_by_id)
    if missing_exceptions:
        raise ValidationError(f"application references unknown exceptions: {sorted(missing_exceptions)}")
    for exception_id in exception_refs:
        item = exception_by_id[exception_id]
        control_id = require_string(item, "control_id", f"exception {exception_id}")
        if control_id in non_exemptible:
            raise ValidationError(f"exception {exception_id} targets non-exemptible control {control_id}")
        if control_id not in exception_eligible:
            raise ValidationError(f"exception {exception_id} targets a rule not marked exception-eligible")
        if item.get("status") != "approved":
            raise ValidationError(f"exception {exception_id} is not approved")
        scope = require_mapping(item.get("scope"), f"exception {exception_id}.scope")
        if scope.get("api_id") != api_id:
            raise ValidationError(f"exception {exception_id} has the wrong API scope")
        for key in ("owner_id", "removal_owner_id", "reviewed_by_role", "audit_ref"):
            require_string(item, key, f"exception {exception_id}")
        unique_strings(item.get("compensating_controls"), f"exception {exception_id}.compensating_controls")
        try:
            expiry = date.fromisoformat(require_string(item, "expires_at", f"exception {exception_id}"))
        except ValueError as exc:
            raise ValidationError(f"exception {exception_id}.expires_at must use YYYY-MM-DD") from exc
        if expiry <= as_of:
            raise ValidationError(f"expired exception: {exception_id} ended on {expiry.isoformat()}")

    cases = require_list(tests.get("cases"), "tests.cases")
    case_ids: set[str] = set()
    covered_operations: set[str] = set()
    negative_count = 0
    for index, case_value in enumerate(cases):
        case = require_mapping(case_value, f"tests.cases[{index}]")
        case_id = require_string(case, "id", f"tests.cases[{index}]")
        if case_id in case_ids:
            raise ValidationError(f"duplicate test case ID: {case_id}")
        case_ids.add(case_id)
        kind = require_string(case, "kind", f"tests.cases[{index}]")
        method = require_string(case, "method", f"tests.cases[{index}]").upper()
        path = require_string(case, "path", f"tests.cases[{index}]")
        require_integer(case, "expected_status", f"tests.cases[{index}]", 100, 599)
        if not path.startswith("/") or method.lower() not in HTTP_METHODS:
            raise ValidationError(f"test case {case_id} has an invalid method/path")
        if kind == "operation":
            operation_id = require_string(case, "operation_id", f"tests.cases[{index}]")
            if operation_id not in operations:
                raise ValidationError(f"test case {case_id} references unknown operation {operation_id}")
            if operations[operation_id][0] != method:
                raise ValidationError(f"test case {case_id} method does not match OpenAPI")
            covered_operations.add(operation_id)
        elif kind == "negative":
            negative_count += 1
        else:
            raise ValidationError(f"test case {case_id} has unsupported kind {kind}")
    if covered_operations != set(operations):
        raise ValidationError(f"operation tests are incomplete; covered {sorted(covered_operations)}, expected {sorted(operations)}")
    if negative_count == 0:
        raise ValidationError("at least one negative behavior case is required")

    target_cp = require_string(target, "control_plane_id", "target")
    require_string(target, "environment", "target")
    require_string(target, "workspace", "target")
    deployment_writer = require_string(target, "deployment_writer_id", "target")
    if not deployment_writer.startswith("platform:"):
        raise ValidationError("target deployment writer must be centrally owned")
    if target.get("required_scope_tag") != f"api_id={api_id}":
        raise ValidationError("target.required_scope_tag must bind the exact API scope")
    if not target_cp.startswith("cp-"):
        raise ValidationError("target.control_plane_id must be a stable CP identifier")
    if not policy_version:
        raise ValidationError("central policy version is required")


def entity_tags(api_id: str, owner_id: str, writer_id: str, *extra: str) -> list[str]:
    return sorted([f"api_id={api_id}", f"owner={owner_id}", f"writer={writer_id}", *extra])


def compose_config(inputs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_inputs(inputs)
    intent = inputs["intent"]
    metadata = inputs["metadata"]
    policy = inputs["policy"]
    api_id = intent["api_id"]
    app_writer = intent["writer_id"]
    policy_writer = policy["writer_id"]
    owner_id = metadata["owner_id"]
    service_intent = intent["service"]
    route_intent = intent["route"]
    service_name = service_intent["name"]

    route = {
        "name": route_intent["name"],
        "hosts": copy.deepcopy(route_intent["hosts"]),
        "paths": copy.deepcopy(route_intent["paths"]),
        "protocols": copy.deepcopy(route_intent["protocols"]),
        "strip_path": route_intent["strip_path"],
        "preserve_host": route_intent["preserve_host"],
        "tags": entity_tags(api_id, owner_id, app_writer, "source=app/api-intent.json"),
    }
    service = {
        "name": service_name,
        "url": service_intent["url"],
        "connect_timeout": service_intent["connect_timeout_ms"],
        "read_timeout": service_intent["read_timeout_ms"],
        "write_timeout": service_intent["write_timeout_ms"],
        "retries": service_intent["retries"],
        "tags": entity_tags(api_id, owner_id, app_writer, "source=app/api-intent.json"),
        "routes": [route],
    }

    plugins: list[dict[str, Any]] = []
    provenance_entities: list[dict[str, str]] = [
        {"kind": "service", "name": service_name, "writer_id": app_writer, "source": "app/api-intent.json"},
        {"kind": "route", "name": route["name"], "writer_id": app_writer, "source": "app/api-intent.json"},
    ]
    for required in policy["required_plugins"]:
        instance_name = plugin_instance(api_id, required["control_id"])
        plugins.append(
            {
                "name": required["name"],
                "instance_name": instance_name,
                "service": service_name,
                "config": copy.deepcopy(required["config"]),
                "tags": entity_tags(
                    api_id,
                    owner_id,
                    policy_writer,
                    f"control={required['control_id']}",
                    f"policy={policy['version']}",
                    f"source={inputs['policy_path']}",
                ),
            }
        )
        provenance_entities.append(
            {
                "kind": "plugin",
                "name": instance_name,
                "writer_id": policy_writer,
                "source": inputs["policy_path"],
                "control_id": required["control_id"],
            }
        )
    for selected in intent["plugins"]:
        instance_name = plugin_instance(api_id, selected["name"], application_owned=True)
        plugins.append(
            {
                "name": selected["name"],
                "instance_name": instance_name,
                "service": service_name,
                "config": copy.deepcopy(selected["config"]),
                "tags": entity_tags(api_id, owner_id, app_writer, "source=app/api-intent.json"),
            }
        )
        provenance_entities.append(
            {"kind": "plugin", "name": instance_name, "writer_id": app_writer, "source": "app/api-intent.json"}
        )

    plugins.sort(key=lambda item: item["instance_name"])
    provenance_entities.sort(key=lambda item: (item["kind"], item["name"]))
    config = {
        "_format_version": "3.0",
        "_transform": True,
        "services": [service],
        "plugins": plugins,
    }
    provenance = {
        "schema_version": 1,
        "api_id": api_id,
        "application_source": "app/api-intent.json",
        "central_policy_source": inputs["policy_path"],
        "central_policy_version": policy["version"],
        "central_policy_sha256": digest(policy),
        "entities": provenance_entities,
    }
    return config, provenance


def writer_from_tags(value: dict[str, Any]) -> str:
    tags = value.get("tags", [])
    if not isinstance(tags, list):
        return ""
    matches = [tag.split("=", 1)[1] for tag in tags if isinstance(tag, str) and tag.startswith("writer=")]
    return matches[0] if len(matches) == 1 else ""


def has_scope(value: dict[str, Any], api_id: str) -> bool:
    tags = value.get("tags", [])
    return isinstance(tags, list) and f"api_id={api_id}" in tags


def scoped_config(config_value: Any, api_id: str) -> dict[str, Any]:
    config = require_mapping(config_value, "Kong configuration")
    services: list[dict[str, Any]] = []
    for service_value in require_list(config.get("services", []), "Kong configuration.services"):
        service = require_mapping(service_value, "Kong configuration.services[]")
        if not has_scope(service, api_id):
            continue
        selected = copy.deepcopy(service)
        selected["routes"] = sorted(
            [
                copy.deepcopy(require_mapping(route, "Kong configuration.routes[]"))
                for route in require_list(service.get("routes", []), "Kong configuration.routes")
                if has_scope(require_mapping(route, "Kong configuration.routes[]"), api_id)
            ],
            key=lambda item: str(item.get("name", "")),
        )
        services.append(selected)
    plugins = sorted(
        [
            copy.deepcopy(require_mapping(plugin, "Kong configuration.plugins[]"))
            for plugin in require_list(config.get("plugins", []), "Kong configuration.plugins")
            if has_scope(require_mapping(plugin, "Kong configuration.plugins[]"), api_id)
        ],
        key=lambda item: str(item.get("instance_name", item.get("name", ""))),
    )
    services.sort(key=lambda item: str(item.get("name", "")))
    return {"_format_version": "3.0", "_transform": True, "services": services, "plugins": plugins}


def flatten(config_value: Any, api_id: str) -> dict[tuple[str, str], dict[str, Any]]:
    config = scoped_config(config_value, api_id)
    entities: dict[tuple[str, str], dict[str, Any]] = {}
    for service in config["services"]:
        service_copy = copy.deepcopy(service)
        routes = service_copy.pop("routes", [])
        service_name = require_string(service_copy, "name", "service")
        service_key = ("service", service_name)
        if service_key in entities:
            raise ValidationError(f"conflicting writers: duplicate service {service_name} in configuration")
        entities[service_key] = service_copy
        for route in routes:
            route_name = require_string(route, "name", "route")
            route_key = ("route", route_name)
            if route_key in entities:
                raise ValidationError(f"conflicting writers: duplicate route {route_name} in configuration")
            entities[route_key] = route
    for plugin in config["plugins"]:
        plugin_name = require_string(plugin, "instance_name", "plugin")
        plugin_key = ("plugin", plugin_name)
        if plugin_key in entities:
            raise ValidationError(f"conflicting writers: duplicate plugin {plugin_name} in configuration")
        entities[plugin_key] = plugin
    return entities


def build_plan(current: Any, desired: Any, api_id: str, target_cp: str) -> dict[str, Any]:
    current_entities = flatten(current, api_id)
    desired_entities = flatten(desired, api_id)
    actions: list[dict[str, Any]] = []
    counts = {"create": 0, "change": 0, "delete": 0, "unchanged": 0}
    for key in sorted(set(current_entities) | set(desired_entities)):
        before = current_entities.get(key)
        after = desired_entities.get(key)
        if before is not None:
            current_writer = writer_from_tags(before)
            if not current_writer:
                raise ValidationError(f"conflicting writers: current {key[0]} {key[1]} has no single governed writer")
            if after is not None and current_writer != writer_from_tags(after):
                raise ValidationError(
                    f"conflicting writers: current {key[0]} {key[1]} is owned by {current_writer}, desired by {writer_from_tags(after)}"
                )
        if before is None:
            action = "create"
        elif after is None:
            action = "delete"
        elif canonical_bytes(before) != canonical_bytes(after):
            action = "change"
        else:
            action = "unchanged"
        counts[action] += 1
        if action != "unchanged":
            actions.append(
                {
                    "action": action,
                    "kind": key[0],
                    "name": key[1],
                    "before_sha256": digest(before) if before is not None else None,
                    "after_sha256": digest(after) if after is not None else None,
                    "writer_id": writer_from_tags(after or before or {}),
                }
            )
    return {
        "schema_version": 1,
        "plan_kind": "offline-equivalent-plan-not-deck-output",
        "api_id": api_id,
        "target_control_plane": target_cp,
        "scope_tag": f"api_id={api_id}",
        "summary": counts,
        "actions": actions,
    }


def build_documents(
    inputs: dict[str, Any], current: Any, application_commit: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if not COMMIT_PATTERN.fullmatch(application_commit):
        raise ValidationError("application commit must be a 40-character lower-case hexadecimal Git commit")
    config, provenance = compose_config(inputs)
    api_id = inputs["intent"]["api_id"]
    target = inputs["target"]
    plan = build_plan(current, config, api_id, target["control_plane_id"])
    pending = {
        "schema_version": 1,
        "evidence_state": "pending-review-and-deployment",
        "execution_boundary": "offline composition only; no decK or Kong execution",
        "api_id": api_id,
        "application_commit": application_commit,
        "central_policy_version": inputs["policy"]["version"],
        "central_policy_sha256": digest(inputs["policy"]),
        "generated_config_sha256": digest(scoped_config(config, api_id)),
        "generated_provenance_sha256": digest(provenance),
        "deployment_plan_sha256": digest(plan),
        "plan_review": {"status": "pending"},
        "target_control_plane": target["control_plane_id"],
        "target_environment": target["environment"],
        "deployment_writer_id": target["deployment_writer_id"],
        "active_config_sha256": None,
        "converged": False,
    }
    return config, provenance, plan, pending


def attest_release(
    generated: Any,
    plan: Any,
    pending: Any,
    review: Any,
    active: Any,
) -> dict[str, Any]:
    pending_record = require_mapping(pending, "pending evidence")
    plan_record = require_mapping(plan, "deployment plan")
    review_record = require_mapping(review, "plan review")
    api_id = require_string(pending_record, "api_id", "pending evidence")
    target_cp = require_string(pending_record, "target_control_plane", "pending evidence")
    application_commit = require_string(pending_record, "application_commit", "pending evidence")
    if not COMMIT_PATTERN.fullmatch(application_commit):
        raise ValidationError("pending evidence contains an invalid application commit")
    generated_digest = digest(scoped_config(generated, api_id))
    if pending_record.get("generated_config_sha256") != generated_digest:
        raise ValidationError("generated configuration does not match the pending evidence digest")
    plan_digest = digest(plan_record)
    if pending_record.get("deployment_plan_sha256") != plan_digest:
        raise ValidationError("deployment plan does not match the pending evidence digest")
    if review_record.get("status") != "approved":
        raise ValidationError("deployment plan review is not approved")
    if review_record.get("plan_sha256") != plan_digest:
        raise ValidationError("approved plan digest does not match the deployment plan")
    if review_record.get("target_control_plane") != target_cp:
        raise ValidationError("approved plan targets a different Control Plane")
    for key in ("review_id", "reviewer_role", "reviewed_at"):
        require_string(review_record, key, "plan review")
    if plan_record.get("target_control_plane") != target_cp or plan_record.get("api_id") != api_id:
        raise ValidationError("deployment plan target or API scope differs from pending evidence")
    active_scoped = scoped_config(active, api_id)
    active_digest = digest(active_scoped)
    if active_digest != generated_digest:
        raise ValidationError(
            f"configuration drift detected: generated {generated_digest}, active {active_digest}"
        )
    return {
        "schema_version": 1,
        "evidence_state": "supplied-active-snapshot-converged",
        "execution_boundary": "attests the supplied API-scoped snapshot; does not by itself prove a Kong deployment or request behavior",
        "api_id": api_id,
        "application_commit": application_commit,
        "central_policy_version": pending_record["central_policy_version"],
        "central_policy_sha256": pending_record["central_policy_sha256"],
        "generated_config_sha256": generated_digest,
        "generated_provenance_sha256": pending_record["generated_provenance_sha256"],
        "deployment_plan_sha256": plan_digest,
        "plan_review": {
            "status": "approved",
            "review_id": review_record["review_id"],
            "reviewer_role": review_record["reviewer_role"],
            "reviewed_at": review_record["reviewed_at"],
        },
        "target_control_plane": target_cp,
        "target_environment": pending_record["target_environment"],
        "deployment_writer_id": pending_record["deployment_writer_id"],
        "active_config_sha256": active_digest,
        "active_snapshot_sha256": digest(active),
        "converged": True,
    }


def resolve_from(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def command_validate(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    inputs = load_inputs(root)
    validate_inputs(inputs)
    print(
        "OK: federated delivery inputs validated; mandatory controls, one-writer registry, "
        "route safety, ownership, exceptions, and operation tests fail closed"
    )


def command_compose(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    output = resolve_from(root, args.output)
    inputs = load_inputs(root)
    current = read_json(resolve_from(root, args.current))
    config, provenance, plan, pending = build_documents(inputs, current, args.app_commit)
    write_json(output / "kong.json", config)
    write_json(output / "provenance.json", provenance)
    write_json(output / "deployment-plan.json", plan)
    write_json(output / "evidence-pending.json", pending)
    print(
        "OK: composed deterministic synthetic candidate and pending evidence under "
        f"{output}; no decK or Kong execution is claimed"
    )


def command_attest(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    result = attest_release(
        read_json(resolve_from(root, args.generated)),
        read_json(resolve_from(root, args.plan)),
        read_json(resolve_from(root, args.pending_evidence)),
        read_json(resolve_from(root, args.review)),
        read_json(resolve_from(root, args.active)),
    )
    output = resolve_from(root, args.output)
    write_json(output, result)
    print(f"OK: supplied active snapshot converges to the approved generated configuration; wrote {output}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="validate the synthetic reference inputs")
    validate.add_argument("--root", default=".")
    validate.set_defaults(handler=command_validate)

    compose = subcommands.add_parser("compose", help="compose a deterministic candidate and review plan")
    compose.add_argument("--root", default=".")
    compose.add_argument("--output", required=True)
    compose.add_argument("--app-commit", required=True)
    compose.add_argument("--current", required=True)
    compose.set_defaults(handler=command_compose)

    attest = subcommands.add_parser("attest", help="bind an approved plan to a supplied active snapshot")
    attest.add_argument("--root", default=".")
    attest.add_argument("--generated", required=True)
    attest.add_argument("--plan", required=True)
    attest.add_argument("--pending-evidence", required=True)
    attest.add_argument("--review", required=True)
    attest.add_argument("--active", required=True)
    attest.add_argument("--output", required=True)
    attest.set_defaults(handler=command_attest)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
