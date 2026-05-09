# `simple_plugin`

A self-contained example exercising every shared `lumid_hooks` protocol
against an in-memory store.

> **Not for production.** Tokens are plaintext in source, all state is
> dropped on restart, and every hook is permissive by design. Use this only
> for poking at the contract.

## What each hook does here

| File | Hook | Behavior |
|------|------|----------|
| `identity.py` | `IdentityProvider` | Looks the bearer token up in `state.TOKENS`. Returns the matching `PrincipalContext`, or `None` (defer to next provider). |
| `submission.py` | `SubmissionGuard` | Rejects if `principal_id` is in `state.BLOCKED_PRINCIPALS`. |
| `usage.py` | `UsageSink[DemoUsageRow]` | Appends each row to `state.USAGE_LEDGER`; logs the running ledger size. |
| `permissions.py` | `PermissionChecker` | Admin scope bypasses every check. Otherwise `accessible_ids` returns the resources the principal owns; `require` allows kind-level (`ResourceRef.id is None`) actions for any non-empty scope and concrete-id actions only when the principal is the registered owner. |
| `registrar.py` | `ResourceRegistrar` | Records `(kind, id) -> principal_id` in `state.OWNERSHIP` on `register`; drops the row on `deregister`. |

`state.py` holds every shared dict / set / list. `__init__.py` wires the
five hook classes into a `lumid_hooks.BaseBindings` and exposes `install()`.

## Demo principals

| Token | `principal_id` | `org_id` | `scopes` |
|-------|----------------|----------|----------|
| `demo-admin-token` | `alice` | `demo` | `["admin"]` |
| `demo-user-token` | `bob` | `demo` | `["user"]` |

## How a host project consumes it

`lumid-hooks` is a contract package — it does not ship a runtime, so
`install()` does not "load" anywhere on its own. A host project imports
`simple_plugin.install`, calls it, and drains the returned bindings into
its own runtime registries:

```python
from simple_plugin import install
bindings = install()
for ip in bindings.identity_providers: ...   # host-defined wiring
```

`install()` returns a plain `lumid_hooks.BaseBindings`. The host's loader
gates on the `lumid_hooks.HookBindings` Protocol — `BaseBindings` satisfies
it structurally — so the host accepts this plugin and drains only the five
shared fields it knows about.

## Caveats

- Every store is in-process Python state. A restart wipes it.
- Tokens are committed plaintext. Real plugins should not ship secrets.
- `PermissionChecker` here is intentionally permissive (any non-empty scope
  passes kind-level checks). Real plugins should map specific scopes to
  specific `(kind, action)` pairs.
- The example raises plain `RuntimeError` subclasses on deny / block. Real
  plugins running under FastAPI hosts typically raise `HTTPException(403)`
  so the host returns a structured error to the caller; `lumid-hooks`
  itself does not depend on `fastapi`.
