"""`simple_plugin` — runnable example exercising every shared hook.

In-memory state lives in `state` and every hook reads/writes it. The
`install()` entry point returns a `lumid_hooks.BaseBindings` — the shared
concrete convenience class. A host that extends `BaseBindings` with extra
fields still accepts this plugin because its Protocol gate only requires the
five shared fields, which `BaseBindings` provides.

NOT FOR PRODUCTION. See README.md.
"""

from lumid_hooks import BaseBindings

from .identity import SimpleIdentityProvider
from .permissions import SimplePermissionChecker
from .registrar import SimpleResourceRegistrar
from .submission import SimpleSubmissionGuard
from .usage import SimpleUsageSink


def install() -> BaseBindings:
    return BaseBindings(
        identity_providers=(SimpleIdentityProvider(),),
        submission_guards=(SimpleSubmissionGuard(),),
        usage_sinks=(SimpleUsageSink(),),
        permission_checkers=(SimplePermissionChecker(),),
        resource_registrars=(SimpleResourceRegistrar(),),
    )


__all__ = ["install"]
