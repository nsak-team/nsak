# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run a single test file or test
uv run pytest src/nsak/core/device/tests/test_device_manager.py
uv run pytest src/nsak/core/device/tests/test_device_manager.py::test_device_manager

# Lint (check and auto-fix)
uvx ruff check
uvx ruff check --fix

# Type check
uvx mypy

# Build package
uv build
```

Pre-commit hooks run ruff (linter + formatter) and mypy (strict mode) automatically on commit.

## Architecture

### Resource Manager Pattern

Every resource type (Device, Drill, Scenario, Environment) follows the same three-layer pattern:

```
ResourceLoader[T]  →  ResourceManager[T]  →  CLI command group
```

- **Loader** (`*_loader.py`): Scans `LIBRARY_PATHS` (defaults to `lib/`) for `{type}.yaml` files, parses YAML, constructs frozen dataclasses via `_to_resource()`.
- **Manager** (`*_manager.py`): Thin wrapper over the loader; adds type-specific operations (execute, build, run, load/unload).
- **Resource** (`*_resource.py`): Frozen dataclass carrying metadata + type-specific fields.

Error hierarchy: `ResourceError` → `InvalidResourceError` / `ResourceNotFoundError` / `MultipleResourcesFoundError`.

### Dynamic Execution (Drills & Scenarios)

Drills and Scenarios are arbitrary Python files (`drill.py` / `scenario.py`) loaded at runtime via `importlib.util.spec_from_file_location()`. Each must expose a `run(**kwargs)` function; `cleanup()` is optional for drills.

The `DrillInterface` / `ScenarioInterface` declared in YAML describes typed arguments (name → type + default). `DrillManager._parse_arguments()` validates and coerces kwargs against this interface before calling `run()`. The same interface is used to auto-generate Click options for each drill/scenario at CLI startup.

### Configuration & Paths (`core/settings.py`, `core/_config.py`)

`BASE_PATH` is determined by `NSAK_BASE_PATH` env var or derived from the installed module location (project root). Runtime state is persisted to `run/config.yaml` (currently-loaded device). The global `config` object in `_config.py` uses `lazy-object-proxy.Proxy` so the config file is only read on first attribute access — important for shell completion to work without filesystem side effects.

### Device Network Configuration

Devices declare Netplan-inspired network config in their YAML. Each Ethernet interface has addresses tagged with `is_target` (interface under test / attack surface) and `is_management` (interface for control traffic). The `network: "auto"` shorthand triggers Scapy-based interface discovery at load time. Loading a device persists it to `run/config.yaml` so subsequent CLI invocations retain state.

### Scenario Containerization

`ScenarioManager.build()` and `.run()` use Podman. Before building, `collect_dependencies()` walks the scenario's transitive drill/scenario graph to aggregate all Python and system package dependencies into a single `ScenarioDependencies` object used to generate the container image.

### Test Layout

Tests live alongside the modules they test: `src/nsak/{module}/tests/test_{module}.py`. CLI tests use `click.testing.CliRunner`; unit tests use `unittest.mock`. Some tests load real resources from `lib/` (integration-style).
