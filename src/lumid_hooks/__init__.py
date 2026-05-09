"""lumid-hooks — shared plugin contract surface.

Plugins implement the protocols defined here; each host project wires them
into its own runtime registries via a project-specific bindings dataclass
that structurally satisfies `HookBindings`.
"""

from .bindings import BaseBindings, HookBindings
from .identity import IdentityProvider
from .permissions import PermissionChecker
from .principal import PrincipalContext
from .registrar import ResourceRegistrar
from .resource import ResourceRef
from .submission import SubmissionGuard
from .usage import UsageSink

__all__ = [
    "BaseBindings",
    "HookBindings",
    "IdentityProvider",
    "PermissionChecker",
    "PrincipalContext",
    "ResourceRef",
    "ResourceRegistrar",
    "SubmissionGuard",
    "UsageSink",
]
