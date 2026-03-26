# NSAK — Code Quality & Design Assessment

## Overview

| Dimension | Grade | Summary |
|---|---|---|
| Type annotations | A | Strict mypy, frozen dataclasses throughout |
| Error handling | B+ | Good hierarchy; silent failures in loaders |
| Abstractions | A– | Clean generics; manager layer is thin |
| Resource Manager pattern | B+ | Consistent but load-time CLI baking |
| Coupling / cohesion | C+ | Global config state; DeviceManager side-effects |
| Circular imports | A | None detected |
| CLI separation | B | Thin wrappers, but tightly coupled to device state |
| Test coverage | C | Mostly integration; execution paths untested |
| Subprocess safety | C | TODOs acknowledge the issue; not yet resolved |

---

## Type Annotations & Data Modelling

**Strength.** The codebase runs `mypy --strict` and passes. All resource models are frozen dataclasses (`frozen=True, kw_only=True`), making them fully immutable after construction. Modern union syntax (`Path | str`, `Device | str`) is used consistently, and generic types (`ResourceManager[T]`, `ResourceLoader[T]`) provide compile-time safety across four resource types without code duplication.

The only systematic workaround is `# noqa: ANN401` on every `*args`/`**kwargs` parameter — unavoidable given the dynamic CLI argument forwarding, but worth noting.

**Weakness.** Type checking for drill/scenario arguments is string-based at runtime:

```python
# drill_manager.py
if type(value).__name__ not in argument.type:
    message = f"Invalid type {type(value)} for argument {name}, expected {argument.type}."
```

`argument.type` is a raw string from YAML (`"str"`, `"int"`, etc.), compared against `type(value).__name__`. This doesn't handle subclasses, type aliases, or anything beyond primitives.

---

## Resource Manager Pattern

The three-layer pattern (`ResourceLoader[T]` → `ResourceManager[T]` → CLI command group) is the architectural backbone and is applied identically to all four resource types (Device, Drill, Scenario, Environment).

**Strength.** The template method in `ResourceLoader` is clean — `_find()`, `_load()`, and `_search()` are concrete; `_to_resource()` is abstract per subclass. The YAML key structure (`resources[drills][drill_id]`) maps naturally to the CLI hierarchy.

**Weakness 1 — thin manager.** `ResourceManager` is 25 lines and only delegates:

```python
class ResourceManager[T]:
    ResourceLoaderClass: type[ResourceLoader[T]]

    @classmethod
    def list(cls) -> List[T]:
        return cls.ResourceLoaderClass.load_all()
```

All domain logic lives in the individual manager subclasses (`DrillManager`, `ScenarioManager`, etc.), not in the base. The base class adds almost no value over a free function or Protocol.

**Weakness 2 — silent failures.** During `load_all()`, `InvalidResourceError` is caught, logged as a warning, and the resource is skipped. Corrupted or malformed YAML silently disappears from the CLI with no user-facing error.

**Weakness 3 — no schema validation.** The YAML structure is assumed, not validated. A missing key in `resource_loader.py:108` raises a bare `KeyError`, not an `InvalidResourceError`:

```python
resource_data = data[cls.ResourceClass.KEY][id]
```

---

## Coupling & Cohesion

This is the weakest architectural area.

**Global mutable config.** A `lazy-object-proxy.Proxy` wrapping `Config.load()` is exported as a module-level singleton. Every CLI module and several managers import and mutate it directly. The lazy proxy is clever — it avoids filesystem I/O during shell completion — but it obscures when and why initialization can fail.

**DeviceManager violates single responsibility.** It mutates the global config as a side effect of `load()`:

```python
# device_manager.py
@classmethod
def load(cls, name: str) -> Device:
    from nsak.core import config
    device = cls.get(name)
    config.device = device   # side-effect
    config.save()            # disk write
```

A `get()` on a manager is expected to be a pure read. Persistence belongs elsewhere.

**CLI is coupled to device state at import time.** Drill and scenario commands check `config.device.target_ethernets` during command *generation*, not during command *execution*:

```python
# cli/drill.py
if name == "interface":
    kwargs["type"] = click.Choice(config.device.target_ethernets.keys())
```

If no device is loaded (`device.id == "unknown"`, no target ethernets), this silently produces an empty choice list. The CLI is generated at startup and baked in — adding a new drill to `lib/` requires restarting the process.

---

## Dynamic Module Loading

Drills and scenarios are loaded at runtime via `importlib.util.spec_from_file_location()`. The design is appropriate for a plugin-style framework, but the implementation has several gaps:

