# Implementation Plan: Repeat Trade Risk CLI Margin Calculator

## 1. Summary

Implement a first-version CLI application that calculates required margin for a repeat trading strategy based on user-provided strategy inputs and a specified amount range.

The implementation will use a layered structure:
- CLI layer for argument parsing and output
- domain calculation layer for pure margin logic
- validation layer for input contracts and error handling

This plan intentionally focuses on a minimal, testable first release and identifies blocker decisions that must be finalized before coding.

## 2. User Request

Create an implementation plan for a script that supports risk management in repeat trading with these requirements:
- Accept strategy inputs (trade currency quantity, order interval, order range)
- Calculate required margin for a specified amount range
- Implement first as a CLI-based application
- Organize and clarify additional points that should be decided before implementation

## 3. Source Material

### Repository Files

- [AGENTS.md](AGENTS.md)
- [pyproject.toml](pyproject.toml)
- [README.md](README.md)
- [README_en.md](README_en.md)
- [src/fx_risk_management/__init__.py](src/fx_risk_management/__init__.py)
- [tests/test_smoke.py](tests/test_smoke.py)
- [.pre-commit-config.yaml](.pre-commit-config.yaml)
- [scripts/pre-commit/checks.sh](scripts/pre-commit/checks.sh)
- [scripts/pre-commit/ruff-format.sh](scripts/pre-commit/ruff-format.sh)
- [scripts/pre-commit/ruff-check.sh](scripts/pre-commit/ruff-check.sh)
- [scripts/pre-commit/mypy.sh](scripts/pre-commit/mypy.sh)
- [scripts/pre-commit/pytest.sh](scripts/pre-commit/pytest.sh)
- [docker/run-docker.sh](docker/run-docker.sh)
- [docker/Dockerfile](docker/Dockerfile)
- [docker/docker-compose.yml](docker/docker-compose.yml)
- [docker/entrypoint.sh](docker/entrypoint.sh)

### Delegated Reports

- Context research by `implementation-plan-context-researcher`
- Strategy design by `implementation-plan-strategy-designer`
- Draft quality review by `implementation-plan-quality-reviewer`

## 4. Delegation Log

| Role | Delegated | Result Used | Notes |
| --- | --- | --- | --- |
| `implementation-plan-context-researcher` | Yes | Yes | Confirmed current repository state, tooling flow, and missing domain definitions. |
| `implementation-plan-strategy-designer` | Yes | Yes | Proposed practical phased approach and file-level change structure. |
| `implementation-plan-quality-reviewer` | Yes | Yes | Identified blocker gaps (formula, input contract, conversion, validation contract) and required fixes incorporated into this plan. |

## 5. Confirmed Current State

- CLI application for this domain is not implemented yet.
- Business/domain logic for repeat-trade margin calculation does not exist in source code.
- Source package currently contains only [src/fx_risk_management/__init__.py](src/fx_risk_management/__init__.py).
- Tests are minimal and currently include only smoke coverage in [tests/test_smoke.py](tests/test_smoke.py).
- `project.scripts` console entry point is not configured in [pyproject.toml](pyproject.toml).
- Quality workflow is defined via wrapper scripts and pre-commit settings.
- Known validation caveat from repo memory: pytest wrapper can fail in CPU mode due to `profile_args[@]` unbound variable in [docker/run-docker.sh](docker/run-docker.sh).

## 6. Requirements

### Functional Requirements

- [ ] Provide a CLI command that accepts strategy inputs and amount-range inputs.
- [ ] Compute required margin across the specified amount range.
- [ ] Output calculated results in a deterministic, documented format.
- [ ] Validate invalid inputs and return actionable errors.

### Non-Functional Requirements

- [ ] Keep implementation small, readable, and testable.
- [ ] Use type hints for public functions and modules.
- [ ] Keep dependencies minimal (prefer standard library for CLI in v1).
- [ ] Ensure output reproducibility via explicit numeric precision rules.

### Compatibility Requirements

