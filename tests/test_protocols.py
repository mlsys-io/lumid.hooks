"""Smoke tests for the shared protocols.

The example `simple_plugin` doubles as the conformance fixture — every hook
class it ships is asserted to satisfy the runtime-checkable protocol.
"""

import dataclasses

from examples.simple_plugin import install
from examples.simple_plugin.identity import SimpleIdentityProvider
from examples.simple_plugin.permissions import SimplePermissionChecker
from examples.simple_plugin.registrar import SimpleResourceRegistrar
from examples.simple_plugin.submission import SimpleSubmissionGuard
from examples.simple_plugin.usage import SimpleUsageSink

from lumid_hooks import (
    BaseBindings,
    HookBindings,
    IdentityProvider,
    PermissionChecker,
    PrincipalContext,
    ResourceRef,
    ResourceRegistrar,
    SubmissionGuard,
    UsageSink,
)


def test_simple_plugin_classes_satisfy_protocols() -> None:
    assert isinstance(SimpleIdentityProvider(), IdentityProvider)
    assert isinstance(SimpleSubmissionGuard(), SubmissionGuard)
    assert isinstance(SimplePermissionChecker(), PermissionChecker)
    assert isinstance(SimpleResourceRegistrar(), ResourceRegistrar)
    assert isinstance(SimpleUsageSink(), UsageSink)


def test_install_returns_hookbindings_protocol_conformant() -> None:
    bindings = install()
    assert isinstance(bindings, BaseBindings)
    assert isinstance(bindings, HookBindings)


def test_base_bindings_defaults_are_empty() -> None:
    bindings = BaseBindings()
    for f in dataclasses.fields(bindings):
        assert len(getattr(bindings, f.name)) == 0


def test_principal_context_is_frozen() -> None:
    p = PrincipalContext(
        principal_id="x",
        org_id="o",
        external_id="x@e",
        principal_type="user",
        scopes=["a"],
    )
    try:
        p.principal_id = "y"  # type: ignore[misc]
    except (TypeError, ValueError):
        return
    raise AssertionError("PrincipalContext should be frozen")


def test_resource_ref_defaults() -> None:
    r = ResourceRef(kind="document")
    assert r.id is None
    assert r.metadata == {}
