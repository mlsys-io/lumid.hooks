"""Resource reference passed to permission and registrar hooks."""

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResourceRef(BaseModel):
    """Reference to a project-specific resource.

    `kind` is a plugin-defined string (e.g. `"workflow"`, `"job"`,
    `"table"`); `lumid-hooks` does not enumerate kinds.

    `id=None` denotes a kind-level / fleet-level reference used at create-time
    before any id has been minted, and for system-typed checks that have no
    associated id. Plugins should treat `None` distinctly from any concrete id;
    never compare against `""`.
    """

    model_config = ConfigDict(frozen=True)

    kind: str = Field(description="Plugin-defined resource kind.")
    id: str | None = Field(
        default=None,
        description="Concrete resource id, or `None` for a kind-level reference.",
    )
    metadata: Mapping[str, Any] = Field(
        default_factory=dict,
        description="Resource-specific context the project attaches at registration "
        "time; plugins may persist or ignore unknown keys.",
    )
