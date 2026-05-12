"""`SubmissionGuard` example: blocklist by `principal_id`.

Add a principal id to `state.BLOCKED_PRINCIPALS` to make this guard reject
that principal's submissions. Real plugins typically check billing balance,
quota, or per-tenant feature flags here.
"""

import logging

from lumid_hooks import PrincipalContext

from . import state


class _BlockedError(RuntimeError):
    """Raised by `SimpleSubmissionGuard` when the principal is blocked.

    Real plugins typically raise FastAPI's `HTTPException(403, ...)` so the
    host returns a structured error to the caller; this example uses a plain
    exception to avoid pulling fastapi into `lumid-hooks`.
    """


class SimpleSubmissionGuard:
    name = "simple_plugin.guard"

    async def check(self, principal: PrincipalContext, logger: logging.Logger) -> None:
        if principal.principal_id in state.BLOCKED_PRINCIPALS:
            logger.warning(
                "%s: blocked principal_id=%s", self.name, principal.principal_id
            )
            raise _BlockedError(f"principal {principal.principal_id} is blocked")
        logger.info("%s: allowed principal_id=%s", self.name, principal.principal_id)