- [ ] Align with project tooling in [pyproject.toml](pyproject.toml) (ruff, mypy, pytest).
- [ ] Preserve existing package behavior and avoid unrelated refactors.
- [ ] Support repository execution model (host and Docker wrapper workflows).

## 7. Assumptions

- Initial release targets single-strategy calculation per command invocation.
- Initial release uses standard-library CLI parsing (`argparse`) unless blocker decisions require otherwise.
- Initial release focuses on required margin and does not include full PnL simulation.
- Currency conversion input is provided explicitly by user or constrained by agreed scope.

## 8. Open Questions

### Blocking

- What is the exact required-margin formula and variable definition set?
  - Include leverage treatment, contract size interpretation, and whether to include additional risk buffer.
- What are the official units for each input?
  - Trade quantity (`lot` vs base units), order interval (`pips` vs price delta), order range unit.
- How should amount range be generated?
  - Inclusive boundaries, step defaults, descending-range support.
- What conversion rule applies when account currency differs from pair quote/base?
  - Rate source, rate input contract, and failure behavior if rate is missing.
- What numeric precision policy should be used?
  - `float` vs `Decimal`, rounding mode, and output decimal places.

### Non-Blocking

- Should output include machine-readable mode (`json`) in v1 or only human-readable table/text?
- Should both [README.md](README.md) and [README_en.md](README_en.md) be updated in the same change?
- Do we need a standardized exit-code map beyond success/input-error/internal-error?

## 9. Proposed Approach

Implement a minimal but extensible architecture with clear module responsibilities:

- `cli` module:
  - parse command-line options
  - map parsed values into typed input models
  - call domain calculation
  - print output and return process exit code
- `validation` module:
  - validate input ranges, signs, and inter-parameter consistency
  - raise explicit exceptions/messages for user-facing failures
- `margin` module:
  - pure functions for range expansion and required-margin calculation
  - deterministic numeric behavior and no I/O

This separates business logic from transport concerns (CLI), enabling stable unit tests and future API/UI reuse.

## 10. Considered Options

### Option A: Single-file CLI (all logic in one module)

Pros:
- Fastest initial coding
- Minimal file count

Cons:
- Poor test isolation
- Hard to extend safely
- Mixes validation/logic/presentation concerns

Decision:
- Rejected.

### Option B: Layered CLI + validation + domain modules (selected)

Pros:
- Strong testability
- Maintains clear responsibilities
- Scales to future interfaces

Cons:
- Slightly higher initial setup cost

Decision:
- Selected as best tradeoff for v1 and future growth.

### Option C: Introduce external CLI framework (Typer/Click)

Pros:
- Better CLI UX out of the box
- Easier command expansion

Cons:
- Adds dependency and maintenance overhead
- Not required for v1 scope

Decision:
- Rejected for v1 (can be revisited later).

## 11. Implementation Steps

### Phase 1: Contract Definition (must complete before coding)

- [ ] Finalize margin formula with parameter glossary and worked example.
- [ ] Finalize input contract table (name, type, unit, bounds, required/default).
- [ ] Finalize range-generation rules (boundary inclusion, step semantics).
- [ ] Finalize output contract (columns/fields, unit labels, rounding).
- [ ] Finalize error contract (exit codes and stderr policy).

Done criteria:
- A written spec section exists in this plan or linked doc, and all blocking questions are resolved.

### Phase 2: Core Modules

- [ ] Add `margin.py` with pure calculation helpers and deterministic numeric handling.
- [ ] Add `validation.py` with explicit input checks and clear error messages.
- [ ] Add tests for domain and validation behavior before CLI integration completion.

Done criteria:
- Domain and validation tests pass locally for normal, boundary, and invalid cases.

### Phase 3: CLI Integration

- [ ] Add `cli.py` with `argparse` command and structured argument definitions.
- [ ] Wire CLI to validation and calculation modules.
- [ ] Add console entry point in [pyproject.toml](pyproject.toml).
- [ ] Keep [src/fx_risk_management/__init__.py](src/fx_risk_management/__init__.py) compatibility.

Done criteria:
- CLI command executes with expected output and error behavior.

### Phase 4: Documentation and Hardening

