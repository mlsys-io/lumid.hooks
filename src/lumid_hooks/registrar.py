"""Resource lifecycle hook.

Plugins implementing this protocol learn about resource creation and
destruction so they can seed their own ACL / ownership tables. The host
fires `register` after a resource is persisted and `deregister` after a
resource is hard-deleted or self-terminated.

`principal` is always a real `PrincipalContext`. For system-initiated paths
the host resolves a system principal at startup via the `IdentityProvider`
chain.

Multiple registrars compose: every registrar's `register` runs in
registration order; failures propagate and abort the originating request.
With no registrars registered both methods are no-ops.
"""

import logging
from typing import Protocol, runtime_checkable

from .principal import PrincipalContext
from .resource import ResourceRef


@runtime_checkable
class ResourceRegistrar(Protocol):
    name: str

    async def register(
        self,
        principal: PrincipalContext,
        resource: ResourceRef,
        logger: logging.Logger,
    ) -> None:
        """Record that `principal` created `resource`.

        `resource.metadata` carries resource-specific context (e.g. a workflow
        name, a worker hardware shape) that the plugin may persist alongside
        the ownership row. Plugins should ignore unknown keys.
        """
        ...

    async def deregister(
        self,
        principal: PrincipalContext,
        resource: ResourceRef,
        logger: logging.Logger,
    ) -> None:
        """Record that `resource` no longer exists.

        `principal` is the actor performing the destruction (the calling admin
        for request-driven teardowns, or the resolved system principal for
        host-initiated teardowns). Plugins typically drop the ownership row
        regardless of who initiated the destruction.
        """
        ...
