"""`ResourceRegistrar` example: write-through to in-memory ownership table."""

import logging

from lumid_hooks import PrincipalContext, ResourceRef

from . import state


class SimpleResourceRegistrar:
    name = "simple_plugin.registrar"

    async def register(
        self,
        principal: PrincipalContext,
        resource: ResourceRef,
        logger: logging.Logger,
    ) -> None:
        if resource.id is None:
            logger.warning(
                "%s: skipping register for kind-level ref kind=%s",
                self.name,
                resource.kind,
            )
            return
        state.OWNERSHIP[(resource.kind, resource.id)] = principal.principal_id
        logger.info(
            "%s: %s -> %s/%s",
            self.name,
            principal.principal_id,
            resource.kind,
            resource.id,
        )

    async def deregister(
        self,
        principal: PrincipalContext,
        resource: ResourceRef,
        logger: logging.Logger,
    ) -> None:
        if resource.id is None:
            return
        prev = state.OWNERSHIP.pop((resource.kind, resource.id), None)
        logger.info(
            "%s: actor=%s removed %s/%s (was_owner=%s)",
            self.name,
            principal.principal_id,
            resource.kind,
            resource.id,
            prev,
        )