- [ ] Add usage examples and parameter explanations to [README.md](README.md).
- [ ] Mirror docs in [README_en.md](README_en.md) if decided in scope.
- [ ] Document assumptions, limitations, and unsupported scenarios.

Done criteria:
- README sections allow a new user to run the command correctly.

### Phase 5: Final Validation

- [ ] Run lint/format/type/test checks via repository wrappers where possible.
- [ ] If wrapper issue reproduces, run documented fallback and record reason.

Done criteria:
- Validation outcomes recorded and consistent with acceptance criteria.

## 12. File-Level Change Plan

| File | Planned Change |
| --- | --- |
| [pyproject.toml](pyproject.toml) | Add CLI console script entry point for risk margin command. |
| [src/fx_risk_management/__init__.py](src/fx_risk_management/__init__.py) | Keep stable exports; optionally expose version/entry metadata if needed. |
| src/fx_risk_management/cli.py | New CLI module using `argparse`, error handling, and command execution flow. |
| src/fx_risk_management/margin.py | New pure calculation module for required margin and range handling. |
| src/fx_risk_management/validation.py | New input validation module and domain-specific validation errors. |
| [tests/test_smoke.py](tests/test_smoke.py) | Keep smoke checks; adjust only if needed for package entry behavior. |
| tests/test_margin.py | New unit tests for formula correctness, boundaries, and numeric stability. |
| tests/test_cli.py | New CLI tests for valid/invalid input, output format, and exit codes. |
| [README.md](README.md) | Add CLI usage, parameter contract, and examples. |
| [README_en.md](README_en.md) | Add equivalent English usage notes if included in scope. |

## 13. Validation Plan

### Automated Checks

Run in this order:

```bash
./scripts/pre-commit/ruff-format.sh
./scripts/pre-commit/ruff-check.sh --fix
./scripts/pre-commit/mypy.sh .
./scripts/pre-commit/pytest.sh
```

If pytest wrapper fails due to known CPU-mode wrapper issue, use fallback:

```bash
python -m pytest -q
```

Final optional aggregate check:

```bash
./scripts/pre-commit/checks.sh
```

Expected result:
- Lint, formatting, typing, and tests succeed for changed scope.
- CLI behavior is validated by automated tests.

### Manual Verification

- Run `--help` and confirm argument descriptions and units are clear.
- Run a known sample input and verify expected margin values.
- Verify invalid inputs produce non-zero exit code and clear stderr messages.
- Verify range boundary behavior matches defined contract.

## 14. Risks and Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Formula ambiguity | High | Block implementation until formula and units are signed off. |
| Currency conversion ambiguity | High | Define conversion contract explicitly and add targeted tests. |
| Numeric precision drift | Medium | Choose and document numeric policy (`Decimal` preferred if precision-critical) and lock expected values in tests. |
| CLI contract churn | Medium | Freeze argument names and output schema in v1 docs/tests. |
| Wrapper-based pytest instability | Medium | Use documented fallback during validation and track wrapper fix as separate follow-up task. |

## 15. Rollback Plan

- Keep changes in small commits by phase.
- If CLI integration causes issues, revert console script exposure in [pyproject.toml](pyproject.toml) first while retaining internal modules.
- If formula implementation is disputed, revert `margin.py` and related tests together to avoid partial behavior.
- Preserve smoke and existing baseline behavior while removing only newly introduced CLI paths.

## 16. Done Criteria

The implementation is complete when:

- [ ] Blocking questions in Section 8 are resolved and documented.
- [ ] CLI command accepts required strategy inputs and amount range.
- [ ] Required margin is computed correctly according to finalized formula.
- [ ] Input validation and error contracts are implemented and tested.
- [ ] Unit and CLI tests are added and pass.
- [ ] Ruff, Mypy, and Pytest checks pass via standard flow or documented fallback.
- [ ] README usage and constraints are updated for in-scope languages.
- [ ] No unrelated code or configuration changes are included.

## 17. Recommended Next Step

Resolve the blocking decisions in Section 8 (formula, units, range rule, conversion rule, precision policy), then approve this plan for implementation phase execution.