```python
# drill_manager.py
spec = importlib.util.spec_from_file_location(module_name, drill.path / "drill.py")
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)   # no try/except — fails hard on syntax errors
run_fn = getattr(module, "run", None)
```

1. `exec_module()` has no try/except. A syntax error in any drill crashes the process.
2. The module is registered in `sys.modules` under `drill.path.name`. Two drills in folders with the same name would silently collide.
3. Modules are never removed from `sys.modules` after execution, causing a memory leak when drills are executed repeatedly in the same process.
4. There is no check that `run()` matches the expected signature declared in the drill's `DrillInterface`.

---

## Subprocess Usage

Three separate `subprocess.run()` calls invoke `sudo podman`, `sudo podman build`, and `sudo podman-compose`. All three are annotated with the same TODO:

```python
# scenario_manager.py
# @TODO: This is potentially insecure and we should replace it with a library:
# - https://pypi.org/project/docker/
# - https://pypi.org/project/podman/
return subprocess.run(  # noqa: S603
    ["/usr/sbin/sudo", "/usr/bin/podman", "build", ...]
```

The problems are:
- **No return code checking.** A failed build or run is not distinguished from success.
- **Hardcoded binary paths.** `/usr/sbin/sudo`, `/usr/sbin/podman-compose` — will fail on systems with different layouts.
- **sudo escalation.** Elevating privilege inside a Python process is a trust boundary that should be explicit and auditable.
- **S603 suppressed.** The ruff security check is disabled rather than addressing the root cause.

The authors are aware and have identified the fix. Using `podman-py` or `docker-py` would remove the subprocess dependency entirely.

---

## Testing

**What is tested.** CLI commands (`test_device.py`, `test_drill.py`) are tested well using `click.testing.CliRunner` and `unittest.mock`. These are the highest-quality tests in the suite.

**What is not tested.**

| Untested path | Risk |
|---|---|
| `DrillManager.execute()` | Core execution path — dynamic import, argument parsing, `run()` call |
| `ScenarioManager.build()` / `run()` | Subprocess calls, return code handling |
| `_parse_arguments()` type coercion | Type mismatch, missing required args, unknown args |
| Exception paths in loaders | Missing YAML key, malformed structure |
| `Config.load()` / `Config.save()` | Deserialization edge cases, missing file |

**Integration tests masquerading as unit tests.** Most core tests load real resources from `lib/`:

```python
# test_drill_manager.py — comment in the file itself
# This test could be improved by mocking the drill library, but is good enough for now.
def test_drill_manager() -> None:
    drill_list = DrillManager.list()
    assert len(drill_list) > 0
```

These tests are brittle (break if `lib/` is empty or resources change), and they assert almost nothing about the data returned.

---

## Miscellaneous

**Typo in a public class name.** `DeviceConfigration` appears in `device.py`, `device_loader.py`, `device_manager.py`, and tests. Should be `DeviceConfiguration`. It's a cosmetically minor but visible issue.

**`functools.cache` on a classmethod** in `ResourceLoader.get_search_paths()` caches globally for the lifetime of the process. If `NSAK_BASE_PATH` changes at runtime (unlikely but possible in tests), the cached value is stale. The test suite may be affected if search paths are shared across test cases.

**Config deserialization is unvalidated:**

```python
# _config.py
_config = cls(**data)  # raw YAML dict unpacked into dataclass
```

If the YAML file is missing a field, or contains an extra field from an older version, `TypeError` is caught but logged without surfacing to the user. Silent config degradation is hard to debug.

---

## Recommendations

**High priority**
- Add `try/except` around `exec_module()` in drill/scenario loaders; raise a meaningful error.
- Check subprocess return codes in `ScenarioManager`; raise `ScenarioError` on non-zero exit.
- Test `DrillManager.execute()` and `_parse_arguments()` with mocked drills.
- Clean up `sys.modules` entries after dynamic module execution.

**Medium priority**
- Replace `subprocess.run([sudo, podman, ...])` with `podman-py` or `docker-py`.
- Rename `DeviceConfigration` → `DeviceConfiguration` (breaking change, but correct).
- Add YAML schema validation in `ResourceLoader._load()` using `jsonschema` or pydantic.
- Make config initialization explicit at CLI startup rather than lazy.

**Low priority**
- Consider making `ResourceManager` a Protocol or removing it — the base adds minimal value over direct loader calls.
- Document the required YAML key structure in `ResourceLoader` docstrings.
- Investigate whether CLI command registration can be deferred to execution time to support hot-reload.
