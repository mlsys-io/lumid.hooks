# lumid-hooks

Shared plugin contract surface for Lumid projects. Defines the protocols and
shared types that downstream projects compose with their own resource vocabulary
and project-specific extension points.

## What's in scope

Generic protocols and shared types every project agrees on:

- `PrincipalContext` — identity envelope returned by `IdentityProvider`.
- `ResourceRef` — `(kind, id, metadata)` triple for resource-scoped checks.
- `IdentityProvider` — bearer-token to principal resolution.
- `SubmissionGuard` — pre-submission gate.
- `PermissionChecker` — bulk filter (`accessible_ids`) and point check (`require`).
- `ResourceRegistrar` — resource lifecycle fan-out (`register` / `deregister`).
- `UsageSink[Row]` — generic per-row usage emission.
- `HookBindings` — runtime-checkable Protocol describing the five shared
  fields a plugin's bindings object exposes. Hosts gate against this Protocol
  at load time; structural typing means a plugin satisfies it by having the
  right field names without importing host packages.
- `BaseBindings` — frozen dataclass with the five fields default-factoried to
  empty tuples. Plugins targeting one host can return `BaseBindings(...)`
  directly; plugins targeting multiple hosts subclass `BaseBindings` and add
  each host's extra field names alongside.

## What's out of scope

Project-specific resource types and actions, and project-specific extension
points (e.g. FlowMesh's `SupplierResolver`). Each project ships its own
Protocol that extends `HookBindings` plus a `BaseBindings` subclass with the
project's extra field.

## Runtime dependency

`pydantic>=2.12.3` for `PrincipalContext` and `ResourceRef`. No other runtime
dependencies — plugins can `pip install lumid-hooks` without pulling in any
project's heavy core stack.
