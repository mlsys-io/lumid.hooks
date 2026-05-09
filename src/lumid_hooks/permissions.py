"""Permission-checker hook.

Filters and gates access to project-defined resources. The two methods cover
the two read patterns:

- `accessible_ids` — bulk filter for list endpoints. Returns either `None`
  (no filter) or a `frozenset[str]` of resource ids the principal may see.
- `require` — point check for get / cancel / mutate endpoints. Raises
  to deny (FastAPI's HTTPException(403) is the documented choice).

Multiple checkers compose conjunctively: `require` denies if any checker
denies, and `accessible_ids` returns the intersection of returned id sets
(checkers returning `None` impose no filter and are skipped). With no checkers
registered, or every checker returning `None`, both helpers are no-ops.
"""

import logging
from typing import Protocol, runtime_checkable

from .principal import PrincipalContext
from .resource import ResourceRef


@runtime_checkable
class PermissionChecker(Protocol):
    name: str

    async def accessible_ids(
        self,
        principal: PrincipalContext,
        kind: str,
        action: str,
        logger: logging.Logger,
    ) -> frozenset[str] | None:
        """Return the ids of `kind` the principal may `action`.

        Returns `None` to opt out of filtering, or a `frozenset[str]` of permitted ids
        (possibly empty).
        """
        ...

    async def require(
        self,
        principal: PrincipalContext,
        resource: ResourceRef,
        action: str,
        logger: logging.Logger,
    ) -> None:
        """Raise if the principal may not `action` `resource`.

        `ResourceRef.id == None` is a kind-level / fleet-level check — "may the
        principal `action` resources of this kind" — used at create-time before any
        id has been minted, and for system-typed checks that have no associated id.
        Plugins should treat `None` distinctly from any concrete id; never compare
        against `""`.
        """
        ...
