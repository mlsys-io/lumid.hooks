"""Shared bindings shape — Protocol contract + concrete convenience class.

`HookBindings` is a runtime-checkable Protocol describing the five fields every
host project agrees on. Hosts use it for the `isinstance` gate at plugin load
time; structural typing means a plugin's bindings object satisfies the Protocol
by having the right field names, without inheriting from anything. Fields are
declared read-only so frozen dataclass instances satisfy the Protocol under
mypy.

`BaseBindings` is a frozen dataclass that ships the same five fields with empty
default factories. Plugins targeting one host use `BaseBindings` (or a host's
subclass like `flowmesh_hook.BaseBindings`) directly. Plugins targeting
multiple hosts subclass `BaseBindings` and add each host's extra field names —
each host's loader picks up the fields it knows about via the host's own
Protocol.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from .identity import IdentityProvider
from .permissions import PermissionChecker
from .registrar import ResourceRegistrar
from .submission import SubmissionGuard
from .usage import UsageSink


@runtime_checkable
class HookBindings(Protocol):
    @property
    def identity_providers(self) -> Sequence[IdentityProvider]: ...
    @property
    def submission_guards(self) -> Sequence[SubmissionGuard]: ...
    @property
    def usage_sinks(self) -> Sequence[UsageSink[Any]]: ...
    @property
    def permission_checkers(self) -> Sequence[PermissionChecker]: ...
    @property
    def resource_registrars(self) -> Sequence[ResourceRegistrar]: ...


@dataclass(frozen=True)
class BaseBindings:
    identity_providers: Sequence[IdentityProvider] = field(default_factory=tuple)
    submission_guards: Sequence[SubmissionGuard] = field(default_factory=tuple)
    usage_sinks: Sequence[UsageSink[Any]] = field(default_factory=tuple)
    permission_checkers: Sequence[PermissionChecker] = field(default_factory=tuple)
    resource_registrars: Sequence[ResourceRegistrar] = field(default_factory=tuple)
